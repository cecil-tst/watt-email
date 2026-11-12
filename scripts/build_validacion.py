#!/usr/bin/env python3
"""build_validacion.py - genera la propuesta de validación (fase 1, solo lectura).

Salidas:
  proposals/2026-11-10-validacion.json   (fuente: casos con opciones)
  reports/validacion.html                (artefacto interactivo autocontenido, JSON embebido)

Sin datos sensibles: solo patrones de remitente, recuentos, asuntos truncados/enmascarados.
Uso: python3 scripts/build_validacion.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FECHA = "2026-11-10"

CATS = [
    ("spam", "Spam"), ("newsletters", "Newsletters"), ("info-servicio", "Info de servicio"),
    ("conversaciones", "Conversaciones"), ("ofertas-comerciales", "Ofertas comerciales"),
    ("alertas", "Alertas"), ("recordatorios-suscripcion", "Recordatorios/renovación"),
    ("pagos-cobros", "Pagos y cobros"), ("facturas-proveedores", "Facturas proveedores"),
    ("facturas-saas", "Facturas SaaS"), ("bancos", "Bancos"), ("impuestos", "Impuestos/gestoría"),
    ("cuentas-usuario", "Cuentas de usuario"), ("administracion-publica", "Administración pública (NUEVA)"),
    ("etiquetas", "Etiquetas existentes"), ("otros", "Otros"),
]

# Vocabulario fase 2: etiquetar+archivar | etiquetar y mantener en bandeja | pseudo-snooze | archivar con Sensible |
# borrar (confirmación individual). Fase 4: PDF -> Drive/Holded | acción manual de Cecil | —


def O(k, cat, f2, f4="—", rec=False):
    return dict(k=k, categoria=cat, f2=f2, f4=f4, recomendada=rec)


def C(id, titulo, patron, h90, h13, rec, ej, cat, ops, reglas=None, nota=None, tipo="remitente"):
    d = dict(id=id, tipo=tipo, titulo=titulo, patron=patron, hilos_90d=h90, hilos_13m=h13,
             recurrencia=rec, ejemplo=ej, categoria=cat, opciones=ops)
    if reglas:
        d["reglas"] = reglas
    if nota:
        d["nota"] = nota
    return d


AP = "administracion-publica"
CASOS = [
    # ---- administración pública / impuestos
    C("c01", "AEAT", "AgenciaTributaria@correo.aeat.es", 10, "31", "mensual (13/14 meses, en racimos)",
      "Aviso de notificación / comunicación AEAT", AP, [
          O("A", AP, "Etiquetar y mantener en bandeja (tienen plazo)", "PDF → Drive/Impuestos", True),
          O("B", "impuestos", "Etiquetar y mantener en bandeja", "PDF → Drive/Impuestos"),
          O("C", AP, "Etiquetar + archivar", "—"),
      ], nota="El asunto es genérico: la acción exacta depende de que sean notificaciones con plazo."),
    C("c02", "Gestoría CVE Advocats", "@cve-advocats.com", 9, "42", "mensual (12/14 meses)",
      "Re: documentación / modelos trimestrales", "impuestos", [
          O("A", "impuestos", "Etiquetar (GESTOR) y mantener en bandeja", "Adjuntos PDF → Drive/Gestoría", True),
          O("B", "conversaciones", "Etiquetar y mantener en bandeja", "—"),
      ], nota="9 hilos con 4 PDF en 90 d. Hilo de conversación real: no archivar solo."),
    C("c03", "Gencat · plataforma de contractació", "plataforma.contractacio@gencat.cat", 5, "≥50 (con c04)",
      "irregular", "Novetats de E2343 Consorci de Serveis…", AP, [
          O("A", AP, "Etiquetar + archivar", "—", True),
          O("B", AP, "Etiquetar y mantener en bandeja", "—"),
          O("C", "info-servicio", "Etiquetar + archivar", "—"),
      ], nota="Novedades de un expediente de licitación. Si Cecil sigue ese expediente, B."),
    C("c04", "CSUC · avisos de notificación", "Consorci de Serveis Universitaris de Catalunya", 4, "≥50 (con c03)",
      "irregular", "IMPORTANT: Avís de notificació de…", AP, [
          O("A", AP, "Etiquetar y mantener en bandeja (notificación con plazo)", "—", True),
          O("B", AP, "Etiquetar + archivar", "—"),
      ], nota="Asunto marcado IMPORTANT. No se ha leído el cuerpo."),
    C("c05", "Avisos puntuales de caducidad", "Junta AFA, Mosyle, Sanity, Registradores", 4, "1-2 por año",
      "anual/puntual", "Fwd: Notificación de caducidad de certi…", "recordatorios-suscripcion", [
          O("A", "recordatorios-suscripcion", "Etiquetar + pseudo-snooze hasta fecha de caducidad", "Acción manual de Cecil", True),
          O("B", "alertas", "Etiquetar y mantener en bandeja", "—"),
          O("C", AP, "Etiquetar y mantener en bandeja", "—"),
      ], nota="Casos de 1 hilo cada uno; sirve de regla común. El certificado de Junta AFA es un reenvío."),
    # ---- remitentes mixtos: reglas por asunto
    C("c06", "OpenAI / ChatGPT Business (mixto)", "noreply@tm.openai.com", 12, "14 (desde 30-sep)",
      "racimos recientes", "WATT is out of credits", "alertas", [
          O("A", "(por asunto)", "Aplicar reglas por asunto, etiquetar + archivar salvo renovación", "—", True),
          O("B", "alertas", "Todo a Alertas, etiquetar y mantener", "—"),
          O("C", "cuentas-usuario", "Solo etiquetar", "—"),
      ], reglas=[
          dict(asunto="credit balance has been reloaded / auto-reload", categoria="pagos-cobros"),
          dict(asunto="out of credits / Add credits / credits remaining / requested more usage", categoria="alertas"),
          dict(asunto="Business subscription renews soon", categoria="recordatorios-suscripcion"),
          dict(asunto="exportación de datos / app's access updated / Your ChatGPT code is", categoria="cuentas-usuario"),
      ], nota="Aparece desde 30-sep: no hay histórico para saber si la renovación es mensual o anual (renueva el día 1)."),
    C("c07", "DreamHost (mixto)", "support@dreamhost.com", 8, "66", "mensual (14 meses, ~5/mes)",
      "[cecser …] <dominio>: Domain Renewal Notice", "recordatorios-suscripcion", [
          O("A", "(por asunto)", "Aplicar reglas por asunto; recibos archivados con etiqueta", "Recibos PDF → Drive/Facturas", True),
          O("B", "facturas-saas", "Todo a facturas-saas", "Recibos PDF → Drive/Facturas"),
          O("C", "info-servicio", "Solo etiquetar", "—"),
      ], reglas=[
          dict(asunto="Domain Name Renewal Receipt / renewal success! / PayPal AutoPay Payment Receipt", categoria="facturas-saas"),
          dict(asunto="Domain Renewal Notice (último aviso)", categoria="recordatorios-suscripcion"),
          dict(asunto="database server upgrade / Update passwords for all users", categoria="info-servicio"),
      ], nota="Hay dominios de clientes con hilo propio (renovación de 1 año, p. ej. oct y dic). La reventa a cliente sería fase 4: a validar."),
    C("c08", "Holded no-reply (mixto)", "no-reply@send.holded.com", 7, "33", "mensual (13/14 meses)",
      "Factura A-… de <proveedor> a We are The Tellers", "facturas-proveedores", [
          O("A", "(por asunto)", "Reglas por asunto; facturas con etiqueta Facturas + __POR PAGAR", "Enlace de factura → Holded (registrar)", True),
          O("B", "facturas-proveedores", "Todo a facturas-proveedores", "—"),
      ], reglas=[
          dict(asunto="Factura A-… de … a We are The Tellers", categoria="facturas-proveedores"),
          dict(asunto="Código de verificación (2FA)", categoria="cuentas-usuario"),
      ], nota="La factura llega ~14 de cada mes con vencimiento a 7 días: candidata a pseudo-snooze. 2FA: no se guarda nada."),
    C("c09", "Holded (equipo, soporte, marketing)", "El equipo de Holded [vía grupo], Eulàlia G. H.", 8, "—",
      "irregular", "Novedades Holded / Soporte", "newsletters", [
          O("A", "newsletters", "Etiquetar + archivar (soporte → info-servicio)", "—", True),
          O("B", "info-servicio", "Etiquetar y mantener", "—"),
      ]),
    C("c10", "WordPress / Wordfence (webs propias y de clientes)", "wordpress@thefoodtellers.com y otros dominios", 7, "≥50",
      "diaria + resumen semanal", "[Wordfence Alert] Problems found on …", "alertas", [
          O("A", "(por asunto)", "Reglas por asunto; etiqueta [Wordfence Alert] ya existente", "—", True),
          O("B", "info-servicio", "Todo etiquetado + archivado", "—"),
      ], reglas=[
          dict(asunto="Problems found / Acceso de administración / recuperación de contraseña", categoria="alertas"),
          dict(asunto="Actividad de Wordfence (resumen semanal)", categoria="info-servicio"),
          dict(asunto="Pendientes de moderación (comentarios)", categoria="info-servicio"),
          dict(asunto="Restablecer la contraseña", categoria="cuentas-usuario"),
      ], nota="Etiqueta existente [Wordfence Alert]: ~4.000 hilos acumulados."),
    C("c11", "Formulario web TST", "no-reply@the-storytellers.es", 6, "7 (8 muestras)",
      "irregular", "TST - CONTACTO WEB", "ofertas-comerciales", [
          O("A", "ofertas-comerciales", "Etiquetar y mantener 1 mes (revisar si hay leads reales)", "—", True),
          O("B", "spam", "Marcar spam (confirmación)", "—"),
          O("C", "conversaciones", "Etiquetar y mantener", "—"),
      ], nota="Los 7 fragmentos vistos eran captación en frío (tráfico, anuncios, SEO). Con un lead real el asunto es idéntico: no se distingue sin cuerpo."),
    C("c12", "PayPal [vía grupo]", "PayPal via hola@", 5, "≥50 (primera página)",
      "mensual (12/14)", "Recibo de su pago a …", "pagos-cobros", [
          O("A", "(por asunto)", "Reglas por asunto; recibos etiquetados + archivados", "Recibo → Drive/Pagos", True),
          O("B", "pagos-cobros", "Todo a pagos-cobros", "—"),
      ], reglas=[
          dict(asunto="Recibo de su pago", categoria="pagos-cobros"),
          dict(asunto="resto (promoción, novedades)", categoria="newsletters"),
      ]),
    C("c13", "Open Arms (donación)", "info@openarms.es, recibos vía PayPal", 3, "≥50 (primera página)",
      "mensual (12/14)", "Recibo / Gracias por tu donación", "pagos-cobros", [
          O("A", "pagos-cobros", "Recibos: etiquetar + archivar; boletín: newsletters", "Recibo → Drive/Donaciones", True),
          O("B", "newsletters", "Todo a newsletters", "—"),
      ], nota="La consulta mezcla otras menciones; el recuento es orientativo."),
    # ---- dudosos / pasivos
    C("c14", "Justicia Alimentaria [vía grupo]", "Justicia Alimentaria via hola@", 4, "—",
      "irregular", "HAGAMOS HUELGA DE COMPRAS …", "newsletters", [
          O("A", "newsletters", "Etiquetar + archivar", "—", True),
          O("B", "conversaciones", "Etiquetar y mantener (es entidad/cliente)", "—"),
      ], nota="Recomendación débil: el inventario anotó «boletín y presupuesto». Decide tú."),
    C("c15", "Particulares: candidaturas y consultas", "7 remitentes gmail/outlook", 7, "—",
      "puntual", "Application for Internship – …; Re: Envato Elements", "conversaciones", [
          O("A", "conversaciones", "Etiquetar y mantener en bandeja", "—", True),
          O("B", "otros", "Candidaturas a «otros», resto a conversaciones", "—"),
      ], nota="Requieren lectura humana; no se abrieron cuerpos."),
    C("c16", "Captación en frío (11 remitentes sueltos)", "seoprojects, tryember, bigfidelity, bookedlab, hypeauditorsapp…", 14, "—",
      "puntual", "Propuesta colaboración / Quick question", "ofertas-comerciales", [
          O("A", "ofertas-comerciales", "Etiquetar + archivar", "—", True),
          O("B", "spam", "Marcar spam (confirmación individual)", "—"),
      ], nota="Incluye el alias cecil.servan@ (solo capta ofertas)."),
    C("c17", "Contactos sueltos (CRG, Canal…)", "crg.eu, canal.es", 2, "—",
      "puntual", "RE: Slidedecks …; Test", "conversaciones", [
          O("A", "conversaciones", "Etiquetar y mantener en bandeja", "—", True),
          O("B", "info-servicio", "Etiquetar + archivar", "—"),
      ]),
    # ---- caso sensible
    C("c18", "Hilo UB con credenciales en claro (sistema retirado)", "hilo 1a0f…8834 · infoweb@ub.edu", 1, "1",
      "puntual", "Noves credencials …", "otros", [
          O("A", "otros", "Archivar con etiqueta Sensible", "—", True),
          O("B", "otros", "Borrar en fase 2 (confirmación individual)", "—"),
      ], nota="No se abrió el cuerpo. Aunque el sistema esté retirado, rotar la contraseña si se reutilizó.", tipo="sensible"),
    # ---- volumen alto: newsletters
    C("c19", "Newsletters de alta frecuencia", "IA Hub, Atlassian (marketing), John Turner/WPVibe, SiteGround Web Hosting, Emexs, OpenAI Ads, Claude Team…",
      80, "—", "semanal o más", "Newsletter semanal / novedades", "newsletters", [
          O("A", "newsletters", "Etiquetar + archivar por remitente (filtro)", "—", True),
          O("B", "newsletters", "Solo etiquetar, dejar en bandeja", "—"),
          O("C", "newsletters", "Etiquetar + archivar y proponer baja (confirmación individual)", "Baja manual"),
      ], nota="≈ 80 de 355 hilos (23 %). La baja de listas nunca es automática (regla 4)."),
    C("c20", "Atlassian Jira/Confluence (po.atlassian.net)", "noreply@po.atlassian.net", 5, "—",
      "irregular", "Actividad en Jira/Confluence", "info-servicio", [
          O("A", "info-servicio", "Etiquetar + archivar", "—", True),
          O("B", "conversaciones", "Etiquetar y mantener", "—"),
      ]),
    C("c21", "Códigos y accesos (2FA, verificación)", "GitHub, Vercel, Holded 2FA, WPVibe, ChatGPT, Link", 26, "—",
      "continua", "Código de verificación …", "cuentas-usuario", [
          O("A", "cuentas-usuario", "Etiquetar + archivar", "—", True),
          O("B", "cuentas-usuario", "Mantener en bandeja", "—"),
      ], nota="Los fragmentos incluyen códigos: no se guardan. Borrado solo con confirmación individual."),
    C("c22", "Alertas de plataformas (GitHub, Vercel)", "noreply@github.com, system@vercel.com", 8, "—",
      "continua", "[repo] PR / deployment", "alertas", [
          O("A", "alertas", "Etiquetar + archivar", "—", True),
          O("B", "alertas", "Mantener en bandeja", "—"),
      ]),
    C("c23", "Informes DMARC", "admin@thefoodtellers.com (vía grupo)", 9, "—",
      "diaria", "Report Domain: … Submitter: …", "info-servicio", [
          O("A", "info-servicio", "Etiquetar + archivar (ya hay etiqueta [NO REVISION])", "—", True),
          O("B", "info-servicio", "Solo etiquetar", "—"),
      ], nota="Adjuntos ZIP/GZ: no se guardan."),
    C("c24", "Google Workspace, Cloud, Search Console", "workspace-noreply@, cloudplatform-noreply@, sc-noreply@", 12, "≥50",
      "mensual (12/14)", "Te damos la bienvenida a la suscripción …", "info-servicio", [
          O("A", "info-servicio", "Etiquetar + archivar", "—", True),
          O("B", "recordatorios-suscripcion", "Facturas/renovación a recordatorios, resto info", "—"),
      ]),
    # ---- recurrencias financieras
    C("c25", "cdmon (dominios)", "no-reply@cdmon.com", 9, "50", "mensual (12/14, avisos repetidos por dominio)",
      "Recordatorio para la renovación de sus …", "recordatorios-suscripcion", [
          O("A", "recordatorios-suscripcion", "Etiquetar + pseudo-snooze hasta la caducidad; último aviso en bandeja", "Pago manual de Cecil", True),
          O("B", "recordatorios-suscripcion", "Etiquetar + archivar todos", "—"),
      ], nota="Regla útil: la caducidad real puede estar en el cuerpo (fase 4)."),
    C("c26", "SiteGround · confirmación de renovación", "'SiteGround' via hola@", 8, "15", "mensual, día 17 (13/14 meses)",
      "Confirmación de renovación del servicio", "facturas-saas", [
          O("A", "facturas-saas", "Etiquetar (Siteground) + archivar", "Adjunto/recibo → Drive/Facturas", True),
          O("B", "recordatorios-suscripcion", "Etiquetar + archivar", "—"),
      ], nota="Otros avisos de SiteGround van a newsletters/autoupdate (info-servicio)."),
    C("c27", "Recibos SaaS mensuales", "Google Payments, Dropbox, Metricool, Canva, SumUp", 12, "≈70",
      "mensual (13/14 meses)", "Gracias por renovar tu plan …", "facturas-saas", [
          O("A", "facturas-saas", "Etiquetar (Facturas) + archivar", "PDF → Drive/Facturas y Holded", True),
          O("B", "facturas-saas", "Etiquetar y mantener hasta conciliar (__POR CONCILIAR)", "PDF → Holded"),
      ], nota="Dropbox y Google Payments tienen 1 hilo/mes exacto: ideal para tarea programada."),
    C("c28", "Anthropic (Stripe)", "invoice+statements+…@stripe.com", 6, "6 (desde 22-oct)",
      "por compra, sin histórico", "Your receipt from Anthropic, PBC", "facturas-saas", [
          O("A", "facturas-saas", "Etiquetar (Facturas) + archivar", "PDF → Drive/Facturas y Holded", True),
          O("B", "pagos-cobros", "Etiquetar y mantener", "—"),
      ], nota="Cada hilo trae PDF (6/6)."),
    C("c29", "Proveedores: rafa, Growth Lab, rmdisseny", "rafa via hola@, growth-lab.es, rmdisseny.es", 6, "18",
      "mensual (10/14 meses)", "Factura nº … (PDF adjunto)", "facturas-proveedores", [
          O("A", "facturas-proveedores", "Etiquetar (Facturas + __POR PAGAR) y mantener hasta pago", "PDF → Drive y Holded", True),
          O("B", "facturas-proveedores", "Etiquetar + archivar", "PDF → Drive"),
      ]),
    C("c30", "BBVA · avisos y marketing", "notificaciones-bbva…, bbva@comunica.bbva.com", 7, "≥50 (primera página)",
      "mensual (12/14)", "Aviso de movimiento / Oferta BBVA", "bancos", [
          O("A", "(por remitente)", "Avisos → bancos (mantener); comunica.bbva → ofertas (archivar)", "—", True),
          O("B", "bancos", "Todo a bancos, etiquetar", "—"),
      ], nota="La gestora de BBVA (hilo largo de conversación) iría a conversaciones."),
    C("c31", "Equipo interno y Trello", "nacho@the-storytellers.es, Nacho Ballesta, Trello", 14, "—",
      "continua", "Re: … / Trello: mención", "conversaciones", [
          O("A", "conversaciones", "Etiquetar y mantener en bandeja (Trello → info-servicio)", "—", True),
          O("B", "conversaciones", "Mantener todo sin etiquetar", "—"),
      ]),
    # ---- etiquetas existentes (totales del buzón, no 90 d)
    C("c32", "Etiquetas de alias: TST/HOLA · TFT/Hola · TFT · TST", "etiquetas de usuario", 126, "totales: 7.185 / 5.198 / 1.191 / 4.254",
      "—", "(etiqueta)", "etiquetas", [
          O("A", "—", "Respetar: es la dimensión «entidad/alias»; la categoría se añade aparte", "—", True),
          O("B", "—", "Solo lectura: no se toca ni se añade categoría", "—"),
      ], tipo="etiqueta", nota="Propuesta: etiqueta de categoría WATT/<categoría> además de la tuya, nunca en su lugar."),
    C("c33", "Etiquetas de flujo: Facturas · __POR PAGAR · __POR CONCILIAR", "etiquetas de usuario", 10, "totales: 364 / 5 / 5",
      "—", "(etiqueta)", "etiquetas", [
          O("A", "facturas-*", "Facturas = estado archivado; __POR PAGAR/CONCILIAR son estado de flujo (no se tocan)", "Al pagar/conciliar: cambio manual de Cecil", True),
          O("B", "facturas-*", "Mapear Facturas ⇒ facturas-proveedores/SaaS; flujo intacto", "—"),
      ], tipo="etiqueta"),
    C("c34", "Etiquetas de filtro: [NO REVISION] · _NO_REVISION_ · SPAMDIGEST · Siteground · [Wordfence Alert]", "etiquetas de usuario", 60, "totales: 238 / 763 / 427 / 585 / 226 / 3.999",
      "—", "(etiqueta)", "etiquetas", [
          O("A", "newsletters / info-servicio", "Equivalen a «ruido ya triado»: mapear a categoría, no a bandeja", "—", True),
          O("B", "—", "Dejar como están, sin mapear", "—"),
      ], tipo="etiqueta"),
    C("c35", "Etiquetas de gestoría y clientes: GESTOR · GESTOR/Impuestos · GESTOR/Nominas · CLIENTE/* · DEV/* · Vice · ICM", "etiquetas de usuario", 0, "totales: 92 / 47 / 68 / varios",
      "—", "(etiqueta)", "etiquetas", [
          O("A", "impuestos / conversaciones", "GESTOR/* → impuestos; CLIENTE/DEV/Vice/ICM fuera de alcance de WATT", "—", True),
          O("B", "—", "Tratar todas como fuera de alcance", "—"),
      ], tipo="etiqueta", nota="Las etiquetas de cliente parecen de otro trabajo de Cecil; WATT solo gestiona finanzas y administración."),
]


def build():
    doc = dict(version="1", fecha=FECHA, fase=1, generado_por="sesion principal (sin hilos hijos)",
               nota="Propuesta. No se ha escrito nada en el buzón ni en rules/categories.yaml.",
               categorias=[dict(id=i, nombre=n) for i, n in CATS], casos=CASOS)
    os.makedirs(os.path.join(ROOT, "proposals"), exist_ok=True)
    jp = os.path.join(ROOT, "proposals", f"{FECHA}-validacion.json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "scripts", "validacion_template.html"), encoding="utf-8") as f:
        tpl = f.read()
    html = tpl.replace("/*__DATA__*/null", json.dumps(doc, ensure_ascii=False).replace("</", "<\\/"))
    with open(os.path.join(ROOT, "reports", "validacion.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("casos:", len(CASOS), "->", jp)


if __name__ == "__main__":
    build()
