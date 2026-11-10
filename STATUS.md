# STATUS · WATT – Email

- **Fase:** 1 — solo lectura. Nada escrito en el buzón.
- **Última actualización:** 2026-11-10
- **Hecho:** estructura del repo; inventario de 90 días (355 hilos) en `reports/inventario.md`, generado por `scripts/inventario.py`.
- **Por validar:** categorías tentativas (83 % de hilos con propuesta; 41 remitentes dudosos o mixtos); si «administración pública» (AEAT/CSUC/Generalitat) merece categoría propia; reglas por asunto para remitentes mixtos (OpenAI, DreamHost, Holded, WordPress).
- **Aviso de seguridad:** el hilo `1a0f6dbb76348834` (hosting web UB, 1-oct) trae una contraseña en claro. Rotarla.
- **Próximo paso:** Prompt 2 (revisión de dudosos). Son pocos: se hace en una sesión, sin hilos hijos. Pendiente tu OK si quieres un barrido de 12 meses de metadatos para detectar lo anual.
- **Nota técnica:** `data/` se ha borrado (regla 6). Regenerar el informe exige repetir la extracción por el conector (~8 páginas de `search_threads`); ver cabecera del script.
- **Datos que cambian lo planificado:** `rules/categories.yaml` sigue sin reglas; el buzón ya usa etiquetas propias (TST/HOLA, TFT, TFT/Hola, Facturas, __POR PAGAR…): respetarlas en la fase 2.
