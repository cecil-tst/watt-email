# WATT – Email · Instrucciones para Claude

## Propósito
Clasificar y gestionar el buzón **cecil@the-storytellers.es** (Google Workspace de WE ARE THE TELLERS SL),
en cuatro fases: 1) clasificar, 2) organizar (etiquetas, archivo, snooze), 3) responder, 4) ejecutar acciones
(adjuntos a Drive / Dropbox / Holded).

Cecil gestiona en WATT: finanzas, documentación, facturación y pagos, bancos, impuestos, renovación de
suscripciones y cuentas de usuario en plataformas digitales.

## Alcance
- Solo este buzón. Nunca otros buzones (Gmail personal, Hotmail) aunque estén accesibles.
- Idioma de trabajo: español. Respuestas de email: formales y concisas, firmadas como Cecil Servan.

## Fase actual
**FASE 2 — organizar** (cambio de fase pedido por Cecil el 2026-11-12; Cecil actualiza esta línea al cambiar de fase).
- Permitido, solo con aprobación explícita de una lista concreta (regla 2) y registro en el log: crear etiquetas
  (`WATT/<categoría>`, `Sensible`, `Snooze/AAAA-MM-DD`), etiquetar, archivar, pseudo-snooze y devolver hilos a la bandeja.
  Las reglas aprobadas están en `rules/categories.yaml` (v1); no se inventan reglas nuevas.
- Sigue prohibido: borrar, vaciar papelera, marcar spam, darse de baja de listas, crear filtros, crear borradores
  (fase 3), enviar o reenviar (excepción de la regla 3) y mover adjuntos a Drive/Dropbox/Holded (fase 4).
- Antes de ejecutar un lote: mostrar la lista (IDs cortos + acción) y esperar «apruebo …».
- Modo de permisos de la sesión principal: «Accept edits» (no Auto), para que cada llamada de escritura al buzón pida confirmación.
- Pendiente de esta fase: dar a Cecil instrucciones para conectar Google Calendar (avisos de caducidad, regla c25).

## Reglas de operación
0. **Economía de uso (plan Pro):** el trabajo pesado y repetible (recuentos, agrupaciones por remitente/dominio,
   detección de recurrencias, listados de adjuntos) se hace con scripts en `scripts/`, no leyendo emails uno a uno.
   El modelo solo lee lo ambiguo. **Hilos/sesiones hijas solo cuando sea estrictamente necesario**: trabajo
   realmente paralelizable que exija leer muchos cuerpos de email. Antes de abrir hilos, indicar cuántos y por qué,
   y esperar el OK de Cecil.
1. **Sesiones hijas (nested) y laterales:** solo leen y proponen. Nunca escriben en el buzón ni en servicios externos.
2. **Sesión principal:** es la única que ejecuta acciones de escritura, y solo tras aprobación explícita de Cecil
   sobre una lista concreta (IDs de mensaje + acción). "Parece bien" sobre un resumen no es aprobación de ejecución.
3. **Nunca enviar emails.** En fase 3 solo se crean borradores; Cecil los revisa y envía.
   **Única excepción (autorizada por Cecil el 2026-11-12):** *reenviar* (herramienta `forward`) mensajes que traigan
   adjunto de factura/recibo al buzón de ingesta de Holded, `parametros.holded_inbox` en `rules/categories.yaml`.
   Solo en fase 4, solo tras aprobación de una lista concreta de IDs (regla 2), a ese único destinatario, y cada
   reenvío se registra en el log (`action: forward`). Ningún otro destinatario ni tipo de envío.
   Filtro por fecha de recepción (`parametros.reenvio_holded`): SaaS desde el 2026-07-01; proveedores solo posteriores al 2026-11-01.
4. **Nada irreversible** (borrar, vaciar papelera, darse de baja de listas, pagar) sin confirmación individual.
5. **Mínimo contenido:** para clasificar, usar remitente, dominio, asunto, fecha, etiquetas y fragmento.
   Leer el cuerpo completo solo cuando sea necesario para decidir.
6. **Privacidad:** no guardar cuerpos de email ni adjuntos en el repositorio. Los datos temporales van en `data/`
   (excluido de git) y se borran al cerrar cada tarea.
7. Ante la duda sobre una categoría o acción, preguntar; no inventar reglas.

## Log de acciones (obligatorio)
Cada acción de escritura se registra en `logs/<AAAA-MM-DD>-<sesion>.jsonl` (un fichero por sesión y día,
para evitar conflictos de merge entre hilos), una línea por acción:
```json
{"ts":"2026-11-10T09:12:00+01:00","session":"main|<nombre-sesion-hija>","phase":2,"message_id":"...","from":"...","subject":"...","action":"label|archive|snooze|draft|upload|...","detail":"...","approved_by":"Cecil","result":"ok|error"}
```
Las propuestas de sesiones hijas se guardan en `proposals/<fecha>-<categoria>.md` indicando qué sesión las generó.

## Estructura del repositorio
```
rules/categories.yaml   # taxonomía y acción por categoría (fuente de verdad, la valida Cecil)
proposals/              # propuestas de clasificación/acción pendientes de validar
reports/                # informes de inventario y resúmenes
logs/                   # registro de acciones ejecutadas (un .jsonl por sesión y día)
STATUS.md               # estado actual en 10 líneas: fase, pendientes de validar, próximos pasos
scripts/                # utilidades (si se necesitan)
data/                   # temporal, en .gitignore
```

## Categorías de partida (a validar en fase 1)
spam · newsletters · info de mantenimiento/servicio · conversaciones personales/profesionales ·
ofertas comerciales de servicios · alertas (seguridad, banco, plataformas) · recordatorios de suscripción/renovación ·
pagos y cobros · facturas de proveedores · facturas de software/SaaS · bancos · impuestos/AEAT/gestoría ·
gestión de cuentas de usuario · otros

## Subagente y tareas programadas
- La revisión de buzón en hilos se delega en el subagente `.claude/agents/revisor-email.md`, que solo tiene
  herramientas de lectura del conector de Gmail y escritura en `proposals/` y `reports/`.
  No modificar su lista de herramientas sin aprobación de Cecil.
- Las tareas programadas (triaje diario, devolución de pseudo-snooze) son de solo lectura o ejecutan únicamente
  acciones pre-aprobadas en `rules/categories.yaml`, y dejan resumen en `reports/` + log.

## Snooze (decisión tomada)
Se usa **pseudo-snooze**: etiqueta `Snooze/AAAA-MM-DD` + archivar; una tarea programada diaria devuelve a la
bandeja los hilos cuya fecha ha llegado y quita la etiqueta. Cada devolución se registra en el log.
No usar el snooze nativo de Gmail.

## Trabajo en remoto y multi-dispositivo
Este proyecto se gestiona desde escritorio, web (claude.ai/code) y móvil, sobre sesiones en la nube.
- **El repositorio es la única fuente de estado.** No depender de rutas locales ni de memoria de una sesión concreta.
- Al terminar cada tarea: actualizar `STATUS.md`, hacer commit con mensaje descriptivo y push.
- Si una sesión trabaja en rama propia, la sesión principal integra en `main` solo lo validado por Cecil.
- Escribir resúmenes y tablas de validación legibles en móvil: breves, máximo ~10 filas por bloque,
  con IDs cortos para aprobar por número (p. ej. "apruebo 1-4 y 7").
- Existe un clon local de solo consulta que se actualiza con `git pull --ff-only`. Nunca asumir que hay
  cambios locales pendientes; GitHub (`main`) es la fuente de verdad.
- **Nunca** guardar credenciales, tokens ni contraseñas en el repositorio (la dirección de ingesta de Holded no es una credencial y Cecil autorizó guardarla en `rules/categories.yaml`). El acceso a Gmail es por el conector
  (OAuth); cualquier otra credencial futura (Holded, Dropbox) va en las variables del entorno cloud.
