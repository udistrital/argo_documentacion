# Browser Fingerprinting Open Source en Argo (Angular 21 + single-spa)

Issue: udistrital/argo_documentacion#376 · Milestone: Soporte y arquitectura general · Fecha: 2026-10-15
PRs: [udistrital/gestion_contractual_crud#49](https://github.com/udistrital/gestion_contractual_crud/pull/49) · [udistrital/gestion_contractual_mf#130](https://github.com/udistrital/gestion_contractual_mf/pull/130) · [udistrital/argo_documentacion#380](https://github.com/udistrital/argo_documentacion/pull/380)

## 1. Contexto y alcance
La issue pide investigar, evaluar e implementar una solución de browser fingerprinting de código abierto en Angular bajo single-spa, capturar la IP pública del cliente, construir un componente reutilizable entre microclientes y enviar la telemetría al backend con fines de auditoría y seguridad.

El texto original de la issue menciona "Sísifo v2" y `sisifo_documentacion`. En la reunión del 2026-10-15 el líder técnico confirmó que el alcance es **Argo**: la PoC se hace en `gestion_contractual_mf` y el informe se publica en este repositorio.

| Tema | Decisión del LT (2026-10-15) |
|---|---|
| Alcance | Argo (`gestion_contractual_mf`) |
| Backend | Módulo nuevo en `gestion_contractual_crud`; en la organización no existe un CRUD genérico de auditoría o telemetría (`seguimiento_crud` es de alternancia) |
| Ubicación del componente reutilizable | En stand by; se documentan las opciones (sección 7) |
| IP | La captura el cliente y se complementa con la huella |
| Privacidad | Se documenta (sección 10) |
| Precisión | Se documenta que la versión open source no garantiza unicidad |

## 2. Qué es el browser fingerprinting y qué no es
Consiste en combinar características del navegador y del equipo (renderizado de canvas y WebGL, procesamiento de audio, fuentes instaladas, pantalla, zona horaria, idioma, hardware) y resumirlas en un hash. No usa cookies ni almacenamiento persistente.

Limitaciones que condicionan su uso:
- **No es un identificador único.** Dos equipos con el mismo hardware, sistema y navegador pueden producir la misma huella. En la Universidad esto es probable en salas de cómputo y equipos con imagen corporativa.
- **No es estable en el tiempo.** Cambia con actualizaciones del navegador o de drivers, cambios de monitor, zoom o idioma.
- **Los navegadores con protección anti-fingerprinting** (Brave, Firefox con resistFingerprinting, Safari) agregan ruido o uniforman valores.
- **Se calcula en el cliente**, así que un usuario técnico puede falsearla.

**Uso recomendado en Argo:** señal complementaria de auditoría, junto con usuario, rol, IP y fecha. No debe usarse como control de acceso ni como prueba única de identidad.

## 3. Librerías evaluadas
| Criterio | FingerprintJS v5 | ThumbmarkJS | ClientJS | Implementación nativa propia |
|---|---|---|---|---|
| Licencia | MIT (v5). La v4 estuvo bajo BSL desde 2023, que exigía pago para uso comercial; volvió a MIT en octubre de 2025 | MIT | Apache-2.0 | Propia |
| Versión evaluada | 5.3.0 (publicada en npm el 2026-10-07) | 1.12.0 (publicada en npm el 2026-09-25) | 0.2.1 (octubre de 2021) | — |
| Mantenimiento | Activo; empresa detrás (Fingerprint) | Activo | Sin publicaciones desde 2021; repositorio es fork de fork | A cargo de OATI |
| Distribución | npm, ESM, tipos TypeScript incluidos | npm, ESM/CJS/UMD | npm, CJS; tipos por @types | — |
| Resultado | `visitorId`, `confidence.score` (0 a 1), componentes con duración, versión | Hash `thumbmark` y componentes | Entero de 32 bits | Hash (p. ej. SHA-256) |
| Precisión declarada | El fabricante indica que es significativamente menos precisa que su versión de pago y vulnerable a suplantación | El proyecto declara cerca del 80 % de unicidad en poblaciones generales; más colisiones en Safari/Mac | "Estadísticamente significativa", sin cifra; 32 bits implica más colisiones | Depende de lo que se implemente |
| Llamadas de red propias | Monitoreo de uso: en el 0,1 % de las llamadas a `load()` hace un GET a `m1.openfpcdn.io/fingerprintjs/v<versión>/npm-monitoring`, y con él viajan la IP y los headers del cliente. En el código de la 5.3.0 el único límite es ese muestreo aleatorio (no encontré un tope semanal). Se desactiva con `monitoring: false` | En el 0,01 % de las ejecuciones (una vez por sesión) envía a `api.thumbmarkjs.com/log` la huella, los **componentes crudos**, las opciones y la ruta, y descarga y evalúa con `eval` un script de `experimental.thumbmarkjs.com`. Se desactiva con `logging: false` | Ninguna | Ninguna |
| Tamaño en el build de producción del MF | 36,62 kB (14,21 kB transferidos) | 32,29 kB (10,84 kB transferidos) | No medido | — |
| Tiempo de cálculo medido (build de producción, Chrome) | 207 a 266 ms | 258 a 364 ms | No medido | — |
| Estabilidad observada en la PoC | Misma huella en pestañas nuevas, incógnito y ventana privada de Firefox; distinta entre Chrome y Firefox (sección 9) | Igual que FingerprintJS (sección 9) | — | — |
| Resultado | **Seleccionada** | **Alternativa** (segundo adaptador) | **Descartada** por obsolescencia | **Descartada**: reimplementar y mantener las técnicas sin ganancia frente a las librerías |

Las cifras de red y de muestreo de las dos librerías se verificaron en el código instalado (`node_modules/@fingerprintjs/fingerprintjs/dist/fp.esm.js` y `node_modules/@thumbmarkjs/thumbmarkjs/dist/thumbmark.esm.js`). En la PoC, con la configuración obligatoria, ninguna de las dos hizo peticiones a sus dominios.

## 4. Selección y justificación
Se selecciona **FingerprintJS v5** como librería por defecto porque:
- tiene licencia MIT y mantenimiento activo;
- entrega un puntaje de confianza que permite registrar qué tan fiable fue cada huella;
- expone los componentes con su duración, útil para analizar la estabilidad;
- se distribuye por npm con ESM y tipos, y el monitoreo de uso se puede desactivar;
- en la PoC fue la que menos bloqueó el hilo principal (sección 9).

ThumbmarkJS queda implementada como segundo adaptador y se puede activar desde el environment (`HUELLA_NAVEGADOR.LIBRERIA`) sin tocar el servicio. Esto permite cambiar de librería si cambian las condiciones de licencia o mantenimiento.

**Condición obligatoria de configuración:** FingerprintJS con `monitoring: false` y ThumbmarkJS con `logging: false`. La CSP del root (`gestion_contractual_root_mf/src/index.ejs`) permite `script-src 'unsafe-eval' https:` y `connect-src https:`, así que sin esa configuración los envíos y el script remoto de ThumbmarkJS sí se ejecutarían. En ThumbmarkJS también se fija `collect_beacon: false`: hoy solo actúa con `api_key`, pero así no depende de eso.

## 5. Captura de la dirección IP
| Opción | Cómo | Ventajas | Riesgos |
|---|---|---|---|
| a) Cliente con servicio de eco (**decisión del LT**) | `fetch` a `https://api64.ipify.org?format=json` | Funciona sin cambios en el gateway; ipify es open source, declara no registrar visitantes y no tiene límite de uso | Se envía la IP del usuario y el origen de la página a un tercero; desde la red de la Universidad o la VPN devuelve la IP pública del NAT, no la del equipo; el usuario puede falsearla; si el servicio cae o lo bloquea un bloqueador de anuncios, se registra null |
| b) Servidor | El backend lee `X-Forwarded-For` | No se puede falsear desde el navegador sin controlar la red; no involucra terceros. Ya es el patrón de `utils_oas/auditoria` en las APIs Beego (`ctx.Input.IP()`) | Requiere que el gateway propague el header |

**Implementación:** se registran ambas. El cliente envía `direccion_ip` (opción a, según la decisión) y el CRUD guarda `direccion_ip_servidor` (opción b) a partir de `X-Forwarded-For`. Resultado en la PoC: `direccion_ip` = la IPv6 pública del equipo (`2800:x:x:x:x`; `api64` responde en IPv6 cuando la red lo tiene y en IPv4 si no) y `direccion_ip_servidor` = `::1`, porque el CRUD corría en el mismo equipo. No coinciden, como se esperaba en local. Red usada: WiFi residencial, sin VPN y fuera de la red de la Universidad. Si el servicio de eco falla o supera los 3 s, el registro se guarda con `direccion_ip` en null (cubierto por pruebas).
Falta verificar, cuando se despliegue, que el API Gateway (`autenticacion.portaloas.udistrital.edu.co/apioas`) propague `X-Forwarded-For` hasta el CRUD; en local siempre será la IP del equipo o localhost.

## 6. Compatibilidad con single-spa
- El servicio vive en el injector del MF (`providedIn: 'root'`); al hacer unmount se destruye y `DestroyRef` cancela el callback pendiente, aborta el `fetch` y la petición HTTP.
- Se calcula y envía una sola vez por sesión: la marca `argo_huella_navegador_registrada` en sessionStorage la comparten todos los MF del mismo origen.
- Se dispara con `afterNextRender` + `requestIdleCallback`, después del primer render, sin bloquear el bootstrap.
- **Las librerías se cargan con import estático, no dinámico.** El diseño proponía `import()` en un chunk aparte y así funcionó con las configuraciones `local` y `development` del MF, que definen `deployUrl`: el chunk se descargó desde el origen del MF (`localhost:4201`). Con la configuración `production`, que no define `deployUrl`, el chunk se pidió al origen del root (`http://localhost:4200/contratos/876.js`) y respondió 404; la huella no se calculó y el servicio quedó en estado `error`. Por eso se pasó a import estático. Impacto en el `main.js` de producción: 2,56 MB → 2,63 MB (+66 kB sin comprimir, +22 kB de transferencia estimada). Frente a `develop` el aumento total es de +74 kB sin comprimir (+24 kB transferidos).
- Nodos y variables globales que quedan después del cálculo: ninguno con las dos librerías. FingerprintJS crea y quita 2 iframes temporales en `body` y ThumbmarkJS 1, durante el cálculo. Al final el DOM, las variables de `window` y `localStorage` son idénticos a los de una carga de control en la que la librería no se ejecuta; en `sessionStorage` solo queda la marca propia.
- Montaje y desmontaje repetido: navegando dentro del root de `/contratos/` a `/inicio` y de vuelta, el MF se desmontó y se volvió a montar sin un segundo envío y sin errores nuevos en consola (los que aparecen también salen en la carga de control; ver sección 13).
- No se usa Web Worker: la CSP del root no incluye `worker-src` ni `blob:`, y las técnicas de canvas, WebGL y audio dependen de APIs del hilo principal.

## 7. Arquitectura y opciones de reutilización
Flujo: `AppComponent` (afterNextRender) → `HuellaNavegadorService` → `ProveedorHuella` (FingerprintJS | ThumbmarkJS) + servicio de eco de IP → `POST gestion_contractual_crud/huellas-navegador`.

Archivos en `gestion_contractual_mf`: `src/app/core/services/huella-navegador/` (modelos, utilidad de hash de componentes, adaptadores, token del proveedor, servicio) y el cambio en `core/intercerptors/spinner.interceptor.ts` (`OMITIR_SPINNER`).

Opciones para compartirlo entre microclientes (decisión en stand by):
| Opción | Ventajas | Desventajas |
|---|---|---|
| a) Utility module de single-spa cargado por import map desde el root | Una sola instancia y un solo cálculo para todos los MF; se actualiza en un solo lugar | Hay que exponer una API en TypeScript plano (la inyección de dependencias de Angular no se comparte entre MF) y registrarlo en el import map del root |
| b) Librería Angular publicada en npm (precedente: `udistrital/utils_frontend`) | Versionado; patrón ya conocido en OATI | Cada MF debe actualizar la dependencia; cada MF tiene su instancia (la marca en sessionStorage evita envíos duplicados) |
| c) Copiar el servicio en cada MF (lo hecho en la PoC) | Simple, sin infraestructura nueva | Duplicación de código y de correcciones |

Recomendación: b) a corto plazo, porque ya existe `utils_frontend` como precedente, y evaluar a) si se quiere un cálculo único para toda la plataforma.

## 8. Contrato de datos
**Payload del cliente** (`POST /huellas-navegador`):
```json
{
  "huella": "1a7908f9************************",
  "libreria": "fingerprintjs",
  "version_libreria": "5.3.0",
  "confianza": 0.7,
  "componentes": { "canvas": { "hash": "a1b2c3d4e5f60718", "duracion_ms": 12, "error": false } },
  "direccion_ip": "190.x.x.x",
  "user_agent": "Mozilla/5.0 ...",
  "usuario_id": 123,
  "usuario_rol": "ROL",
  "microcliente": "gestion_contractual_mf",
  "ruta": "/gestion-contractual/consulta-contrato",
  "fecha_captura": "2026-10-16T15:00:00.000Z"
}
```
Los componentes se envían solo como hash SHA-256 truncado a 16 caracteres más su duración (minimización: no se almacenan los valores crudos de canvas, fuentes, etc.). La ruta se envía sin query string.

`usuario_id` y `usuario_rol` salen de las mismas fuentes que usa el MF al registrar `estados-contrato`: `UserService.getPersonaId()` y `RolService.getRol()`. Como aquí no hay un contrato del cual derivar el rol, se toma el primer rol de Argo del usuario. Sin sesión, ambos van en null.

**Tabla `huella_navegador`** (`gestion_contractual_crud`, script en `sql/creacion-tablas.sql`): id serial, huella varchar(64), libreria varchar(50), version_libreria varchar(20), confianza numeric(5,4) nula, componentes jsonb nula, direccion_ip varchar(45) nula, direccion_ip_servidor varchar(45) nula, user_agent varchar(512), usuario_id integer nula, usuario_rol varchar(40) nula, microcliente varchar(100), ruta varchar(255) nula, fecha_captura timestamp, activo, fecha_creacion, fecha_modificacion. Restricciones: `pk_huella_navegador`, `idx_huella_navegador_huella`, `idx_huella_navegador_usuario_id`.

**Endpoints:** `POST /huellas-navegador`, `GET /huellas-navegador` (filtros y paginación) y `GET /huellas-navegador/:id`, todos con StandardResponse. No se exponen PATCH ni DELETE: es un registro de auditoría y no debe poder modificarse. Si se define una política de retención, se agregaría un DELETE lógico.

## 9. Rendimiento y estabilidad (resultados de la PoC)
Equipo: AMD Ryzen 5 3500U, 8 hilos, 13 GB de RAM, Ubuntu 22.04, Chrome 155 y Firefox 157. Root y MF servidos en local. Los tiempos son de tres corridas por librería con el MF en configuración `production`; entre paréntesis, una corrida con el build de desarrollo (sin optimizar e incluyendo la descarga del chunk dinámico). Una long task es una tarea del hilo principal de más de 50 ms.

| Medición | FingerprintJS | ThumbmarkJS |
|---|---|---|
| Tiempo de cálculo (`huella-navegador-calculo`) | 207 a 266 ms (desarrollo: 847 ms) | 258 a 364 ms (desarrollo: 1 081 ms) |
| Long tasks atribuibles al cálculo | 1 por carga, de 126 a 157 ms (desarrollo: 7 tareas, la mayor de 249 ms) | 1 por carga, de 231 a 332 ms (desarrollo: 1 de 990 ms) |
| Tamaño | 36,62 kB (14,21 kB transferidos); con el import estático va dentro de `main.js` | 32,29 kB (10,84 kB transferidos); también dentro de `main.js` |
| Misma huella entre pestañas nuevas | Sí (`1a7908f9…` en todas las pestañas de las corridas en Chrome) | Sí (`df30b952…`) |
| Misma huella normal vs incógnito | Sí en Chrome; sí en Firefox (ventana privada) | Sí en Chrome; sí en Firefox |
| Huella en otro navegador del mismo equipo | Distinta: Firefox 157 da `e0617202…` (estable entre normal y privada) | Distinta: Firefox 157 da `81c6941c…` |
| Confianza reportada | 0,7 en Chrome 155 y en Firefox 157 | No aplica |

Las long tasks se atribuyen al cálculo porque empiezan dentro de la ventana de `huella-navegador-calculo`, y porque al recargar la misma pestaña (sin cálculo, la marca ya existe) no aparece ninguna o solo una de 50 a 60 ms durante el arranque de la app.

Conclusión sobre el criterio "sin bloquear el hilo principal": **se considera cumplido, con esta nota.**
- La transmisión de la huella es asíncrona y no bloquea: el `fetch` a ipify y el POST al CRUD no ocupan el hilo principal, no muestran spinner ni alertas.
- El cálculo genera **una long task por sesión**: de 126 a 157 ms con FingerprintJS, por debajo del umbral de 200 ms que Google considera bueno para la respuesta a interacciones (INP), y de 231 a 332 ms con ThumbmarkJS, por encima de ese umbral.
- El cálculo se ejecuta en un momento ocioso, después del primer render (`afterNextRender` + `requestIdleCallback`), así que no retrasa el bootstrap del MF ni la primera pintura.
- No puede moverse a un Web Worker: las técnicas de canvas y audio requieren el hilo principal y la CSP del root no permite `blob:` (no define `worker-src`).

Esto refuerza la elección de FingerprintJS: es la única de las dos librerías cuya long task queda por debajo de 200 ms.

## 10. Privacidad y normativa
*Este análisis es técnico y no reemplaza un concepto jurídico.*
- Según la Superintendencia de Industria y Comercio (Concepto 277885 de 2015), la dirección IP es dato personal cuando está vinculada a una persona o permite identificarla. Aquí la IP y la huella se guardan junto al `usuario_id`, así que ambas deben tratarse como **datos personales** bajo la Ley 1581 de 2012 y el Decreto 1377 de 2013 (compilado en el Decreto 1074 de 2015).
- Principios que aplican (art. 4, Ley 1581): **finalidad** (auditoría y seguridad de Argo, informada al titular), **libertad** y **transparencia** (el aviso o la política de tratamiento deben mencionar esta recolección), **seguridad** y **acceso y circulación restringida** (solo personal autorizado consulta la tabla).
- Medidas ya aplicadas en la PoC: componentes solo como hash truncado, ruta sin query string, sin valores crudos, monitoreo de las librerías desactivado, IP del servidor para no depender solo de un tercero.
- **Tercero:** con la opción a) se envía la IP del usuario a ipify, un servicio externo. Debe evaluarse si es aceptable o si basta con la IP del servidor.
- Pendientes para la Universidad: confirmar que la política de tratamiento de datos y el aviso de privacidad cubren esta finalidad; definir el tiempo de retención y la disposición final de los registros (el documento de controles de protección de datos publicado por la Universidad muestra pendientes las políticas de ciclo de vida y disposición final); definir quién puede consultar la tabla. Se recomienda validar con OATI y la dependencia jurídica antes de activarlo en producción.

## 11. Mantenibilidad y riesgos
- **Licencia:** FingerprintJS ya cambió de licencia una vez (v4 BSL). Se fija `^5` y antes de subir de versión mayor hay que revisar la licencia.
- **Configuración por defecto insegura en ThumbmarkJS** (`logging: true`): cualquier integración nueva debe mantener `logging: false`.
- **Precisión decreciente:** los navegadores siguen endureciendo sus protecciones contra fingerprinting, así que la precisión tenderá a bajar con el tiempo.
- **ClientJS** sin mantenimiento desde 2021.
- El patrón de adaptadores permite reemplazar la librería sin tocar el servicio ni el contrato con el backend.
- **Import estático:** las dos librerías van en el bundle principal aunque solo se use una. Si se corrige el `deployUrl` de la configuración `production` (sección 13), se puede volver al import dinámico y sacarlas del bundle.

## 12. Guía de integración en otro microcliente
1. Copiar `src/app/core/services/huella-navegador/` (o instalar la librería compartida cuando se decida la sección 7).
2. Instalar `@fingerprintjs/fingerprintjs@^5` (y `@thumbmarkjs/thumbmarkjs` si se usa).
3. Agregar el bloque `HUELLA_NAVEGADOR` al environment con el `MICROCLIENTE` propio y la URL del CRUD.
4. Si el MF tiene un interceptor de spinner o de errores, permitir omitirlo con un `HttpContextToken` como `OMITIR_SPINNER`.
5. En `AppComponent`: `afterNextRender(() => inject(HuellaNavegadorService).iniciar())` (en el constructor).
6. Verificar que la CSP del root permita `connect-src` al servicio de IP y al CRUD.
7. Si se usa import dinámico para las librerías, verificar que la configuración de build del MF defina `deployUrl`; sin él, el chunk se pide al origen del root (sección 6).

## 13. Hallazgos adicionales
- `ng test` falla en `gestion_contractual_mf` porque `@angular-builders/jest` no está instalado; las pruebas se ejecutan con `pnpm test`.
- El root (`gestion_contractual_root_mf`) carga single-spa 5.9.0 y zone.js 0.11.3 por CDN, mientras el MF compila contra single-spa 6.0.3 y zone.js 0.15.1.
- `RequestManager` usa un `setPath` mutable compartido por todos los servicios: dos peticiones simultáneas a servicios distintos pueden pisarse la URL.
- El interceptor del spinner afectaba cualquier petición en segundo plano; se agregó `OMITIR_SPINNER`.
- `gestion_contractual_crud` (NestJS) no tiene un middleware de auditoría equivalente a `utils_oas/auditoria` de Beego, así que sus peticiones no dejan IP ni user agent en los logs.
- `environment.ts` y `environment.development.ts` del MF son idénticos (`production: false`).
- **La configuración `production` del MF no define `deployUrl`.** Bajo single-spa, cualquier chunk de carga diferida (`import()`, rutas lazy, librerías que cargan módulos bajo demanda) se pide al origen del root y no al del MF, y responde 404. Afecta a cualquier lazy loading futuro del MF, no solo a la huella: le pasó a la huella en la PoC (sección 6) y, por el mismo mecanismo, probablemente afecta hoy al chunk lazy de `ngx-quill` (editor enriquecido), aunque esto último no se probó. Las configuraciones `local` y `development` sí definen `deployUrl` y no tienen el problema.
- **`pnpm run build:prod` del MF falla en `develop`** por el presupuesto de 2 MB del bundle inicial (`main.js` = 2,56 MB). Es el script que usa el paso de `master` en `.drone.yml`.
- **Pruebas del MF con red real:** los specs de `revision-contrato`, `paso-info-general` y `consulta-contrato` hacen peticiones reales al gateway (responde 401). Cuando la respuesta llega tarde, su callback abre un SweetAlert sobre un documento ya destruido y jest atribuye ese error a la suite que esté corriendo en ese momento. En `develop` el error aparece en 5 de 6 corridas sin tumbar ninguna suite. Con las suites nuevas, en unas 2 de 10 corridas cae sobre una de ellas y jest reporta la suite como fallida aunque todas las pruebas pasen.
- **Pruebas del CRUD:** en `develop` fallan 6 suites (10 pruebas) que ya estaban desactualizadas: `acta-inicio`, `cdp`, `contratista`, `contrato-general`, `especificacion-tecnica` y `ordenador-contrato` (mocks de repositorios faltantes y firmas antiguas). Las pruebas del módulo nuevo pasan.
- **Errores de validación del CRUD:** los 400 del `ValidationPipe` global no salen en formato StandardResponse, porque el pipe responde antes de llegar al controlador. Pasa en todos los módulos.
- **Fechas en el CRUD:** las columnas son `timestamp without time zone` con `DEFAULT now()`. En local, con PostgreSQL en UTC y Node en hora de Colombia, `fecha_creacion` quedó 5 horas corrida respecto a `fecha_captura` (ver evidencia 02). En los ambientes desplegados depende de que la base y el contenedor usen la misma zona horaria.
- **`core-mf` no carga en localhost por CORS:** se carga desde `pruebascoreclientes.portaloas.udistrital.edu.co`, que no permite el origen `localhost:4200`. Sin `core-mf` no hay login en local, así que en la PoC `usuario_id` y `usuario_rol` llegaron en null; ese caso se cubrió solo con pruebas unitarias.
- **`RolService.cargarRol()` falla sin sesión:** lanza `TypeError: Cannot read properties of undefined (reading 'role')` cuando no hay usuario en `localStorage`.
- `pnpm` 12.4.1 (el `packageManager` de los repos) no arranca con el corepack de Node 20; el CI usa Node 24.

## 14. Referencias
- FingerprintJS: https://github.com/fingerprintjs/fingerprintjs y API: https://github.com/fingerprintjs/fingerprintjs/blob/master/docs/api.md
- Cambio de licencia de FingerprintJS a MIT (v5): https://fingerprint.com/blog/fingerprintjs-version-5-0-mit-license/
- ThumbmarkJS: https://github.com/thumbmarkjs/thumbmarkjs
- ClientJS: https://github.com/BendingBender/clientjs
- ipify: https://www.ipify.org/
- SIC, Concepto 277885 de 2015 (IP como dato personal)
- Ley 1581 de 2012 y Decreto 1377 de 2013

## 15. Evidencia
Ver la carpeta `evidencias/` (pantallazos numerados del 01 al 08). En las capturas la IP pública aparece difuminada (02) o enmascarada en la consulta (03). Las huellas que se ven son las del equipo de prueba, sin usuario asociado.

| Archivo | Qué muestra |
|---|---|
| `01-network-ipify-y-post.png` | Pestaña Network de Chrome: petición a `api64.ipify.org` (200), preflight (204) y POST a `huellas-navegador` (201); la página sin spinner |
| `02-respuesta-post.png` | Respuesta StandardResponse del POST |
| `03-registro-bd.png` | `SELECT` de `huella_navegador` con un registro de cada librería y la estructura de la tabla |
| `04-rendimiento.png` | `performance.getEntriesByName('huella-navegador-calculo')` y la tabla de long tasks (FingerprintJS) |
| `05-sessionstorage-una-vez-por-sesion.png` | Tras recargar la misma pestaña: la marca en sessionStorage y ningún POST nuevo |
| `06-swagger-huellas-navegador.png` | Los 3 endpoints en `/swagger` |
| `07-pruebas-mf.png` | `pnpm test` del MF (30 suites, 59 pruebas) y las suites nuevas |
| `08-pruebas-crud.png` | Pruebas del módulo `huellas-navegador` del CRUD (22 pruebas) |
