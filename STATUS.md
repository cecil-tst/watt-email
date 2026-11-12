# STATUS · WATT – Email

- **Fase:** 1 — solo lectura. Nada escrito en el buzón ni en `rules/categories.yaml`.
- **Última actualización:** 2026-11-10
- **Hecho:** inventario 90 d (`reports/inventario.md`); barrido de recurrencias 13 m por remitentes (`reports/recurrencias-13m.md`, ~30 consultas con solo IDs); 35 casos en `proposals/2026-11-10-validacion.json` + ficha interactiva `reports/validacion.html` (publicada como artefacto).
- **Decisiones recibidas (2026-11-12):** 35 casos volcados en `rules/categories.yaml` v1 (31 reglas, 15 categorías incl. `administracion-publica`, mapeo de etiquetas). Sigue siendo fase 1: nada se ejecuta.
- **Hallazgo:** el barrido completo de 12 m no es viable por el conector (50 hilos ≈ 18k tokens; >100 páginas). Se hizo por remitentes: PayPal, Open Arms, BBVA, Workspace y gencat/csuc solo recogen la primera página (≥50). Las recurrencias salen mensuales; no apareció ninguna anual clara (los avisos de dominios van por dominio y hay pocos hilos de 1/año).
- **Aviso de seguridad:** el hilo `1a0f…8834` (hosting UB) trae contraseña en claro. Rotarla si se reutilizó. No se ha abierto.
- **Pendientes que necesitan tu decisión:** (1) c26-c29 fase 4 pide reenviar por correo al buzón Holded y la regla 3 prohíbe enviar emails: ¿excepción solo para ese reenvío, o descargar a Drive? (2) c25 Calendar: no hay conector de Calendar; de momento pseudo-snooze. (3) c04 archiva avisos IMPORTANT de CSUC: revisar a los 30 días. (4) La dirección de Holded va en la variable de entorno `HOLDED_INBOX_EMAIL`, no en el repo.
- **Próximo paso:** resueltos esos puntos, tú cambias la línea de fase en CLAUDE.md a fase 2 (modo «preguntar»).
- **Nota técnica:** `data/` borrado (regla 6). `python3 scripts/inventario.py --barrido` y `python3 scripts/build_validacion.py` regeneran los informes; ver cabeceras.
