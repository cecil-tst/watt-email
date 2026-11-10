# WATT – Email · Guía de setup

Flujo: **sesiones de Claude Code en la nube → GitHub (`main`) → clon local de solo consulta.**
Todo lo que hagas desde web, móvil o escritorio en sesiones cloud sobre el repo acaba en GitHub.

---

## Paso 1 · Crear el repositorio en GitHub
1. github.com → **New repository** → nombre `watt-email`, **Private**, con README.
2. Sube `CLAUDE.md` y este `SETUP.md` a la raíz (Add file → Upload files → Commit).

## Paso 2 · Dar acceso a la Claude GitHub App (solo a este repo)
1. github.com → Settings → Applications → **Installed GitHub Apps** → Claude → **Configure**.
2. En *Repository access*: mantener **Only select repositories** y añadir `watt-email`.
   (No usar "All repositories".)

## Paso 3 · Conectar Gmail (OAuth)
1. claude.ai → Ajustes → **Conectores** → Gmail → conectar con **cecil@the-storytellers.es**.
2. Revisar los permisos que pide antes de aceptar.
3. (Más adelante, tras la auditoría de apps conectadas en GWS) marcar la app de Claude como *De confianza*
   en Admin console → Seguridad → Acceso y control de datos → Controles de API.

## Paso 4 · Crear la sección y la sesión principal en la nube
(Sin la beta de Projects. Cuando llegue, se migra: el estado ya vive en el repo.)
1. Pestaña **Code** → en la barra lateral, filtro de secciones → **Nueva sección** → `WATT – Email`.
2. **Nuevo** → selector de entorno: **cloud** (no local) → repo `cecil-tst/watt-email` → rama `main`.
3. Modelo: Opus 5.5 o Sonnet (no Fable: consume cuota más rápido).
4. Modo de permisos: **Auto** vale para fase 1 (solo lectura). **Desde fase 2, cambiar a modo "preguntar"**
   para que cada escritura en el buzón requiera tu aprobación.
5. Renombra la sesión como `WATT – Email · principal` y muévela a la sección.
6. Ejecutar `/mcp` → comprobar que **Gmail** aparece y está conectado. Si no, parar y revisar el Paso 3.
7. Cada tarea larga o fase nueva = sesión nueva en la misma sección, que arranca leyendo CLAUDE.md y STATUS.md.

## Paso 5 · Prompt 0 — Arranque (sin acceso al buzón)
```
Lee CLAUDE.md. Crea la estructura de carpetas, .gitignore (data/), STATUS.md y
rules/categories.yaml con las categorías de partida. Commit y push a main.
Resúmeme en 5 líneas las reglas de fase 1. No accedas al buzón.
```

## Paso 6 · Clon local con actualización automática (una sola vez)
Abre en la app de escritorio una sesión **local** de Code (no del Proyecto) en tu carpeta de usuario y pega:
```
Quiero un clon local de solo consulta del repo privado github.com/<mi-usuario>/watt-email.
1. Comprueba si tengo git y acceso a GitHub (gh auth status o SSH). Si no, guíame para autenticarme;
   no guardes tokens en ficheros de texto.
2. Clónalo en ~/watt-email.
3. Programa una actualización automática cada 15 minutos con `git -C ~/watt-email pull --ff-only --quiet`
   usando el mecanismo nativo de mi sistema operativo (launchd en macOS, Programador de tareas en Windows,
   cron en Linux). Que se ejecute también al iniciar sesión.
4. Ejecútalo una vez, enséñame el resultado y explícame cómo desactivarlo.
No modifiques nada dentro del repo.
```
> El Proyecto en la nube no puede escribir en tu ordenador: es tu ordenador quien se trae los cambios
> de GitHub cada vez que está encendido.

## Paso 7 · Activar /advisor (antes de leer el buzón)
En la sesión principal:
1. Seleccionar **Sonnet** como modelo.
2. Escribir `/advisor` → elegir **Opus**.
3. En la siguiente sesión cloud que abras, comprobar que sigue activo; si no, activarlo ahí.
> Si en fases 2–3 (escritura) ves decisiones flojas, usa Opus directamente.

## Paso 8 · Prompt 1 — Inventario (solo lectura, con script)
```
Fase 1, solo lectura. Escribe un script en scripts/ que, vía el conector de Gmail, extraiga
solo metadatos de los últimos 90 días de la bandeja de entrada a data/ y genere
reports/inventario.md: volumen, top 40 remitentes y dominios, % con adjuntos, recurrencias
y categoría tentativa por remitente, marcando los "dudosos". No abras hilos.
Actualiza STATUS.md, commit y push.
```

## Paso 9 · Subagente revisor de solo lectura
```
Crea un subagente en .claude/agents/revisor-email.md: rol "revisor de solo lectura del buzón WATT",
con acceso exclusivamente a las herramientas de lectura/búsqueda del conector de Gmail y a
lectura/escritura de ficheros en proposals/ y reports/. Lista las herramientas que le asignas y las
que excluyes, y espera mi OK antes de hacer commit.
```

## Paso 10 · Prompt 2 — Revisión de dudosos
```
Revisa los "dudosos" de reports/inventario.md usando el subagente revisor-email.
Si son pocos, hazlo en esta sesión. Solo si el volumen justifica paralelizar, propónme
cuántos hilos abrir y por qué, y espera mi OK. Resultado: proposals/<fecha>-dudosos.md
con tabla numerada (remitente, categoría, acción fase 2, acción fase 4), legible en móvil.
```

## Paso 11 · Prompt 3 — Consolidar reglas
```
Aplica mis aprobaciones a rules/categories.yaml, indica qué categorías convertir en filtros
nativos de Gmail en fase 2, actualiza STATUS.md, commit y push.
```

---

## Cambio de fase
Editar la línea **"Fase actual"** de `CLAUDE.md` (en GitHub o pidiéndoselo a la sesión principal) y hacer commit.
Claude no pasa a escribir en el buzón hasta que esa línea cambie.

## Recordatorios
- Aprobar desde el móvil: "apruebo 1-4 y 7".
- Copia local = solo consulta. Si editas en local, push inmediato.
- `/compact` si el contexto de la sesión se llena; `/doctor` de vez en cuando para revisar configuración.
