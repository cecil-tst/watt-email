#!/usr/bin/env python3
"""inventario.py - genera reports/inventario.md a partir de metadatos guardados en data/.

FASE 1 (solo lectura). Este script NO accede al buzón.

Por qué el script no llama a Gmail: el conector de Gmail es una herramienta MCP de la sesión de
Claude; un proceso Python no puede invocarla. El flujo es:

  1. La sesión (solo herramientas de lectura) pagina
         search_threads(query="in:inbox newer_than:90d", view=THREAD_VIEW_SUMMARY)
     y vuelca a data/threads*.tsv solo: thread_id, msg_count, date, sender, display_name,
     to, labels, subject  (8 columnas separadas por tab; sin snippets, sin cuerpos, sin adjuntos).
  2. Para adjuntos, la sesión lanza consultas THREAD_VIEW_IDS_ONLY (has:attachment, filename:pdf, ...)
     y guarda los IDs en data/attachments.json (claves: any, pdf, xls_csv, doc, img, zip_gz, ics_xml_ppt).
  3. data/labels.json (id -> nombre de las etiquetas de usuario) sale de list_labels.
  4. data/notas.txt (opcional): una línea por hallazgo, se copia a la sección final.
  5. Este script lee data/ y genera el informe de forma determinista.

Rehacer el informe requiere volver a ejecutar el paso 1-3 en una sesión con el conector.
Las categorías propuestas son una heurística («propuesta»); la fuente de verdad sigue siendo
rules/categories.yaml, que valida Cecil. El script solo comprueba que las categorías que usa existan ahí.

Uso:  python3 scripts/inventario.py [--ahora AAAA-MM-DD]
Solo biblioteca estándar.
"""
import argparse
import collections
import datetime as dt
import glob
import json
import os
import re
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "reports", "inventario.md")
CATS_FILE = os.path.join(ROOT, "rules", "categories.yaml")

SELF = "cecil@the-storytellers.es"
INTERNAL = {"the-storytellers.es", "thefoodtellers.com"}
GROUPS = {"hola@the-storytellers.es", "hola@thefoodtellers.com", "admin@thefoodtellers.com",
          "dev@the-storytellers.es", "ai@the-storytellers.es"}
COLLEAGUES = {"nacho", "jair"}
FREEMAIL = {"gmail.com", "outlook.com", "hotmail.com", "yahoo.com", "msn.com", "icloud.com", "live.com"}
VIA = re.compile(r"^'?(.+?)'?\s+via\s+(.+)$")
NO_CLASIF = "?"

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Europe/Madrid")
except Exception:  # sin tzdata: UTC+1 (aproximación)
    TZ = dt.timezone(dt.timedelta(hours=1))

# ---------------------------------------------------------------- reglas de categoría (PROPUESTA)
# (regex sobre "sender|nombre|dominio|clave|to:destino", regex de asunto o None, categoría, certeza, nota)
# La primera regla que encaja gana. Las categorías deben existir en rules/categories.yaml.
R = [
    (r"to:cecil\.servan@", None, "ofertas-comerciales", "media", "alias usado solo por captación en frío"),
    (r"aeat", None, "impuestos", "alta", ""),
    (r"cve-advocats", None, "impuestos", "media", "gestoría"),
    (r"gencat\.cat|enotum\.cat", None, NO_CLASIF, "dudoso", "administración pública: ¿categoría nueva?"),
    (r"registradores\.org", None, "alertas", "media", ""),
    (r"notificaciones-bbva", None, "bancos", "alta", ""),
    (r"comunica\.bbva", None, "ofertas-comerciales", "media", "marketing bancario"),
    (r"stripe\.com|via:anthropic, pbc", None, "facturas-saas", "alta", ""),
    (r"payments-noreply@google\.com|via:google payments", None, "facturas-saas", "alta", ""),
    (r"via:(metricool|canva)", None, "facturas-saas", "alta", ""),
    (r"via:(sumup|no reply - mailchimp)", None, "facturas-saas", "media", ""),
    (r"via:siteground\|", None, "facturas-saas", "alta", ""),
    (r"growth-lab|rmdisseny|via:rafa", None, "facturas-proveedores", "alta", ""),
    (r"ivanberbel", None, NO_CLASIF, "dudoso", "factura recibida: ¿proveedor o cliente?"),
    (r"via:paypal", r"recibo de su pago", "pagos-cobros", "alta", ""),
    (r"via:paypal", None, "newsletters", "media", ""),
    (r"via:open arms", None, "pagos-cobros", "media", "donación recurrente"),
    (r"tm\.openai\.com", r"reloaded|charged", "pagos-cobros", "alta", ""),
    (r"tm\.openai\.com", r"renews", "recordatorios-suscripcion", "alta", ""),
    (r"tm\.openai\.com", r"credits|usage", "alertas", "media", "plataforma"),
    (r"tm\.openai\.com", r"access|export|exportaci", "cuentas-usuario", "media", ""),
    (r"tm\.openai\.com", None, NO_CLASIF, "dudoso", "asunto no concluyente"),
    (r"email\.openai\.com|via:openai ads", None, "newsletters", "alta", ""),
    (r"holded\.com", r"factura", "facturas-proveedores", "media", ""),
    (r"holded\.com", r"verificaci|invitado", "cuentas-usuario", "alta", ""),
    (r"holded\.com", None, NO_CLASIF, "dudoso", "asunto no concluyente"),
    (r"via:holded de holded", None, "info-servicio", "media", "soporte"),
    (r"via:.*holded", None, "newsletters", "media", ""),
    (r"txn\.dropbox\.com", None, "recordatorios-suscripcion", "media", "renovación/recibo"),
    (r"dropbox\.com", None, "alertas", "alta", ""),
    (r"@github\.com", None, "alertas", "alta", ""),
    (r"(system|notifications)@vercel\.com", None, "alertas", "alta", ""),
    (r"no-reply@accounts\.google\.com", None, "alertas", "alta", ""),
    (r"info\.vercel\.com", None, "newsletters", "alta", ""),
    (r"link\.com", None, "cuentas-usuario", "media", ""),
    (r"support@wpvibe\.ai|via:wpvibe\||via:the cirqle|via:anthropic\|", None, "cuentas-usuario", "alta", ""),
    (r"via:chatgpt", r"código|code", "cuentas-usuario", "alta", ""),
    (r"via:chatgpt", None, NO_CLASIF, "dudoso", "asunto no concluyente"),
    (r"john@wpvibe\.ai|via:john turner", None, "newsletters", "alta", ""),
    (r"workspace-noreply@google\.com|cloudplatform-noreply@google\.com|businessprofile-noreply@google\.com",
     None, "info-servicio", "media", ""),
    (r"wordpress@thefoodtellers\.com", r"contraseña|usuario", "cuentas-usuario", "media", ""),
    (r"wordpress@", None, "info-servicio", "alta", ""),
    (r"noreply@wpml\.org|jira@the-storytellers\.atlassian\.net|infoweb@ub\.edu|via:siteground autoupdate|"
     r"via:(meta for business|the meta business team)", None, "info-servicio", "media", ""),
    (r"\|dmarc\|", None, "info-servicio", "alta", "informes DMARC"),
    (r"no-reply@cdmon\.com", None, "recordatorios-suscripcion", "alta", "caducidad de dominios"),
    (r"via:marina de cdmon", None, "newsletters", "media", ""),
    (r"sanity\.io|mosyle", None, "recordatorios-suscripcion", "media", "trial"),
    (r"dreamhost", r"receipt", "facturas-saas", "alta", ""),
    (r"dreamhost", r"renewal notice", "recordatorios-suscripcion", "alta", ""),
    (r"dreamhost", r"upgrade|password", "info-servicio", "media", ""),
    (r"dreamhost", None, NO_CLASIF, "dudoso", "asunto no concluyente"),
    (r"iahub\.space|e\.atlassian\.com|po\.atlassian\.net|email\.claude\.com|openarms\.es|allthose|lifeandthyme|"
     r"emexs\.es|fetalifetech|komkal|news\.wpml\.org|"
     r"via:(password protected|wpbakery page builder|siteground web hosting)", None, "newsletters", "alta", ""),
    (r"s:(nacho|jair)@", None, "conversaciones", "alta", "interno"),
    (r"botiga@canal\.es", None, "info-servicio", "alta", "avisos de WordPress de un cliente"),
    (r"trello\.com", None, "conversaciones", "media", "menciones de compañeros"),
    (r"via:(george garnish|camila perchik|locutora susana garcia|gabriel martínez|maría rojas díaz)",
     None, "ofertas-comerciales", "media", "captación en frío"),
    (r"via:justicia alimentaria", None, NO_CLASIF, "dudoso", "entidad/cliente: boletín y presupuesto"),
    (r"no-reply@the-storytellers\.es", None, NO_CLASIF, "dudoso", "formulario web: requiere cuerpo"),
    (r"@(gmail|outlook|hotmail|yahoo|msn|icloud|live)\.", None, NO_CLASIF, "dudoso", "particular: requiere cuerpo"),
]
R = [(re.compile(a), re.compile(b) if b else None, c, d, e) for a, b, c, d, e in R]
KW_ANUAL = re.compile(r"renov|caduc|expire|renew|anual|annual|dominio|domain|suscripci|subscription", re.I)


def load_cat_ids():
    ids = []
    with open(CATS_FILE, encoding="utf-8") as f:
        for ln in f:
            m = re.match(r"\s*-\s*id:\s*(\S+)", ln)
            if m:
                ids.append(m.group(1))
    return ids


def mask(s, n=46, emails=True):
    s = re.sub(r"\d{5,}", "***", s)
    if emails:
        s = re.sub(r"\S+@\S+", "<email>", s)
    s = s.replace("|", "/").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def load_threads():
    rows, bad = {}, 0
    for fn in sorted(glob.glob(os.path.join(DATA, "threads*.tsv"))):
        with open(fn, encoding="utf-8") as f:
            for ln in f:
                ln = ln.rstrip("\n")
                if not ln.strip() or ln.startswith("thread_id\t"):
                    continue
                p = ln.split("\t")
                if len(p) != 8:
                    bad += 1
                    continue
                tid, n, d, sender, dn, to, labels, subj = p
                if tid in rows:
                    continue
                when = dt.datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(TZ)
                rows[tid] = dict(id=tid, n=int(n), when=when, sender=sender.strip().lower(), dn=dn.strip(),
                                 to=(to.strip().lower() or SELF), labels=labels.split(","), subject=subj.strip())
    return rows, bad


def entity(t):
    """Devuelve (clave, nombre real/visible, dominio, tipo)."""
    s, dn, subj = t["sender"], t["dn"], t["subject"].lower()
    dom = s.split("@")[-1]
    if re.match(r"(report domain|dmarc aggregate report)", subj):
        return "dmarc", "Informes DMARC (thefoodtellers.com)", "(informes DMARC)", "dmarc"
    m = VIA.match(dn)
    if s in GROUPS and m:
        real = m.group(1).strip(" '")
        return "via:" + real.lower(), f"{real} [vía grupo]", "vía grupo (desconocido)", "via"
    if s == SELF:
        to = t["to"]
        return "s:" + to, to, to.split("@")[-1], "propio"
    if dom in INTERNAL and s.split("@")[0] in COLLEAGUES:
        to = t["to"]
        if to.split("@")[-1] not in INTERNAL:
            return "s:" + to, to, to.split("@")[-1], "propio"
        return "s:" + s, dn or s, dom, "interno"
    return "s:" + s, dn or s, dom, "normal"


def classify(t, ent):
    key, name, dom, kind = ent
    real = name.replace(" [vía grupo]", "") if kind == "via" else t["dn"]
    hay = f"{t['sender']}|{real.lower()}|{dom}|{key}|to:{t['to']}|".lower()
    if key == "dmarc":
        hay = "|dmarc|"
    subj = t["subject"].lower()
    for rx, sx, cat, cert, note in R:
        if rx.search(hay) and (sx is None or sx.search(subj)):
            return cat, cert, note
    if "CATEGORY_PROMOTIONS" in t["labels"]:
        return "newsletters", "media", "pestaña Promociones de Gmail"
    return NO_CLASIF, "dudoso", "sin regla: requiere cuerpo"


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def blocks(title_fn, headers, rows, size=10):
    out = []
    for i in range(0, len(rows), size):
        chunk = rows[i:i + size]
        out.append(f"**{title_fn(i + 1, i + len(chunk))}**\n")
        out.append(table(headers, chunk))
        out.append("")
    return "\n".join(out)


def pct(a, b):
    return f"{(100.0 * a / b):.0f} %" if b else "0 %"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ahora", default=None)
    args = ap.parse_args()

    cat_ids = load_cat_ids()
    rows, bad = load_threads()
    if not rows:
        sys.exit("No hay datos en data/threads*.tsv")
    for _, _, c, _, _ in R:
        assert c == NO_CLASIF or c in cat_ids, f"categoría inexistente en categories.yaml: {c}"

    T = sorted(rows.values(), key=lambda t: t["when"])
    total = len(T)
    ahora = dt.date.fromisoformat(args.ahora) if args.ahora else T[-1]["when"].date()
    desde = ahora - dt.timedelta(days=90)
    msgs = sum(t["n"] for t in T)
    unread = sum(1 for t in T if "UNREAD" in t["labels"])
    sent_only = sum(1 for t in T if t["labels"] == ["SENT"])

    # entidades
    ents = collections.OrderedDict()
    for t in T:
        e = entity(t)
        t["ent"] = e
        t["cat"], t["cert"], t["note"] = classify(t, e)
        d = ents.setdefault(e[0], dict(key=e[0], names=collections.Counter(), dom=e[2], kind=e[3], th=[]))
        d["names"][e[1] if e[3] in ("via", "propio", "dmarc") else (t["dn"] or e[1])] += 1
        d["th"].append(t)

    def ent_label(d):
        if d["dom"] in FREEMAIL:
            return f"(particular @{d['dom']})"
        nm = d["names"].most_common(1)[0][0]
        addr = d["key"][2:] if d["key"].startswith("s:") else ""
        lab = nm if (not addr or nm == addr or d["kind"] in ("via", "dmarc")) else f"{nm} ({addr})"
        return mask(lab, 52, emails=False)

    for d in ents.values():
        cs = collections.Counter(t["cat"] for t in d["th"])
        certs = {t["cert"] for t in d["th"]}
        known = {c for c in cs if c != NO_CLASIF}
        if len(known) == 1 and NO_CLASIF not in cs:
            d["cat"] = next(iter(known))
            d["cert"] = "media" if "media" in certs else "alta"
            d["motivo"] = ""
        elif not known:
            d["cat"], d["cert"] = NO_CLASIF, "dudoso"
            d["motivo"] = d["th"][-1]["note"]
        else:
            d["cat"], d["cert"] = "mixto", "mixto"
            d["motivo"] = "mixto: " + "/".join(sorted(known)) + ("/?" if NO_CLASIF in cs else "")
        d["n"] = len(d["th"])
        d["label"] = ent_label(d)

    # semanas
    def monday(d):
        return d - dt.timedelta(days=d.weekday())
    wk = collections.Counter(monday(t["when"].date()) for t in T)
    wkm = collections.Counter()
    for t in T:
        wkm[monday(t["when"].date())] += t["n"]
    w0, w1 = min(wk), max(wk)
    weeks = []
    w = w0
    while w <= w1:
        weeks.append((w, wk.get(w, 0), wkm.get(w, 0)))
        w += dt.timedelta(days=7)
    assert sum(x[1] for x in weeks) == total, "las semanas no suman el total"

    # categorías gmail y etiquetas de usuario
    gcat = collections.Counter()
    for t in T:
        c = [l for l in t["labels"] if l.startswith("CATEGORY_")]
        gcat[c[0].replace("CATEGORY_", "").title() if c else "(sin pestaña)"] += 1
    lname = {}
    lp = os.path.join(DATA, "labels.json")
    if os.path.exists(lp):
        lname = json.load(open(lp, encoding="utf-8"))
    ucount = collections.Counter()
    for t in T:
        for l in t["labels"]:
            if l.startswith("Label_"):
                ucount[lname.get(l, l)] += 1

    # adjuntos
    att = json.load(open(os.path.join(DATA, "attachments.json"), encoding="utf-8"))
    ids = set(rows)
    sets = {k: set(v) for k, v in att.items()}
    outside = sets["any"] - ids
    a_any = sets["any"] & ids
    TIPOS = [("PDF", "pdf"), ("Imágenes (jpg/png/gif/webp)", "img"), ("ZIP/GZ (informes DMARC)", "zip_gz"),
             ("ICS/XML/PPT (invitaciones, DMARC)", "ics_xml_ppt"), ("Word/ODT", "doc"), ("Excel/CSV", "xls_csv")]

    # recurrentes
    mensuales, anuales, frecuentes = [], [], []
    for d in ents.values():
        days = sorted({t["when"].date().toordinal() for t in d["th"]})
        gaps = [b - a for a, b in zip(days, days[1:])]
        med = statistics.median(gaps) if gaps else None
        d["med"] = med
        if len(days) >= 3 and med is not None and 24 <= med <= 36:
            mensuales.append((d, "mensual", len(days), med))
        elif len(days) == 2 and 24 <= gaps[0] <= 36:
            mensuales.append((d, "posible mensual (2 obs.)", 2, gaps[0]))
        if len(days) >= 6 and med is not None and med <= 7:
            frecuentes.append(d)
        if any(KW_ANUAL.search(t["subject"]) for t in d["th"]):
            anuales.append(d)
    mens_keys = {d["key"] for d, *_ in mensuales}
    anuales = [d for d in anuales if d["key"] not in mens_keys]

    # resúmenes por categoría (hilo)
    tcat = collections.Counter(t["cat"] for t in T)
    tcert = collections.Counter(t["cert"] for t in T)
    ecat = collections.defaultdict(set)
    for t in T:
        ecat[t["cat"]].add(t["ent"][0])

    L = []
    A = L.append
    A("# Inventario del buzón · fase 1 (solo lectura)\n")
    A(f"- Generado: {ahora.isoformat()} · script `scripts/inventario.py` · propuesta, no validada por Cecil.")
    A(f"- Consulta: `in:inbox newer_than:90d` (desde {desde.isoformat()}). Hilos con mensajes en la ventana: "
      f"{T[0]['when'].date().isoformat()} → {T[-1]['when'].date().isoformat()}.")
    A("- **Unidad: hilos**, fechados por su último mensaje (zona Europe/Madrid). Los mensajes son una cifra "
      "aproximada (suma de `messageCount`).")
    A("- Solo metadatos: remitente, asunto, fecha, etiquetas. Sin cuerpos. Asuntos truncados y con dígitos largos "
      "enmascarados.")
    A("- Las categorías son una **propuesta** del script; `rules/categories.yaml` no se ha tocado.\n")

    A("## 1. Volumen\n")
    A(table(["Dato", "Valor"], [
        ["Hilos en la bandeja (90 d)", total],
        ["Mensajes (aprox.)", msgs],
        ["Hilos sin leer", f"{unread} ({pct(unread, total)})"],
        ["Hilos donde el último mensaje es tuyo (SENT)", sent_only],
        ["Media por semana", f"{total / len(weeks):.0f} hilos"],
    ]))
    A("\n**Por pestaña de Gmail**\n")
    A(table(["Pestaña", "Hilos", "%"], [[k, v, pct(v, total)] for k, v in gcat.most_common()]))
    A("")
    wr = [[i + 1, f"{w.strftime('%d/%m')} (S{w.isocalendar()[1]})", n, m] for i, (w, n, m) in enumerate(weeks)]
    A(blocks(lambda a, b: f"Por semana {a}-{b} (lunes de inicio)", ["#", "Semana", "Hilos", "Msgs"], wr))
    A("_Ojo: antes del 28/09 casi no hay hilos porque la bandeja solo guarda lo no archivado; no es el volumen real que llegó._")
    A(f"_Comprobación: las semanas suman {sum(x[1] for x in weeks)} = total {total}._\n")

    ranking = sorted(ents.values(), key=lambda d: (-d["n"], d["label"]))
    top = ranking[:40]
    assert sum(d["n"] for d in top) <= total
    A("## 2. Top 40 remitentes\n")
    A("«[vía grupo]» = el remitente real va detrás de un alias de grupo (hola@, ai@, dev@, admin@…). "
      "«→ x» = hilo cuyo último mensaje es de Cecil o de un compañero, contado por su interlocutor. "
      "Cat. = propuesta; «?» = dudoso; «mixto» = varía según el asunto.\n")
    tr = []
    for i, d in enumerate(top, 1):
        cat = d["cat"] if d["cert"] in ("alta", "media") else ("?" if d["cert"] == "dudoso" else "mixto")
        tr.append([i, d["label"], d["n"], cat])
    A(blocks(lambda a, b: f"Remitentes {a}-{b}", ["#", "Remitente", "Hilos", "Cat."], tr))
    A(f"_Top 40 = {sum(d['n'] for d in top)} hilos ({pct(sum(d['n'] for d in top), total)}) de {total}; "
      f"remitentes distintos: {len(ents)}._\n")

    dom = collections.defaultdict(lambda: [0, set()])
    for d in ents.values():
        dom[d["dom"]][0] += d["n"]
        dom[d["dom"]][1].add(d["key"])
    domr = sorted(dom.items(), key=lambda kv: (-kv[1][0], kv[0]))[:20]
    A("## 3. Top 20 dominios\n")
    A("«vía grupo (desconocido)» agrupa lo que llega por alias de grupo: el dominio real no se ve sin leer el "
      "mensaje.\n")
    A(blocks(lambda a, b: f"Dominios {a}-{b}", ["#", "Dominio", "Hilos", "Remitentes"],
             [[i, k if k not in FREEMAIL else f"{k} (particulares)", v[0], len(v[1])]
              for i, (k, v) in enumerate(domr, 1)]))

    A("## 4. Adjuntos\n")
    A(f"- Hilos con adjunto: **{len(a_any)} de {total} ({pct(len(a_any), total)})**"
      + (f" (+{len(outside)} hilo(s) que la consulta de adjuntos ve y el listado no)." if outside else "."))
    A("- El dato es **por hilo** (no por mensaje) y `has:attachment` cuenta también imágenes incrustadas: "
      "el % de «imágenes» está inflado por firmas y logos (p. ej. avisos de cdmon).")
    A("- Los tipos se solapan (un hilo puede tener PDF e imagen).\n")
    A(table(["#", "Tipo", "Hilos", "% de los adjuntos"],
            [[i, n, len(sets[k] & ids), pct(len(sets[k] & ids), len(a_any))] for i, (n, k) in enumerate(TIPOS, 1)]))
    A("")
    pdf_ents = collections.Counter()
    for t in T:
        if t["id"] in sets["pdf"]:
            pdf_ents[ents[t["ent"][0]]["label"]] += 1
    A("**Quién manda PDF (top 10)**\n")
    A(table(["#", "Remitente", "Hilos con PDF"], [[i, k, v] for i, (k, v) in enumerate(pdf_ents.most_common(10), 1)]))
    A("")

    A("## 5. Recurrencias\n")
    A("- Mensual: ≥3 fechas distintas con mediana entre 24 y 36 días (o 2 fechas a 24-36 días = «posible»). "
      "Con 90 días **no se puede detectar lo anual**: abajo solo van pistas por palabras del asunto.")
    A("- Ojo: la bandeja solo contiene lo no archivado; si algo se archiva a mano, aquí se ve menos de lo que llega.\n")
    mr = sorted(mensuales, key=lambda x: (-x[2], x[0]["label"]))
    A(blocks(lambda a, b: f"Mensuales {a}-{b}", ["#", "Remitente", "Veces", "Tipo", "Cat."],
             [[i, d["label"], n, tipo, d["cat"] if d["cert"] in ("alta", "media") else d["cert"]]
              for i, (d, tipo, n, _) in enumerate(mr, 1)]) if mr else "_Ninguno._\n")
    fr = sorted(frecuentes, key=lambda d: -d["n"])[:10]
    A("**Alta frecuencia (≥6 fechas, mediana ≤7 días; top 10)**\n")
    A(table(["#", "Remitente", "Hilos", "Cat."], [[i, d["label"], d["n"],
            d["cat"] if d["cert"] in ("alta", "media") else d["cert"]] for i, d in enumerate(fr, 1)]) if fr
      else "_Ninguno._")
    A("")
    an = sorted(anuales, key=lambda d: -d["n"])[:10]
    A("**Posible anual (solo pista por palabras: renov/caduc/dominio/suscripción…; top 10)**\n")
    A(table(["#", "Remitente", "Hilos", "Ejemplo de asunto"], [[i, d["label"], d["n"], mask(
        next(t["subject"] for t in d["th"] if KW_ANUAL.search(t["subject"])), 40)] for i, d in enumerate(an, 1)])
      if an else "_Ninguno._")
    A("\n_Propuesta: un barrido de 12 meses solo de metadatos confirmaría lo anual. No se amplía la ventana sin tu OK._\n")

    A("## 6. Categorías tentativas y dudosos\n")
    A("Reparto de **hilos** por categoría propuesta (por hilo, no por remitente):\n")
    crow = []
    for i, c in enumerate(cat_ids, 1):
        crow.append([i, c, tcat.get(c, 0), len(ecat.get(c, ()))])
    crow.append([len(cat_ids) + 1, "**? dudoso (sin regla)**", tcat.get(NO_CLASIF, 0), len(ecat.get(NO_CLASIF, ()))])
    A(blocks(lambda a, b: f"Categorías {a}-{b}", ["#", "Categoría", "Hilos", "Remitentes"], crow))
    cl = tcert.get("alta", 0) + tcert.get("media", 0)
    A(f"_Clasificables por remitente/asunto: {cl} hilos ({pct(cl, total)}); alta {tcert.get('alta', 0)}, "
      f"media {tcert.get('media', 0)}; dudosos {tcert.get('dudoso', 0)} ({pct(tcert.get('dudoso', 0), total)})._\n")
    dud = sorted([d for d in ents.values() if d["cert"] in ("dudoso", "mixto")], key=lambda d: (-d["n"], d["label"]))
    A(f"**Dudosos y mixtos: {len(dud)} remitentes ({sum(d['n'] for d in dud)} hilos). Se muestran los 30 con más hilos.**\n")
    A("«mixto» = una regla por remitente no basta, pero el asunto sí distingue (no hace falta leer cuerpo). "
      "«?» = hace falta abrir el cuerpo o que Cecil decida.\n")
    dr = []
    for i, d in enumerate(dud[:30], 1):
        ej = mask(d["th"][-1]["subject"], 34)
        mot = d["motivo"] if d["cert"] == "mixto" else f"? {d['motivo']}"
        dr.append([f"D{i}", d["label"], d["n"], f"{mot} · «{ej}»" if d["cert"] == "dudoso" else mot])
    A(blocks(lambda a, b: f"Dudosos D{a}-D{b}", ["#", "Remitente", "Hilos", "Motivo / ejemplo"], dr))
    if len(dud) > 30:
        A(f"_Quedan {len(dud) - 30} remitentes más (casi todos con 1-2 hilos), no listados._\n")

    A("## 7. Etiquetas de usuario ya en uso (en estos hilos)\n")
    A("Tu buzón ya tiene un sistema de etiquetas. Conviene respetarlo en la fase 2.\n")
    A(table(["#", "Etiqueta", "Hilos"], [[i, k, v] for i, (k, v) in enumerate(ucount.most_common(10), 1)]))
    A("")

    A("## 8. Hallazgos y límites\n")
    npth = os.path.join(DATA, "notas.txt")
    if os.path.exists(npth):
        for ln in open(npth, encoding="utf-8"):
            if ln.strip():
                A(f"- {ln.strip()}")
    if bad:
        A(f"- {bad} líneas de data/ con formato incorrecto, ignoradas.")
    A("- La vista SUMMARY devuelve el último mensaje de cada hilo: en hilos largos el remitente puede ser el último "
      "que contestó, no quien lo abrió.")
    A("- Los alias («Hola», «AI», «Dev Team», «Admin TFT») ocultan al remitente real; ya se agrupan por nombre visible.")
    A("- Para regenerar este informe hay que repetir la extracción en una sesión con el conector de Gmail (ver cabecera "
      "del script). `data/` se borra al cerrar la tarea (regla 6).")
    A("- Sin cuerpos ni adjuntos abiertos; no se ha escrito nada en el buzón.")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"OK: {total} hilos, {len(ents)} remitentes, {len(a_any)} con adjunto, informe en {OUT}")


if __name__ == "__main__":
    main()
