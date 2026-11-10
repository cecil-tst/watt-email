# Inventario del buzón · fase 1 (solo lectura)

- Generado: 2026-11-10 · script `scripts/inventario.py` · propuesta, no validada por Cecil.
- Consulta: `in:inbox newer_than:90d` (desde 2026-08-12). Hilos con mensajes en la ventana: 2026-08-27 → 2026-11-10.
- **Unidad: hilos**, fechados por su último mensaje (zona Europe/Madrid). Los mensajes son una cifra aproximada (suma de `messageCount`).
- Solo metadatos: remitente, asunto, fecha, etiquetas. Sin cuerpos. Asuntos truncados y con dígitos largos enmascarados.
- Las categorías son una **propuesta** del script; `rules/categories.yaml` no se ha tocado.

## 1. Volumen

| Dato | Valor |
|---|---|
| Hilos en la bandeja (90 d) | 355 |
| Mensajes (aprox.) | 419 |
| Hilos sin leer | 296 (83 %) |
| Hilos donde el último mensaje es tuyo (SENT) | 7 |
| Media por semana | 30 hilos |

**Por pestaña de Gmail**

| Pestaña | Hilos | % |
|---|---|---|
| Forums | 131 | 37 % |
| Updates | 128 | 36 % |
| Personal | 49 | 14 % |
| Promotions | 40 | 11 % |
| (sin pestaña) | 7 | 2 % |

**Por semana 1-10 (lunes de inicio)**

| # | Semana | Hilos | Msgs |
|---|---|---|---|
| 1 | 24/08 (S35) | 1 | 3 |
| 2 | 31/08 (S36) | 9 | 9 |
| 3 | 07/09 (S37) | 2 | 2 |
| 4 | 14/09 (S38) | 4 | 4 |
| 5 | 21/09 (S39) | 4 | 11 |
| 6 | 28/09 (S40) | 26 | 34 |
| 7 | 05/10 (S41) | 33 | 37 |
| 8 | 12/10 (S42) | 58 | 66 |
| 9 | 19/10 (S43) | 55 | 75 |
| 10 | 26/10 (S44) | 70 | 76 |

**Por semana 11-12 (lunes de inicio)**

| # | Semana | Hilos | Msgs |
|---|---|---|---|
| 11 | 02/11 (S45) | 64 | 68 |
| 12 | 09/11 (S46) | 29 | 34 |

_Ojo: antes del 28/09 casi no hay hilos porque la bandeja solo guarda lo no archivado; no es el volumen real que llegó._
_Comprobación: las semanas suman 355 = total 355._

## 2. Top 40 remitentes

«[vía grupo]» = el remitente real va detrás de un alias de grupo (hola@, ai@, dev@, admin@…). «→ x» = hilo cuyo último mensaje es de Cecil o de un compañero, contado por su interlocutor. Cat. = propuesta; «?» = dudoso; «mixto» = varía según el asunto.

**Remitentes 1-10**

| # | Remitente | Hilos | Cat. |
|---|---|---|---|
| 1 | IA Hub Barcelona (contact@iahub.space) | 15 | newsletters |
| 2 | Atlassian (info@e.atlassian.com) | 13 | newsletters |
| 3 | OpenAI (noreply@tm.openai.com) | 12 | mixto |
| 4 | John Turner [vía grupo] | 10 | newsletters |
| 5 | agenciatributaria@correo.aeat.es | 10 | impuestos |
| 6 | Informes DMARC (thefoodtellers.com) | 9 | info-servicio |
| 7 | Nuria García (nuriagarcia@cve-advocats.com) | 9 | impuestos |
| 8 | The Google Workspace Team (workspace-noreply@google… | 9 | info-servicio |
| 9 | cdmon (no-reply@cdmon.com) | 9 | recordatorios-suscripcion |
| 10 | DreamHost Registration Service (support@dreamhost.c… | 8 | mixto |

**Remitentes 11-20**

| # | Remitente | Hilos | Cat. |
|---|---|---|---|
| 11 | SiteGround Web Hosting [vía grupo] | 8 | newsletters |
| 12 | Emexs Marketing (marketing@emexs.es) | 7 | newsletters |
| 13 | Holded (no-reply@send.holded.com) | 7 | mixto |
| 14 | WordPress (wordpress@thefoodtellers.com) | 7 | mixto |
| 15 | Anthropic Ireland, Limited (invoice+statements+acct… | 6 | facturas-saas |
| 16 | ChatGPT (noreply@email.openai.com) | 6 | newsletters |
| 17 | WordPress (no-reply@the-storytellers.es) | 6 | ? |
| 18 | Atlassian (noreply@po.atlassian.net) | 5 | newsletters |
| 19 | El equipo de Holded [vía grupo] | 5 | newsletters |
| 20 | John Turner (john@wpvibe.ai) | 5 | newsletters |

**Remitentes 21-30**

| # | Remitente | Hilos | Cat. |
|---|---|---|---|
| 21 | OpenAI Ads Platform [vía grupo] | 5 | newsletters |
| 22 | PayPal [vía grupo] | 5 | mixto |
| 23 | Trello (do-not-reply@trello.com) | 5 | conversaciones |
| 24 | WPVibe (support@wpvibe.ai) | 5 | cuentas-usuario |
| 25 | WPVibe [vía grupo] | 5 | cuentas-usuario |
| 26 | nacho@the-storytellers.es | 5 | conversaciones |
| 27 | plataforma.contractacio@gencat.cat | 5 | ? |
| 28 | BBVA (bbva@comunica.bbva.com) | 4 | ofertas-comerciales |
| 29 | Claude Team (no-reply@email.claude.com) | 4 | newsletters |
| 30 | Consorci de Serveis Universitaris de Catalunya (nor… | 4 | ? |

**Remitentes 31-40**

| # | Remitente | Hilos | Cat. |
|---|---|---|---|
| 31 | GitHub (noreply@github.com) | 4 | alertas |
| 32 | Justicia Alimentaria [vía grupo] | 4 | ? |
| 33 | Nacho Ballesta - The Foodtellers Digital Food Agenc… | 4 | conversaciones |
| 34 | Password Protected [vía grupo] | 4 | newsletters |
| 35 | Portals web.ATIC (infoweb@ub.edu) | 4 | info-servicio |
| 36 | Eulàlia González Hernández (no-reply@mail.holded.co… | 3 | mixto |
| 37 | FetaLife Technologies (team@fetalifetech.com) | 3 | newsletters |
| 38 | Google Cloud (cloudplatform-noreply@google.com) | 3 | info-servicio |
| 39 | Lesianna Gnanguenon (l.gnanguenon@hypeauditorsapp.c… | 3 | ? |
| 40 | Open Arms (info@openarms.es) | 3 | newsletters |

_Top 40 = 248 hilos (70 %) de 355; remitentes distintos: 123._

## 3. Top 20 dominios

«vía grupo (desconocido)» agrupa lo que llega por alias de grupo: el dominio real no se ve sin leer el mensaje.

**Dominios 1-10**

| # | Dominio | Hilos | Remitentes |
|---|---|---|---|
| 1 | vía grupo (desconocido) | 79 | 34 |
| 2 | google.com | 16 | 4 |
| 3 | iahub.space | 15 | 1 |
| 4 | e.atlassian.com | 13 | 1 |
| 5 | the-storytellers.es | 12 | 3 |
| 6 | tm.openai.com | 12 | 1 |
| 7 | thefoodtellers.com | 11 | 2 |
| 8 | correo.aeat.es | 10 | 1 |
| 9 | wpvibe.ai | 10 | 2 |
| 10 | (informes DMARC) | 9 | 1 |

**Dominios 11-20**

| # | Dominio | Hilos | Remitentes |
|---|---|---|---|
| 11 | cdmon.com | 9 | 1 |
| 12 | cve-advocats.com | 9 | 1 |
| 13 | dreamhost.com | 8 | 1 |
| 14 | emexs.es | 7 | 1 |
| 15 | gmail.com (particulares) | 7 | 7 |
| 16 | send.holded.com | 7 | 1 |
| 17 | email.openai.com | 6 | 1 |
| 18 | gencat.cat | 6 | 2 |
| 19 | stripe.com | 6 | 1 |
| 20 | po.atlassian.net | 5 | 1 |

## 4. Adjuntos

- Hilos con adjunto: **60 de 355 (17 %)** (+1 hilo(s) que la consulta de adjuntos ve y el listado no).
- El dato es **por hilo** (no por mensaje) y `has:attachment` cuenta también imágenes incrustadas: el % de «imágenes» está inflado por firmas y logos (p. ej. avisos de cdmon).
- Los tipos se solapan (un hilo puede tener PDF e imagen).

| # | Tipo | Hilos | % de los adjuntos |
|---|---|---|---|
| 1 | PDF | 31 | 52 % |
| 2 | Imágenes (jpg/png/gif/webp) | 15 | 25 % |
| 3 | ZIP/GZ (informes DMARC) | 9 | 15 % |
| 4 | ICS/XML/PPT (invitaciones, DMARC) | 11 | 18 % |
| 5 | Word/ODT | 2 | 3 % |
| 6 | Excel/CSV | 0 | 0 % |

**Quién manda PDF (top 10)**

| # | Remitente | Hilos con PDF |
|---|---|---|
| 1 | Anthropic Ireland, Limited (invoice+statements+acct… | 6 |
| 2 | (particular @gmail.com) | 4 |
| 3 | Nuria García (nuriagarcia@cve-advocats.com) | 4 |
| 4 | rafa [vía grupo] | 3 |
| 5 | Growth Lab (info@growth-lab.es) | 2 |
| 6 | Google Payments (payments-noreply@google.com) | 2 |
| 7 | rafa@rmdisseny.es | 1 |
| 8 | Anthropic, PBC [vía grupo] | 1 |
| 9 | nacho@the-storytellers.es | 1 |
| 10 | SumUp [vía grupo] | 1 |

## 5. Recurrencias

- Mensual: ≥3 fechas distintas con mediana entre 24 y 36 días (o 2 fechas a 24-36 días = «posible»). Con 90 días **no se puede detectar lo anual**: abajo solo van pistas por palabras del asunto.
- Ojo: la bandeja solo contiene lo no archivado; si algo se archiva a mano, aquí se ve menos de lo que llega.

**Mensuales 1-3**

| # | Remitente | Veces | Tipo | Cat. |
|---|---|---|---|---|
| 1 | rafa [vía grupo] | 3 | mensual | facturas-proveedores |
| 2 | Google Payments (payments-noreply@google.com) | 2 | posible mensual (2 obs.) | facturas-saas |
| 3 | Metricool [vía grupo] | 2 | posible mensual (2 obs.) | facturas-saas |

**Alta frecuencia (≥6 fechas, mediana ≤7 días; top 10)**

| # | Remitente | Hilos | Cat. |
|---|---|---|---|
| 1 | IA Hub Barcelona (contact@iahub.space) | 15 | newsletters |
| 2 | Atlassian (info@e.atlassian.com) | 13 | newsletters |
| 3 | OpenAI (noreply@tm.openai.com) | 12 | mixto |
| 4 | John Turner [vía grupo] | 10 | newsletters |
| 5 | The Google Workspace Team (workspace-noreply@google… | 9 | info-servicio |
| 6 | Informes DMARC (thefoodtellers.com) | 9 | info-servicio |
| 7 | DreamHost Registration Service (support@dreamhost.c… | 8 | mixto |
| 8 | SiteGround Web Hosting [vía grupo] | 8 | newsletters |
| 9 | Holded (no-reply@send.holded.com) | 7 | mixto |
| 10 | Emexs Marketing (marketing@emexs.es) | 7 | newsletters |

**Posible anual (solo pista por palabras: renov/caduc/dominio/suscripción…; top 10)**

| # | Remitente | Hilos | Ejemplo de asunto |
|---|---|---|---|
| 1 | OpenAI (noreply@tm.openai.com) | 12 | ChatGPT - Your Business subscription re… |
| 2 | cdmon (no-reply@cdmon.com) | 9 | Recordatorio para la renovación de sus … |
| 3 | The Google Workspace Team (workspace-noreply@google… | 9 | Te damos la bienvenida a la suscripción… |
| 4 | Informes DMARC (thefoodtellers.com) | 9 | Report Domain: thefoodtellers.com Submi… |
| 5 | DreamHost Registration Service (support@dreamhost.c… | 8 | [cecser ***] danielgmoreno.com: Domain … |
| 6 | nacho@the-storytellers.es | 5 | Re: Forkandpillow > Apuntar dominio de … |
| 7 | SiteGround [vía grupo] | 2 | Confirmación de renovación del servicio |
| 8 | Mosyle Business (hello@business.mosyle.com) | 1 | Your Mosyle Business trial is about to … |
| 9 | Junta AFA (junta@afalaflordemaig.cat) | 1 | Fwd: Notificación de caducidad de certi… |
| 10 | Dropbox (no-reply@txn.dropbox.com) | 1 | Gracias por renovar tu plan Dropbox Sta… |

_Propuesta: un barrido de 12 meses solo de metadatos confirmaría lo anual. No se amplía la ventana sin tu OK._

## 6. Categorías tentativas y dudosos

Reparto de **hilos** por categoría propuesta (por hilo, no por remitente):

**Categorías 1-10**

| # | Categoría | Hilos | Remitentes |
|---|---|---|---|
| 1 | spam | 0 | 0 |
| 2 | newsletters | 109 | 25 |
| 3 | info-servicio | 49 | 18 |
| 4 | conversaciones | 15 | 4 |
| 5 | ofertas-comerciales | 14 | 11 |
| 6 | alertas | 17 | 7 |
| 7 | recordatorios-suscripcion | 18 | 6 |
| 8 | pagos-cobros | 5 | 3 |
| 9 | facturas-proveedores | 11 | 5 |
| 10 | facturas-saas | 20 | 10 |

**Categorías 11-15**

| # | Categoría | Hilos | Remitentes |
|---|---|---|---|
| 11 | bancos | 3 | 1 |
| 12 | impuestos | 19 | 2 |
| 13 | cuentas-usuario | 26 | 10 |
| 14 | otros | 0 | 0 |
| 15 | **? dudoso (sin regla)** | 49 | 32 |

_Clasificables por remitente/asunto: 306 hilos (86 %); alta 213, media 93; dudosos 49 (14 %)._

**Dudosos y mixtos: 37 remitentes (91 hilos). Se muestran los 30 con más hilos.**

«mixto» = una regla por remitente no basta, pero el asunto sí distingue (no hace falta leer cuerpo). «?» = hace falta abrir el cuerpo o que Cecil decida.

**Dudosos D1-D10**

| # | Remitente | Hilos | Motivo / ejemplo |
|---|---|---|---|
| D1 | OpenAI (noreply@tm.openai.com) | 12 | mixto: alertas/cuentas-usuario/pagos-cobros/recordatorios-suscripcion/? |
| D2 | DreamHost Registration Service (support@dreamhost.c… | 8 | mixto: facturas-saas/info-servicio/recordatorios-suscripcion |
| D3 | Holded (no-reply@send.holded.com) | 7 | mixto: cuentas-usuario/facturas-proveedores |
| D4 | WordPress (wordpress@thefoodtellers.com) | 7 | mixto: cuentas-usuario/info-servicio |
| D5 | WordPress (no-reply@the-storytellers.es) | 6 | ? formulario web: requiere cuerpo · «TST - CONTACTO WEB» |
| D6 | PayPal [vía grupo] | 5 | mixto: newsletters/pagos-cobros |
| D7 | plataforma.contractacio@gencat.cat | 5 | ? administración pública: ¿categoría nueva? · «Novetats de E2343 Consorci de Ser…» |
| D8 | Consorci de Serveis Universitaris de Catalunya (nor… | 4 | ? administración pública: ¿categoría nueva? · «IMPORTANT: Avís de notificació de…» |
| D9 | Justicia Alimentaria [vía grupo] | 4 | ? entidad/cliente: boletín y presupuesto · «🛒 ¡HAGAMOS HUELGA DE COMPRAS! ‼️ …» |
| D10 | Eulàlia González Hernández (no-reply@mail.holded.co… | 3 | mixto: cuentas-usuario/facturas-proveedores |

**Dudosos D11-D20**

| # | Remitente | Hilos | Motivo / ejemplo |
|---|---|---|---|
| D11 | Lesianna Gnanguenon (l.gnanguenon@hypeauditorsapp.c… | 3 | ? sin regla: requiere cuerpo · «Por si en algún momento surge una…» |
| D12 | ChatGPT [vía grupo] | 2 | mixto: cuentas-usuario/? |
| D13 | (particular @gmail.com) | 1 | ? particular: requiere cuerpo · «Application for Internship – Janu…» |
| D14 | (particular @gmail.com) | 1 | ? particular: requiere cuerpo · «Re: Internship Application — Grap…» |
| D15 | (particular @gmail.com) | 1 | ? particular: requiere cuerpo · «Accepted: Consell d'Infants - Ses…» |
| D16 | (particular @gmail.com) | 1 | ? particular: requiere cuerpo · «Re: Envato Elements» |
| D17 | (particular @gmail.com) | 1 | ? particular: requiere cuerpo · «Re: Agencia de Mkt» |
| D18 | (particular @gmail.com) | 1 | ? particular: requiere cuerpo · «Social media y contenido: mi perf…» |
| D19 | (particular @gmail.com) | 1 | ? particular: requiere cuerpo · «Muuuuuucho interés en formar part…» |
| D20 | Carmen Moccia (carmen.moccia@crg.eu) | 1 | ? sin regla: requiere cuerpo · «RE: Slidedecks EvoMG-DN and ProtA…» |

**Dudosos D21-D30**

| # | Remitente | Hilos | Motivo / ejemplo |
|---|---|---|---|
| D21 | Comunicacio (comunicacio@canal.es) | 1 | ? sin regla: requiere cuerpo · «Test» |
| D22 | David Avila Coronado (david@seoprojects.es) | 1 | ? sin regla: requiere cuerpo · «Propuesta colaboración» |
| D23 | David Monge (d@tryember.site) | 1 | ? sin regla: requiere cuerpo · «Sneakers limitados» |
| D24 | Fav - Studio (info@fav-studio.com) | 1 | ? sin regla: requiere cuerpo · «Fitur 2027» |
| D25 | Fernando Pazos (fernando@bigfidelity.com) | 1 | ? sin regla: requiere cuerpo · «Colaboración entre The Foodteller…» |
| D26 | Guillermo Lasso (g.lasso@glotio.com) | 1 | ? sin regla: requiere cuerpo · «Mejora el ratio de conversión de …» |
| D27 | Hailey (hailey@bookedlab.org) | 1 | ? sin regla: requiere cuerpo · «Conceptos de marca» |
| D28 | Juan Pablo (info@clarisdata.es) | 1 | ? sin regla: requiere cuerpo · «Informacion de The Foodtellers - …» |
| D29 | Junta AFA (junta@afalaflordemaig.cat) | 1 | ? sin regla: requiere cuerpo · «Fwd: Notificación de caducidad de…» |
| D30 | Mia Taylor (mia.taylor@nextgrowiq.com) | 1 | ? sin regla: requiere cuerpo · «Quick question Cecil» |

_Quedan 7 remitentes más (casi todos con 1-2 hilos), no listados._

## 7. Etiquetas de usuario ya en uso (en estos hilos)

Tu buzón ya tiene un sistema de etiquetas. Conviene respetarlo en la fase 2.

| # | Etiqueta | Hilos |
|---|---|---|
| 1 | TST/HOLA | 72 |
| 2 | TFT/Hola | 30 |
| 3 | TFT | 20 |
| 4 | __POR PAGAR | 4 |
| 5 | __POR CONCILIAR | 4 |
| 6 | TST | 4 |
| 7 | Facturas | 2 |

## 8. Hallazgos y límites

- Hilo 1a0f6dbb76348834 (1-oct, hosting web de la UB, «Noves credencials»): el fragmento que devuelve Gmail muestra usuario y contraseña en claro. No se ha copiado en ningún sitio. Conviene rotar esa contraseña y tratar el hilo como sensible.
- Los fragmentos de otros hilos incluyen códigos de verificación (GitHub, Vercel, Holded, WPVibe, ChatGPT) y un NIF/IBAN parcialmente enmascarados. Tampoco se han guardado; en data/ solo hay remitente, fecha, etiquetas y asunto.
- El estimado de resultados de Gmail (201) no era fiable: el listado real tiene más páginas. La paginación por la vista SUMMARY omitió al menos 1 hilo con PDF (1a140c94ee69567f) que sí aparece en la consulta de adjuntos.
- La bandeja tiene 5.975 hilos en total (408 sin leer); este informe solo cubre los de los últimos 90 días.
- La vista SUMMARY devuelve el último mensaje de cada hilo: en hilos largos el remitente puede ser el último que contestó, no quien lo abrió.
- Los alias («Hola», «AI», «Dev Team», «Admin TFT») ocultan al remitente real; ya se agrupan por nombre visible.
- Para regenerar este informe hay que repetir la extracción en una sesión con el conector de Gmail (ver cabecera del script). `data/` se borra al cerrar la tarea (regla 6).
- Sin cuerpos ni adjuntos abiertos; no se ha escrito nada en el buzón.
