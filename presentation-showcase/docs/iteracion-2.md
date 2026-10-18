# Misión 2 · Qué cambió y cómo se revisó

Fecha de cierre: 18 de octubre de 2026. Preparación, implementación y validación de esta iteración realizadas por Codex a partir de las decisiones que el candidato declaró en su solicitud. Esto no acredita que el candidato haya ejecutado personalmente esas validaciones.

## Punto de partida

La rama de trabajo es `presentation/conectapyme-junior-pov`. Se verificó que la rama preparada partía exactamente de `bad88c56d850a87d188a9b0d7a4d515f6766f408`, igual que la versión original `presentation/conectapyme-evidence-showcase`. Se usó un worktree independiente. Los cambios se limitan a `presentation-showcase/`; no se modificaron `main`, el motor productivo, los datasets, las pruebas originales ni las evidencias de la primera versión.

El código productivo que respalda las cifras sigue siendo `774dacd80e6410ca43299f63f19d9744a31929c0`. El commit de esta iteración de presentación se puede consultar en Git y en el PR; no sustituye al commit de origen de los resultados técnicos.

## Una historia desde el punto de vista del candidato

Se conservaron la identidad visual, las fuentes locales, los diagramas y las capturas reales. La presentación ahora sigue las decisiones del candidato: entender el reto, elegir adquisición B2B en una Telco ficticia, plantear una hipótesis, construir una PoC sintética con apoyo de IA, comparar reglas y explicar qué falta medir.

- La primera diapositiva muestra la pregunta central del reto de Totalplay. Se leyeron las 13 diapositivas del PPTX y sus notas; la extracción completa, su huella y las diferencias entre ejemplos del reto y resultados propios están en `reto-original.md`.
- El contexto empresarial es una simulación. No se atribuyen a Totalplay procesos, resultados ni problemas operativos de ConectaPyME.
- La forma de trabajo se explica una vez: ChatGPT/GPT, Gemini y Codex apoyaron el desarrollo; el candidato declara haber definido el alcance, revisado propuestas y tomado decisiones. Los registros técnicos conservan su origen automatizado.
- El caso elegido incluye empresas similares o conectadas con clientes actuales. La PoC implementa una regla de vecinos económicos confirmados; no implementa similitud aprendida ni una ponderación especial por conexión con clientes actuales. Esta diferencia se explica en las notas y en `origen-y-alcance.md`.
- Se explica por qué se comenzó con reglas. KNN, modelos supervisados, comunidades y RL quedan como opciones consideradas, sujetas a preguntas y datos distintos. No se presentan como modelos implementados ni como una ruta obligatoria.

Hay **16 diapositivas principales y 14 de anexo**. Filtros globales, embudo y depuración siguen disponibles en el anexo. Cada diapositiva tiene discurso en primera persona, evidencia que señalar, pregunta, respuesta sencilla, explicación adicional y advertencia. Los discursos principales duran aproximadamente 52–59 segundos a 140 palabras por minuto; la exposición principal suma unos 14.7 minutos, sin preguntas ni interacción.

La fuente editable es `scripts/content.py`. Se regeneraron `content.json`, `data.js`, `docs/guion.md`, `docs/guia-estudio.html` y `docs/trazabilidad.csv` con `scripts/build_material.py`. No se editaron únicamente los textos generados.

## Un inicio de exposición más claro

El botón **Iniciar presentación** vuelve al inicio y solicita pantalla completa desde el clic del usuario. **Continuar aquí** conserva la diapositiva actual. El modo de exposición oculta las barras; las flechas siguen funcionando y **Esc** o **Salir · Esc** permiten volver. Si hay un panel abierto, Esc primero cierra ese panel.

Si la API no existe o rechaza la solicitud, se mantiene un modo inmersivo dentro de la ventana y aparece una instrucción para usar F11 o el menú del navegador. La salida nativa de pantalla completa también restaura el modo normal.

Se conservó el presentador con notas, preguntas, referencias y reloj. La guía explica cómo mover manualmente esa ventana a una segunda pantalla y seleccionar la ventana de diapositivas en la aplicación de reuniones. La página no captura la pantalla del sistema, no coloca ventanas automáticamente en monitores y no administra permisos de videollamada.

## Evidencia que se conservó

`evidence/iteration-2/results/preservation-baseline.json` registra **240 archivos originales** con SHA-256. La validación encontró cero cambios en ellos. Además, se revisó el alcance del diff de Git: los diagramas y experimentos originales siguen intactos y todos los archivos cambiados pertenecen a la presentación.

Se mantienen las capturas auténticas de las cinco vistas, los 16 estados explorados en la primera misión, las fuentes con líneas y los resultados originales: 284 pruebas aprobadas, una integración excluida, cobertura con su alcance, rankings, escenarios y el caso aislado de fechas. **No se volvieron a ejecutar las 284 pruebas ni se recapturó Streamlit en esta iteración.** Los registros anteriores se reutilizan como evidencia histórica verificable, sin cambiar sus fechas ni su autoría.

Permanecen las cifras de la PoC: 30 empresas en el diseño; 12, 17 y 23 conocidas; 28, 54 y 83 observaciones; K = 5; tres sustituciones del Top 5 y Jacaranda del puesto 10 al 3. Los escenarios de +$39,000 y −$41,000 MXN siguen siendo cálculos hipotéticos para 500 plazas, no ventas ni ROI observados. El calculador y el experimento causal conservan funciones distintas.

## Validación nueva, ejecutada de verdad

Resultado: **PASS**, en Chromium sobre Linux, con Playwright y servidor HTTP local. El detalle reproducible está en `evidence/iteration-2/results/presentation-qa.json`; las capturas de esta versión están en `evidence/iteration-2/presentation/`.

| Revisión | Resultado observado |
|---|---|
| 30 diapositivas × 3 tamaños | 90 composiciones revisadas: 1600×1030, 1366×768 y 1920×1080 inmersivo; sin desbordamientos detectados |
| Revisión visual | Se inspeccionaron las 30 capturas, el inicio, el presentador, el aviso alternativo y muestras del PDF |
| Fuentes | 59 enlaces únicos comprobados, incluyendo anclas de línea |
| Notas | Los 30 discursos coinciden con la fuente regenerada; sincronización de ambas ventanas comprobada |
| Inicio y salida | Pantalla completa nativa aceptada; inicio desde primera, continuación, teclado, Esc, botón Salir y salida nativa comprobados |
| Alternativas a fullscreen | Dos fallos **controlados**: API rechazada y API ausente. El modo inmersivo, la instrucción manual y la salida funcionaron; no se atribuyen a rechazos naturales observados |
| Interacciones conservadas | Filtros mantienen #10/#3, escenarios mantienen los resultados y las cinco capturas de la torre se amplían correctamente |
| Consola y recursos | Cero errores de JavaScript y cero solicitudes fallidas registrados |
| Copia independiente | Las 30 diapositivas se recorrieron desde otra copia con el servidor del README, sin paquetes de ejecución ni servidor de Streamlit |
| PDF | Exportación actualizada de 30 páginas, formato 16:9; las notas se consultan por separado |

También se comprobaron la sintaxis de JavaScript, el formato y análisis estático de Python y la limpieza del diff. El registro final está en `evidence/iteration-2/results/final-checks.json`.

## Límites que siguen visibles

- Atlas real continúa pendiente. No se tocaron credenciales, conexiones ni datos remotos.
- No hay conversiones, ventas, margen incremental ni ROI comercial demostrados. Tampoco se ejecutó el experimento causal propuesto.
- Los modelos de ML descritos como opciones futuras no están entrenados ni evaluados.
- La revisión automática se hizo en Linux/Chromium. Las instrucciones de Windows están documentadas; la ejecución nativa en Windows y una exposición física con dos monitores quedan por comprobar.
- El navegador administrado bloqueó `file://`; no se afirma que el doble clic funcione aquí. Sí se comprobó el servidor local y una copia independiente sin dependencias de la app original.
- Los chequeos de diseño no garantizan compatibilidad con todos los navegadores, proyectores o políticas de pantalla completa.
- El caso de fechas es un defecto reproducido con un fixture aislado, conservado de V1. No se aplicó su corrección al motor productivo.

## Cómo revisarla

Desde la raíz del repositorio, en Windows:

```powershell
py -m http.server 8765 --bind 127.0.0.1 --directory presentation-showcase
```

Abre `http://127.0.0.1:8765/`. El README incluye clonación de la subrama, navegación, dos pantallas, generación y reproducción de la validación. No hay despliegue público. El PR se entrega en borrador contra la rama de la primera presentación, sin fusionar ninguna rama.
