# Cola de órdenes para la FASE 4 (guardadas en fase 2; NO ejecutar hasta abrir la sesión «WATT - fase 4»)

Origen: orden de Cecil del 2026-11-12. Este fichero no autoriza nada por sí mismo: en fase 4 hay que mostrar la lista y esperar «apruebo …» (regla 2).
Contenido: solo IDs, remitente y asunto (sin cuerpos).

## Orden 1 · Reenviar facturas/recibos SaaS a Holded
- Destino único: `parametros.holded_inbox` de `rules/categories.yaml` (herramienta `forward`, excepción de la regla 3, solo fase 4).
- Filtro de fecha: facturas-saas recibidas el 2026-07-01 o después (`parametros.reenvio_holded`).
- Éxito = tiene PDF de factura/recibo y se reenvía bien → registrar en `logs/` (`action: forward`) y **archivar** el hilo.
- Fallo (sin factura/recibo, no se puede reenviar) → etiqueta **`WATT/revisar`** (se crea en la sesión de fase 2 al aprobar el lote 3) y dejar en bandeja.
- Remitentes citados por Cecil: Anthropic, OpenAI, Google Payments, Dropbox. DreamHost: solo etiquetar y archivar, NO se reenvía.

| # | hilo | remitente | asunto | nota |
|---|---|---|---|---|
| 1 | 1a1c3c558c8a1aa4 | Anthropic Ireland (Stripe) | Receipt #2034-5828-2941 (2026-11-10) | trae Invoice PDF + Receipt PDF |
| 2 | 1a16d704c945d1f6 | Anthropic Ireland (Stripe) | Receipt #2916-4307 (2026-10-24) | por comprobar adjuntos |
| 3 | 1a1692cce603bf7d | Anthropic Ireland (Stripe) | Receipt #2097-8143 (2026-10-23) | por comprobar adjuntos |
| 4 | 1a163afbfd58b5fc | Anthropic Ireland (Stripe) | Receipt #2493-8756 (2026-10-22) | por comprobar adjuntos |
| 5 | 1a17a3baf05b519e | Anthropic Ireland (Stripe) | Refund #3286-1830 (2026-10-26) | REEMBOLSO: preguntar a Cecil si va a Holded (¿abono?) |
| 6 | 1a17a3b4a214c857 | Anthropic Ireland (Stripe) | Refund #3934-9886 (2026-10-26) | REEMBOLSO: ídem |
| 7 | 1a15e5c470aa11b0 | Dropbox (no-reply@txn.dropbox.com) | Renovación plan Dropbox Standard, 58,00 € (2026-10-21) | SIN PDF: «este correo vale como recibo»; probable `WATT/revisar` |
| 8 | 1a198c1d00cfea66 | Google Payments | Factura Google Workspace (2026-11-01) | dice PDF adjunto; sin verificar |
| 9 | 1a0fa007176fdc5a | Google Payments | Factura Google Workspace (2026-10-02) | dice PDF adjunto; sin verificar |
| 10 | 1a1c063593be2549 | OpenAI | Crédito del workspace recargado, 10,89 $ (2026-11-09) | comprobar si trae factura |
| 11 | 1a1c06353d1a4588 | OpenAI | Auto-recarga activada (2026-11-09) | probablemente no es factura → `WATT/revisar` o descartar |

Estos 11 hilos se etiquetan en fase 2 (lote 3) y **quedan en la bandeja** hasta que la fase 4 los archive.

## Pendientes de ampliar la cola (se añadirán desde fase 2)
- Recibos SaaS posteriores al 2026-07-01 de Anthropic/OpenAI/Google/Dropbox que no estaban en la primera página de la consulta (lote 4).
- Facturas de proveedores recibidas después del 2026-11-01 (hasta hoy, ninguna: las de Holded/WELOFT son anteriores).

## Arranque de la sesión de fase 4
1. Integrar antes en `main` el PR de la fase 2 (este fichero llega con él) y arrancar la fase 4 desde `main`, rama `claude/watt-fase-4`.
2. Prompt: `/advisor opus` + «Sesión WATT - fase 4. Lee CLAUDE.md, STATUS.md, rules/categories.yaml y proposals/fase4-cola.md. Comprueba adjuntos de cada hilo de la cola, muéstrame la lista (ID corto + remitente + asunto + adjunto sí/no) y espera mi «apruebo …». Después reenvía solo a holded_inbox, registra cada forward y archiva los éxitos; los fallos van a WATT/revisar.»
3. Cecil autoriza expresamente, para esa sesión, archivar los hilos reenviados con éxito.
