# STATUS · WATT – Email

- **Fase:** 2 — organizar (rama `claude/watt-fase-2`, sesión «WATT - fase 2»). Fase 1 cerrada e integrada en `main`. Nada escrito en el buzón todavía.
- **Última actualización:** 2026-11-12
- **Hecho:** inventario 90 d (`reports/inventario.md`); barrido de recurrencias 13 m por remitentes (`reports/recurrencias-13m.md`, ~30 consultas con solo IDs); 35 casos en `proposals/2026-11-10-validacion.json` + ficha interactiva `reports/validacion.html` (publicada como artefacto).
- **Decisiones recibidas (2026-11-12):** 35 casos volcados en `rules/categories.yaml` v1 (31 reglas, 15 categorías incl. `administracion-publica`, mapeo de etiquetas). Sigue siendo fase 1: nada se ejecuta.
- **Hallazgo:** el barrido completo de 12 m no es viable por el conector (50 hilos ≈ 18k tokens; >100 páginas). Se hizo por remitentes: PayPal, Open Arms, BBVA, Workspace y gencat/csuc solo recogen la primera página (≥50). Las recurrencias salen mensuales; no apareció ninguna anual clara (los avisos de dominios van por dominio y hay pocos hilos de 1/año).
- **Aviso de seguridad:** el hilo `1a0f…8834` (hosting UB) trae contraseña en claro. Rotarla si se reutilizó. No se ha abierto.
- **Resuelto 2026-11-12:** excepción de la regla 3 (reenviar solo facturas al buzón Holded, fase 4, lista aprobada); dirección de Holded guardada en `rules/categories.yaml`; c04 aprobado; filtro de fechas de reenvío fijado.
- **Pendientes:** (1) f04 (xdesign.barcelona) sin decidir; f01-f03, f05, f06 = proveedores. Reenvío a Holded: SaaS desde 2026-07-01, proveedores solo posteriores a 2026-11-01 (confirmar). (2) Instrucciones para conectar Google Calendar (regla c25), a dar al arrancar la ejecución.
- **Lote 1 (aprobado «apruebo 1-36», NO ejecutado):** `proposals/2026-11-12-lote1.md`, 36 hilos (c22-c24). Bloqueado: el conector Gmail no tiene permiso para crear etiquetas (`create_label` falla; ver `logs/2026-11-12-main.jsonl`). Sin etiquetas WATT no se etiqueta ni archiva nada. Cecil debe reconectar Gmail con todos los permisos en https://claude.ai/customize/connectors y abrir sesión nueva; la aprobación 1-36 sigue vigente en esa sesión solo si Cecil la repite.
- **Próximo paso:** en esta sesión, ejecutar el lote 1 tras tu aprobación; pendientes: f04, Calendar (c25), confirmar filtro de fechas de proveedores.
- **Nota técnica:** `data/` borrado (regla 6). `python3 scripts/inventario.py --barrido` y `python3 scripts/build_validacion.py` regeneran los informes; ver cabeceras.
