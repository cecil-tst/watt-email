# Barrido de recurrencias · ventana de 13 meses (solo IDs de hilo)

- Generado: 2026-11-10 · `python3 scripts/inventario.py --barrido`. Fechas decodificadas del ID del hilo (inicio del hilo).
- Ventana de **13 meses** (oct-2025 a nov-2026 = 14 meses naturales) a propósito: en 12 una renovación anual aparece una sola vez.
- **Límite:** no es un barrido completo del buzón (5.975 hilos en bandeja, más archivados): son consultas por remitente/patrón. Las consultas con muchos resultados (PayPal, Open Arms, BBVA, Workspace) solo recogen la primera página (50 hilos más recientes).

| Fichero | Hilos | Meses activos | Tipo | Primer → último |
|---|---|---|---|---|
| admin_pub | 50 | 11/14 | mensual | 2025-10-22 → 2026-11-04 |
| aeat | 31 | 13/14 | mensual | 2025-10-13 → 2026-11-10 |
| bbva | 50 | 12/14 | mensual | 2025-12-17 → 2026-11-10 |
| cdmon | 50 | 12/14 | mensual | 2025-10-17 → 2026-11-09 |
| cve | 42 | 12/14 | mensual | 2025-10-08 → 2026-11-10 |
| dreamhost | 66 | 14/14 | mensual | 2025-10-13 → 2026-11-06 |
| dropbox | 13 | 13/14 | mensual | 2025-10-21 → 2026-10-21 |
| googlepay | 16 | 13/14 | mensual | 2025-11-02 → 2026-11-01 |
| holded | 33 | 13/14 | mensual | 2025-11-07 → 2026-11-04 |
| openai_tm | 14 | 3/14 | irregular (racimos) | 2026-09-30 → 2026-11-10 |
| openarms | 50 | 12/14 | mensual | 2025-12-30 → 2026-11-05 |
| paypal | 50 | 12/14 | mensual | 2025-11-15 → 2026-10-28 |
| rafa_growth | 18 | 10/14 | mensual | 2025-10-28 → 2026-10-30 |
| saas_fact | 40 | 14/14 | mensual | 2025-10-26 → 2026-11-03 |
| siteground_renov | 15 | 13/14 | mensual | 2025-10-17 → 2026-10-17 |
| stripe | 6 | 2/14 | irregular (racimos) | 2026-10-22 → 2026-11-10 |
| workspace | 50 | 12/14 | mensual | 2025-11-16 → 2026-11-02 |
