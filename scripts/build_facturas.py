#!/usr/bin/env python3
"""build_facturas.py - ficha para clasificar remitentes de la etiqueta Facturas (proveedor / SaaS / cliente).
Reutiliza scripts/validacion_template.html. Salidas: proposals/2026-11-12-facturas-remitentes.json y
reports/facturas-remitentes.html. Solo nombre visible/dominio y recuentos; sin cuerpos ni direcciones de particulares."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F2 = "Etiquetar (Facturas) + archivar"
F4 = "Reenviar adjunto de factura a Holded (con lista aprobada)"
def C(id, tit, pat, h, rec, ej, nota, recom):
    ops = [
        dict(k="A", categoria="facturas-proveedores", f2=F2, f4=F4, recomendada=recom == "A"),
        dict(k="B", categoria="facturas-saas", f2=F2, f4=F4, recomendada=recom == "B"),
        dict(k="C", categoria="conversaciones", f2="Etiquetar y mantener en bandeja (cliente / factura emitida: no se reenvía a Holded)", f4="—", recomendada=recom == "C"),
    ]
    return dict(id=id, tipo="remitente", titulo=tit, patron=pat, hilos_90d=h, hilos_13m=h, recurrencia=rec,
                ejemplo=ej, categoria="facturas-proveedores" if recom == "A" else "facturas-saas" if recom == "B" else "conversaciones",
                opciones=ops, nota=nota)
CASOS = [
    C("f01", "Ivan Berbel (fotografía)", "ivanberbel.com y cuenta de gmail del mismo nombre", "2 + 1 antiguo", "irregular",
      "(PDF adjunto, sin asunto leído)", "Un hilo lleva __POR PAGAR y __POR CONCILIAR. El inventario lo marcó «¿proveedor o cliente?». No se abrió.", "A"),
    C("f02", "Claudia Martí Lladó (particular)", "cuenta gmail", 1, "puntual", "(PDF de 600 KB)", "Un solo hilo en feb-2026 con la etiqueta Facturas.", "A"),
    C("f03", "Javier Funez · aiavisuals.com", "info@aiavisuals.com", 1, "puntual", "(PDF adjunto)", "Un hilo en feb-2026. Por el dominio podría ser un servicio de IA (SaaS).", "A"),
    C("f04", "Xavi · xdesign.barcelona", "xavi@xdesign.barcelona", 1, "puntual", "(PDF de 770 KB)", "Estudio de diseño; un hilo en jun-2025.", "A"),
    C("f05", "Joan Aguadé (vía grupo hola@)", "Joan Aguadé via Hola | The Storytellers", 1, "puntual", "(conversación de 4 mensajes)", "Cecil contestó en el hilo (oct-2024): parece conversación, no factura recibida.", "C"),
    C("f06", "Daniel G Moreno (dominio gestionado en DreamHost)", "danielgmoreno.com", 1, "anual (renovación de dominio)", "(PDF de 450 KB, jun-2025)", "Los avisos de DreamHost de su dominio llegan a Cecil. Posible factura emitida a cliente.", "C"),
]
doc = dict(version="1", fecha="2026-11-12", fase=2, generado_por="sesion principal",
           nota="Muestra de la etiqueta Facturas; no es exhaustiva (364 hilos en total, la mayoría antiguos).",
           categorias=[dict(id=i, nombre=n) for i, n in [("facturas-proveedores", "Facturas de proveedores"), ("facturas-saas", "Facturas SaaS"), ("conversaciones", "Cliente / conversación")]],
           casos=CASOS)
json.dump(doc, open(os.path.join(ROOT, "proposals", "2026-11-12-facturas-remitentes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
t = open(os.path.join(ROOT, "scripts", "validacion_template.html"), encoding="utf-8").read()
t = t.replace("<title>Validación WATT</title>", "<title>Remitentes de facturas</title>").replace("Validación WATT · fase 1", "Remitentes de facturas")
t = t.replace("Una ficha por patrón. La opción marcada con «Recomendada» viene preseleccionada.", "Una ficha por remitente de la etiqueta Facturas: ¿proveedor, SaaS o cliente? La opción marcada con «Recomendada» es una suposición mía por el nombre y el dominio; no he leído los cuerpos.")
t = t.replace("/*__DATA__*/null", json.dumps(doc, ensure_ascii=False).replace("</", "<\\/"))
t = t.replace("watt-validacion-v", "watt-facturas-v")
open(os.path.join(ROOT, "reports", "facturas-remitentes.html"), "w", encoding="utf-8").write(t)
print("ok", len(CASOS))
