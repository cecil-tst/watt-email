# STATUS · WATT – Email

- **Fase:** 2 — organizar (cambio hecho el 2026-11-12 a petición de Cecil). Aún no se ha escrito nada en el buzón.
- **Última actualización:** 2026-11-12
- **Hecho:** inventario 90 d (`reports/inventario.md`); barrido de recurrencias 13 m por remitentes (`reports/recurrencias-13m.md`, ~30 consultas con solo IDs); 35 casos en `proposals/2026-11-10-validacion.json` + ficha interactiva `reports/validacion.html` (publicada como artefacto).
- **Decisiones recibidas (2026-11-12):** 35 casos volcados en `rules/categories.yaml` v1 (31 reglas, 15 categorías incl. `administracion-publica`, mapeo de etiquetas). Sigue siendo fase 1: nada se ejecuta.
- **Hallazgo:** el barrido completo de 12 m no es viable por el conector (50 hilos ≈ 18k tokens; >100 páginas). Se hizo por remitentes: PayPal, Open Arms, BBVA, Workspace y gencat/csuc solo recogen la primera página (≥50). Las recurrencias salen mensuales; no apareció ninguna anual clara (los avisos de dominios van por dominio y hay pocos hilos de 1/año).
- **Aviso de seguridad:** el hilo `1a0f…8834` (hosting UB) trae contraseña en claro. Rotarla si se reutilizó. No se ha abierto.
- **Resuelto 2026-11-12:** excepción de la regla 3 (reenviar solo facturas al buzón Holded, fase 4, lista aprobada); dirección de Holded guardada en `rules/categories.yaml`; c04 aprobado; CLAUDE.md en fase 2.
- **Pendientes:** (1) f04 (xdesign.barcelona) sin decidir; f01-f03, f05, f06 = proveedores. Reenvío a Holded: SaaS desde 2026-07-01, proveedores solo posteriores a 2026-11-01 (confirmar). (2) Instrucciones para conectar Google Calendar (regla c25), a dar al arrancar la ejecución.
- **Lote 1 propuesto (sin ejecutar):** `proposals/2026-11-12-lote1.md`, 36 hilos de la bandeja (c22-c24). Espera tu «apruebo …».
- **Próximo paso:** primer lote de fase 2: proponer lista (IDs cortos + acción) sobre los hilos de la bandeja y esperar «apruebo …». Log en `logs/`.
- **Nota técnica:** `data/` borrado (regla 6). `python3 scripts/inventario.py --barrido` y `python3 scripts/build_validacion.py` regeneran los informes; ver cabeceras.
