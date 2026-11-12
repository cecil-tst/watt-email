# Cola de órdenes para la FASE 4 (guardadas en fase 2; NO ejecutar hasta abrir la sesión «WATT - fase 4»)

Origen: orden de Cecil del 2026-11-12. Este fichero no autoriza nada por sí mismo: en fase 4 hay que mostrar la lista y esperar «apruebo …» (regla 2).
Contenido: solo IDs, remitente y asunto (sin cuerpos).

## Orden 1 · Reenviar facturas/recibos SaaS a Holded
- Destino único: `parametros.holded_inbox` de `rules/categories.yaml` (herramienta `forward`, excepción de la regla 3, solo fase 4).
- Filtro de fecha: facturas-saas recibidas el 2026-07-01 o después (`parametros.reenvio_holded`).
- Éxito = tiene PDF de factura/recibo y se reenvía bien → registrar en `logs/` (`action: forward`) y **archivar** el hilo.
- Fallo (sin factura/recibo, no se puede reenviar) → etiqueta **`WATT/revisar`** (creada en fase 2, 2026-11-12) y dejar en bandeja.
- Remitentes citados por Cecil: Anthropic, OpenAI, Google Payments, Dropbox; solo con PDF adjunto (sin PDF: etiquetar y archivar, ya hecho). DreamHost: NO se reenvía.

| # | hilo | remitente | asunto | adjuntos (verificado 2026-11-12) |
|---|---|---|---|---|
| 1 | 1a1c3c558c8a1aa4 | Anthropic Ireland (Stripe) | Receipt #2034-5828-2941 (2026-11-10) | Invoice PDF + Receipt PDF |
| 2 | 1a16d704c945d1f6 | Anthropic Ireland (Stripe) | Receipt #2916-4307 (2026-10-24) | Invoice PDF + Receipt PDF |
| 3 | 1a1692cce603bf7d | Anthropic Ireland (Stripe) | Receipt #2097-8143 (2026-10-23) | Invoice PDF + Receipt PDF |
| 4 | 1a163afbfd58b5fc | Anthropic Ireland (Stripe) | Receipt #2493-8756 (2026-10-22) | Invoice PDF + Receipt PDF |
| 5 | 1a17a3baf05b519e | Anthropic Ireland (Stripe) | Refund #3286-1830 (2026-10-26) | Invoice PDF + Refund PDF (reembolso, Cecil: a la lista) |
| 6 | 1a17a3b4a214c857 | Anthropic Ireland (Stripe) | Refund #3934-9886 (2026-10-26) | Invoice PDF + Refund PDF (reembolso, Cecil: a la lista) |
| 7 | 1a198c1d00cfea66 | Google Payments | Factura Google Workspace nº 5726006294 (2026-11-01) | PDF adjunto |
| 8 | 1a0fa007176fdc5a | Google Payments | Factura Google Workspace nº 5700738508 (2026-10-02) | PDF adjunto |

Estos 8 hilos están etiquetados `WATT/facturas-saas` + `Facturas` y siguen en la bandeja hasta que la fase 4 los reenvíe y archive.
Decisión de Cecil (2026-11-12): los de Dropbox y OpenAI SIN PDF adjunto, y todos los de DreamHost, ya se etiquetaron y archivaron en fase 2 (no se reenvían). Sus facturas solo existen como enlace/panel (OpenAI RKGIXTU7-0005, Dropbox B59NY9N6CD4L): si Cecil las quiere en Holded, habrá que descargarlas a mano.


## Orden 2 · Bajas de listas (unsubscribe), orden de Cecil 2026-11-12
- Siempre con confirmación individual (regla 4): mostrar remitente, frecuencia y método de baja y esperar «apruebo» por cada uno. No se da de baja nada en fase 2.
| # | remitente | dato | método propuesto |
|---|---|---|---|
| B1 | BBVA promociones (bbva@comunica.bbva.com) | boletines/ofertas; 5 hilos ya archivados con `WATT/ofertas-comerciales` (ids 1a1c62f2ffd843b6 1a186df4648e869a 1a11bb9a29085d5e 1a11181aa44e99af 19d96ddede093c7c) | enlace de baja del correo o preferencias en BBVA (Cecil) |
| B2 | Canva (start@engage.canva.com) | boletín semanal; hilos 16a3471aa1bfcd2e 1691439b518ec749 (2019, etiquetados `WATT/newsletters` y archivados) | enlace de baja del correo (Cecil) |
También pendientes de decisión de baja (regla c19): IA Hub, Atlassian marketing, WPVibe, SiteGround Web Hosting, Emexs, OpenAI Ads, Claude Team.

## Pendientes de ampliar la cola (se añadirán desde fase 2)
- Recibos SaaS posteriores al 2026-07-01 de Anthropic/OpenAI/Google/Dropbox que no estaban en la primera página de la consulta (lote 4).
- Facturas de proveedores recibidas después del 2026-11-01 (hasta hoy, ninguna: las de Holded/WELOFT son anteriores).

## Arranque de la sesión de fase 4
1. Integrar antes en `main` el PR de la fase 2 (este fichero llega con él) y arrancar la fase 4 desde `main`, rama `claude/watt-fase-4`.
2. Prompt: `/advisor opus` + «Sesión WATT - fase 4. Lee CLAUDE.md, STATUS.md, rules/categories.yaml y proposals/fase4-cola.md. Comprueba adjuntos de cada hilo de la cola, muéstrame la lista (ID corto + remitente + asunto + adjunto sí/no) y espera mi «apruebo …». Después reenvía solo a holded_inbox, registra cada forward y archiva los éxitos; los fallos van a WATT/revisar.»
3. Cecil autoriza expresamente, para esa sesión, archivar los hilos reenviados con éxito. Regla permanente de Cecil: todo hilo archivado queda también como LEÍDO (quitar INBOX y UNREAD).
