'use strict';
const D = window.DECK_DATA;
const slides = D.slides;
const mainCount = slides.filter(s => !s.annex).length;
const $ = (q, root = document) => root.querySelector(q);
const $$ = (q, root = document) => [...root.querySelectorAll(q)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money = v => `${Number(v) < 0 ? '−' : Number(v) > 0 ? '+' : ''}$${Math.abs(Number(v)).toLocaleString('es-MX', {maximumFractionDigits:0})}`;
const ctx = D.context;
const cafe = ctx.ranking.companies.find(c => c.display_name === 'Café Jacaranda');
const code = (name, small = false) => `<pre class="code-block ${small ? 'small-code' : ''}"><code>${D.code[name] || esc(name)}</code></pre>`;
const screenshot = (file, title, extra = '', crop = false) => `<div class="image-shell ${extra}"><div class="image-title"><span>CAPTURA REAL · STREAMLIT OFFLINE</span><span>${esc(title)}</span></div><div class="image-area ${crop ? 'crop' : ''}"><img src="evidence/screenshots/${file}" alt="${esc(title)}" data-zoom="${file}" tabindex="0" role="button" aria-label="Ampliar captura: ${esc(title)}"></div><span class="zoom-tag">Ampliar →</span></div>`;
const checkList = a => `<ul class="check-list">${a.map(t => `<li>${t}</li>`).join('')}</ul>`;
const pills = (values, selected, type) => `<div class="segmented" aria-label="${type}">${values.map(v => `<button data-${type}="${v[0]}" aria-pressed="${v[0] === selected}">${v[1]}</button>`).join('')}</div>`;
const graphSvg = () => `<svg class="cover-network" viewBox="0 0 560 430" role="img" aria-label="Vista explicativa: Café Jacaranda y sus conexiones sintéticas, dos confirmadas">
 <defs><radialGradient id="halo"><stop stop-color="#267c7a" stop-opacity=".28"/><stop offset="1" stop-color="#267c7a" stop-opacity="0"/></radialGradient></defs>
 <circle cx="280" cy="211" r="205" fill="url(#halo)"/><circle cx="280" cy="211" r="150" fill="none" stroke="#294c60" stroke-dasharray="3 8"/><circle cx="280" cy="211" r="202" fill="none" stroke="#1a3a50"/>
 <path d="M280 211 93 120M280 211 429 92" stroke="#50e4c7" stroke-width="3"/><path d="M280 211 463 285M280 211 130 341M280 211 78 245" stroke="#537184" stroke-width="1.4" stroke-dasharray="6 7"/>
 <circle cx="93" cy="120" r="13" fill="#50e4c7"/><circle cx="429" cy="92" r="13" fill="#50e4c7"/><circle cx="463" cy="285" r="9" fill="#496779"/><circle cx="130" cy="341" r="9" fill="#496779"/><circle cx="78" cy="245" r="9" fill="#496779"/>
 <circle cx="280" cy="211" r="34" fill="#103b49" stroke="#50e4c7" stroke-width="2"/><circle cx="280" cy="211" r="9" fill="#50e4c7"/>
 <g fill="#c9e0e2" class="network-label"><text x="93" y="87" text-anchor="middle">Hornos del Centro</text><text x="429" y="59" text-anchor="middle">Enlace Punto POS</text><text x="280" y="267" text-anchor="middle" font-weight="700" fill="#fff">Café Jacaranda</text><text x="463" y="316" text-anchor="middle">Mesa de Barrio</text><text x="130" y="373" text-anchor="middle">Papelería Horizonte</text><text x="80" y="278" text-anchor="middle">Ruta Corta</text></g>
 <text x="280" y="417" text-anchor="middle" fill="#8eacba" font-size="10" letter-spacing="1">VISTA EXPLICATIVA · DATOS SINTÉTICOS T2</text></svg>`;
function architectureSvg() {
 return `<svg class="architecture-svg" viewBox="0 0 1280 375" role="img" aria-label="Flujo real: ledger a load_observations, build_context con ramas snapshot y compare_rankings que tiene su propio snapshot; finanzas con fuente independiente">
 <defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10" fill="none" stroke="#6c8b7b" stroke-width="1.5"/></marker></defs>
 <g fill="none" stroke="#6c8b7b" stroke-width="1.6" marker-end="url(#arr)"><path d="M210 73H260"/><path d="M464 73H514"/><path d="M734 73H790V42H840"/><path d="M790 73V129H840"/><path d="M1040 129H1090"/><path d="M734 73H790V218H840"/><path d="M625 106V270H1128V229"/><path d="M235 321H375"/><path d="M590 321H1037V229"/></g>
 <g fill="#e2eae0" stroke="#bacfc0"><rect x="0" y="40" width="210" height="66" rx="8"/><rect x="260" y="40" width="204" height="66" rx="8"/><rect x="514" y="40" width="220" height="66" rx="8"/></g>
 <g fill="#102b40"><rect x="840" y="10" width="200" height="61" rx="8"/><rect x="840" y="99" width="200" height="61" rx="8"/><rect x="1090" y="99" width="185" height="61" rx="8"/><rect x="840" y="189" width="200" height="59" rx="8"/></g>
 <rect x="1050" y="190" width="225" height="39" rx="8" fill="#007f78"/><rect x="0" y="290" width="235" height="62" rx="8" fill="#e8ddcd"/><rect x="375" y="290" width="215" height="62" rx="8" fill="#e8ddcd"/>
 <g fill="#214836" text-anchor="middle" font-size="15"><text x="105" y="69">observations.json</text><text x="105" y="91" font-size="11">Registro observable</text><text x="362" y="69">load_observations()</text><text x="362" y="91" font-size="11">Lee y valida</text><text x="624" y="69" font-weight="700">build_context()</text><text x="624" y="91" font-size="11">Prepara datos de las vistas</text></g>
 <g fill="#e3f5f2" text-anchor="middle" font-size="15"><text x="940" y="36">snapshot()</text><text x="940" y="57" font-size="11">Conocimiento al corte</text><text x="940" y="125">compare_rankings()</text><text x="940" y="147" font-size="11">Dos políticas, misma cohorte</text><text x="1182" y="125">snapshot()</text><text x="1182" y="146" font-size="11">Llamada interna</text><text x="940" y="214">Evolución</text><text x="940" y="235" font-size="11">snapshot por corte pasado</text><text x="1162" y="215" font-size="13" font-weight="600">Control Tower · filtros al final</text></g>
 <g fill="#714c2d" text-anchor="middle" font-size="14"><text x="118" y="317">financial_assumptions.json</text><text x="118" y="338" font-size="11">Supuestos independientes</text><text x="482" y="317">financial_report()</text><text x="482" y="338" font-size="11">No lee empresas ni rankings</text></g>
 <text x="0" y="20" font-size="10" fill="#64816d" letter-spacing="1.5">RUTA EMPRESARIAL · DATOS OBSERVABLES</text><text x="0" y="276" font-size="10" fill="#916f4c" letter-spacing="1.5">RUTA FINANCIERA · HIPÓTESIS</text></svg>`;
}
function rankLists() {
 const all = ctx.ranking.companies;
 const list = policy => ctx.ranking.top_k[policy].map(id => {
  const c = all.find(c => c.company_id === id);
  const shared = c.baseline_selected && c.graph_selected;
  return `<div class="rank-row ${shared ? 'shared' : policy === 'graph' ? 'entered' : 'left'}"><b>${c[`${policy}_position`]}</b><span>${esc(c.display_name)}</span>${!shared ? `<span class="flag">${policy === 'graph' ? 'Entra' : 'Sale'}</span>` : ''}<span class="rank-score">${c[`${policy}_score`]} pts</span></div>`;
 }).join('');
 return `<div class="rank-comparison"><div><span class="eyebrow">Solo información individual</span><h2 style="margin-top:10px">Baseline</h2><div class="rank-list">${list('baseline')}</div></div><div><span class="eyebrow">También relaciones confirmadas</span><h2 style="margin-top:10px">Con grafo</h2><div class="rank-list">${list('graph')}</div></div><span class="comparison-result">3</span></div>`;
}
const pool = '<div class="pool-dots"><span></span><span></span><span></span><span></span><span></span></div>';
function template(s) {
 switch (s.kind) {
 case 'cover': return `<div class="cover-grid"><div><div class="eyebrow">SME ECONOMIC GRAPH</div><div class="cover-title">ConectaPyME<span style="color:var(--mint)">.</span></div><div class="cover-subtitle">Elegir a quién<br>investigar primero.</div><div class="cover-proof"><strong>3/5</strong><p>cuentas cambian al usar<br>relaciones confirmadas.<br><span class="muted">El valor comercial falta medirlo.</span></p></div></div><div>${graphSvg()}</div></div>`;
 case 'problem': return `<div class="split"><div class="centered"><p class="lead">La pregunta comercial es<br><strong>por dónde empezar.</strong></p><div class="node-field" aria-label="21 empresas elegibles, cinco priorizadas">${Array.from({length:21},(_,i)=>`<span class="business-dot ${i<5?'selected':''}">${i<5?'✓':'·'}</span>`).join('')}</div><p class="small muted">T2: 21 cuentas elegibles en la simulación.<br>La cobertura y el permiso de contacto siguen por validar.</p></div><div class="capacity centered"><span class="eyebrow">Misma capacidad en ambas políticas</span><div class="number">5</div><h2>lugares para investigar</h2><p class="medium muted">¿Qué cambia al agregar relaciones<br>a la información individual?</p></div></div><p class="line-note">Hipótesis de trabajo: mejores señales podrían ayudar a dedicar mejor el esfuerzo comercial.</p>`;
 case 'timeline': return `<div class="timeline">${D.summary.cuts.map((c,i)=>`<div class="time-step"><span class="eyebrow">${c.cut} · ${['15 ENE','15 MAY','15 SEP'][i]} 2026</span><div class="number">${c.companies}</div><p class="medium">empresas conocidas</p><div class="time-bar"><span style="width:${c.companies/30*100}%"></span></div><div class="observation"><strong>${c.observations}</strong><span>observaciones</span></div><span class="tiny muted">${c.relationship_claims} afirmaciones económicas · ${c.referrals} referencias</span></div>`).join('')}</div><div class="knowledge-rule"><code>available_at ≤ fecha de corte</code><span class="small">30 empresas en el diseño.<br><strong>7 aún no conocidas en T2.</strong></span><span class="tiny muted">Cortes: 12:00 UTC / 06:00 CDMX.<br>El diseño privado no completa el ranking.</span></div>`;
 case 'provenance': return `<div class="split wide"><div class="observation-sheet"><div class="eyebrow">Ejemplo real del ledger sintético</div><h2 style="margin-top:10px">Hornos del Centro</h2><div class="row"><span class="mono">OBS-028</span><span>2 sucursales</span><span class="badge">Evidencia conservada</span></div><div class="row"><span class="mono">OBS-047</span><span>3 sucursales</span><span class="badge">Evidencia conservada</span></div><div class="row"><span class="mono">OBS-075</span><span>3 sucursales</span><span class="badge">Evidencia conservada</span></div><div class="conflict-values"><span>2</span><b>≠</b><span>3</span><p class="small" style="margin:0 0 0 12px">Estado: <strong>en conflicto</strong><br>Esta señal aporta 0 puntos.</p></div></div><div class="centered"><h2>No elijo una versión<br>sin una regla válida.</h2><p class="medium muted">Fuente · fechas · estado · historial.</p><div class="grid3" style="grid-template-columns:1fr 1fr"><div class="fact"><div class="number">2</div><p>Atributos en conflicto</p></div><div class="fact"><div class="number">2</div><p>Registros candidatos</p></div></div></div></div><p class="line-note">Un nombre parecido genera un candidato. No demuestra que dos registros sean la misma empresa.</p>`;
 case 'rules': return `<div class="rule-layout"><div class="equation-box"><span class="eyebrow">01 · Baseline</span><div class="formula">10 × sucursales<br>adicionales válidas</div><p>Tope: 5 adicionales.<br>Sin evidencia utilizable: 0 puntos.</p></div><div class="rule-plus">+</div><div class="equation-box"><span class="eyebrow">02 · Señal del grafo</span><div class="formula">5 × vecinos<br>confirmados distintos</div><p>Tope: 4 vecinos.<br>Solo suministro y alianzas utilizables.</p></div></div><div class="grid3"><div><h3>Referencias no puntúan</h3><p class="small muted">Tampoco reportes o inferencias.</p></div><div><h3>Una regla explicable</h3><p class="small muted">No hay modelo predictivo entrenado.</p></div><div><h3>Puntos ≠ probabilidad</h3><p class="small muted">Los pesos aún no están calibrados.</p></div></div>`;
 case 'ranking': return `${rankLists()}<div class="knowledge-rule"><strong>2 cuentas compartidas · 3 sustituciones</strong><span class="small">Mismas 21 elegibles · mismo corte T2 · K = 5</span></div><p class="tiny muted" style="margin:0">Orden determinista por puntos e ID público. Los empates se declaran; no prueban mayor valor comercial.</p>`;
 case 'cafe': return `<div class="split narrow"><div class="centered"><span class="eyebrow">Posiciones globales en T2</span><div class="cafe-score"><div><div class="number">10</div><span class="label">Baseline · 0 pts</span></div><span class="arrow">→</span><div><div class="number accent">3</div><span class="label">Con grafo · 10 pts</span></div></div><div class="calc"><strong>2</strong><span>vecinos × 5 puntos = <b>10</b></span></div><p class="small muted">Hornos del Centro + Enlace Punto POS</p><div><span class="source-chip">OBS-026 · CRM</span><span class="source-chip">OBS-063 · CRM</span></div></div><div class="centered">${screenshot('02-graph-cafe-chart.png','Café Jacaranda · T2','graph-image')}<p class="image-caption">Líneas gruesas: respaldo confirmado. El resto da contexto.</p></div></div><p class="line-note">El gráfico muestra evidencia; no calcula el score ni representa intención de compra.</p>`;
 case 'architecture': return `${architectureSvg()}<div class="diagram-note"><span><strong>El ranking se calcula completo.</strong> Los filtros vienen después.</span><span class="tiny muted">MongoDB: alternativa de lectura.<br>Atlas real pendiente en esta misión.</span></div>`;
 case 'filters': return `<div class="split wide"><div class="reconstruction"><div class="interactive-label">Reconstrucción con resultados congelados del código</div><div style="margin-top:15px">${pills([['all','Todas'],['industry','Restaurantes y cafeterías'],['cafe','Solo Jacaranda']],'all','filter')}</div><div id="filter-table"></div><div class="rank-fixed"><span>Café Jacaranda<br><b>Posición general con grafo</b></span><strong id="fixed-position">#3</strong></div><p class="filter-state" id="filter-state"></p></div><div class="centered"><h2>Una fila visible<br>puede seguir en #3.</h2><p class="medium muted">Primero: ranking global.<br>Después: IDs del segmento.<br>Al final: copiar las mismas posiciones.</p><p class="small accent"><strong>El Top 5 no se rellena al filtrar.</strong></p><button class="text-button" data-open-capture="10-ranking-cafe-viewport.png">Ver captura de la app original →</button></div></div>`;
 case 'tower': return `<div><div class="tower-tabs" role="tablist" aria-label="Vistas de Control Tower">${['Resumen','Graph Health','AI Performance','Business Funnel','Economic Impact'].map((n,i)=>`<button role="tab" data-tower="${i}" aria-selected="${i===0}">${n}</button>`).join('')}</div><div class="tower-layout"><div id="tower-image"></div><div id="tower-description" class="tower-description"></div></div></div><p class="line-note">Aplicación original en Chromium · 16 estados capturados · fuente offline · sin acceso remoto a Atlas.</p>`;
 case 'tests': return `<div class="test-count"><div class="number accent">284</div><p><strong>pruebas originales aprobadas.</strong><br><span class="muted">1 integración remota excluida.<br>Ejecutadas por Codex en esta misión.</span></p></div><div class="test-layers"><div class="test-layer"><strong>Funciones</strong><p>Fechas, reglas y aritmética.<br>Resultados reproducibles.</p></div><div class="test-layer"><strong>Dobles de MongoDB</strong><p>Consultas e idempotencia.<br>Sin servidor real.</p></div><div class="test-layer"><strong>AppTest + Chromium</strong><p>Lógica de Streamlit<br>y revisión de pantallas.</p></div><div class="test-layer pending"><strong>Atlas real</strong><p>Pendiente de verificar.<br>No sustituido por dobles.</p></div></div><div class="coverage-strip"><div><strong>95.9%</strong><span>líneas · 904 / 943</span></div><div><strong>91.4%</strong><span>ramas · 362 / 396</span></div><div class="tiny muted" style="align-self:center">Cobertura: paquete <span class="mono">economic_graph</span>, incluido simulador.<br>No incluye <span class="mono">app/</span> ni <span class="mono">scripts/</span>. No prueba ausencia de errores.</div></div>`;
 case 'debug': return `<div class="split"><div><p class="medium">Mismo instante. Dos formas de escribirlo.</p><div class="debug-date">12:00:00<span>Z</span><br>12:00:00<span>+00:00</span></div><div class="debug-outcomes"><div><span class="eyebrow orange">Vista original</span><strong>Descartada</strong></div><div><span class="eyebrow">Ranking original</span><strong>En conflicto</strong></div></div><p class="tiny muted" style="margin-top:15px">Fixture válido con estados opuestos simultáneos.<br>No aparece en el ledger aprobado, que normaliza las fechas.</p></div><div><span class="eyebrow">Corrección experimental en memoria</span><div style="margin-top:18px">${code('timezone_fixed')}</div><div class="pass-fail"><span class="fail">Original: 2 pruebas fallan</span><span class="pass">Copia: 2 pruebas pasan</span></div><p class="small muted" style="margin-top:21px">Hallazgo y experimento de Codex.<br>El motor y los datos originales siguen intactos.</p></div></div>`;
 case 'funnel': return `<div class="funnel-line"><div class="funnel-step"><span class="eyebrow">Conocimiento</span><div class="number">23</div><p>Empresas conocidas</p></div><span class="funnel-arrow">→</span><div class="funnel-step"><span class="eyebrow">Regla de adquisición</span><div class="number">21</div><p>Elegibles para ranking</p></div><span class="funnel-arrow">→</span><div class="funnel-step"><span class="eyebrow">Capacidad K = 5</span><div class="number accent">5</div><p>Priorizadas</p></div></div><p class="small muted">↳ 2 excluidas por servicio activo confirmado. Son una rama aparte.</p><div class="funnel-stop"><strong>No observado</strong><p>Contactos · oportunidades · activaciones · ventas.<br>No hay eventos para calcular conversión. Faltante no significa cero.</p></div><button class="text-button" data-open-capture="12-business-funnel-viewport.png">Abrir captura real del embudo →</button>`;
 case 'economics': return `<div class="economic-top"><span class="eyebrow">Supuestos educativos no calibrados · MXN en valor presente</span>${pills([['demo','5 plazas'],['hypothetical','500 plazas']],'hypothetical','scope')}</div><div id="economic-cases" class="economic-cases"></div><div id="economic-details" class="economic-equation"></div><p class="line-note">El calculador pregunta “¿qué tendría que pasar?”. El experimento mediría qué pasó realmente.</p>`;
 case 'experiment': return `<div class="experiment-arms"><div class="arm"><span class="eyebrow">Bolsas de control</span><h2>Baseline</h2>${pool}<p>Cinco plazas por bolsa.</p><span class="tiny muted">Misma oferta, esfuerzo y seguimiento.</span></div><div class="randomization">1:1<br><span class="tiny muted">al azar</span></div><div class="arm graph"><span class="eyebrow">Bolsas de tratamiento</span><h2>Con grafo</h2>${pool}<p>Cinco plazas por bolsa.</p><span class="tiny muted">Reducir cruces entre cuentas y equipos.</span></div></div><div class="experiment-kpi">Margen neto por <span class="accent">toda cuenta elegible asignada.</span></div><div class="grid3"><p class="small muted"><strong>90 días</strong> para activar.<br><strong>12 meses</strong> desde asignación.</p><p class="small muted"><strong>Falta:</strong> varianza, correlación dentro<br>de bolsas y unidades suficientes.</p><p class="small muted"><strong>Sin muestra calculada.</strong><br>El protocolo aún no se ejecuta.</p></div>`;
 case 'closing': return `<div class="closing-title">El ranking <span>cambia.</span><br>El valor falta medirlo.</div><div class="close-columns"><div><span class="eyebrow">Puedo demostrar</span><p style="margin-top:16px">Cortes y procedencia · reglas explicables.<br>Tres sustituciones · posiciones consistentes.<br>Control Tower offline · pruebas reproducidas.</p></div><div><span class="eyebrow" style="color:var(--orange)">Todavía falta</span><p style="margin-top:16px">Resultados comerciales y costos reales.<br>Atlas en esta misión · escala y producción.<br>Un experimento válido y práctica personal del código.</p></div></div><div class="annex-link"><span>La siguiente decisión: validar datos, permisos y viabilidad del experimento.</span><button data-goto="a-flujo">Explorar anexo técnico →</button></div>`;
 case 'calltree': return `<div class="split wide"><div class="calltree">build_context(rows, cut)
├── <em>snapshot(rows, cut)</em> → view
├── <em>compare_rankings(rows, cut)</em>
│   └── snapshot(rows, cut)
├── summarize(view) → summary
└── evolución de cortes pasados
    ├── snapshot(rows, T0)
    ├── snapshot(rows, T1)
    └── snapshot(rows, T2)</div><div class="centered"><div class="number accent">5</div><h2>llamadas a snapshot en T2</h2><p class="medium muted">La primera vista no se pasa<br>como entrada al ranking.</p><p class="small muted">Los filtros no entran a esta función.<br>No hay benchmark de escala.</p></div></div>`;
 case 'data-detail': return `<div class="split"><div><div class="data-schema">${[['observation_id','Identidad de la evidencia'],['subject_id / value','Qué entidad y qué se afirma'],['source_type / source_record_id','De dónde viene'],['observed_at','Cuándo ocurrió o se observó'],['recorded_at','Cuándo se registró'],['available_at','Desde cuándo puedo usarlo']].map(a=>`<div><code>${a[0]}</code><span class="tiny muted">${a[1]}</span></div>`).join('')}</div><p class="small rule" style="margin-top:22px">Fecha del hecho ≤ registro ≤ disponibilidad.<br>Zona horaria explícita e IDs públicos estables.</p></div><div>${checkList(['Sin campos privados del simulador.','Sin extremos de relaciones desconocidos.','Valores distintos: conservar conflicto.','Nombres parecidos: candidatos, sin fusión.'])}<p class="small muted" style="margin-top:20px">El universo de 30 es del diseño.<br>La ruta comercial solo usa el ledger público.</p></div></div>`;
 case 'policy-detail': return `<div class="split"><div><span class="eyebrow">Elegibilidad de la PoC</span><h2 style="margin-top:16px">Excluir solo servicio activo<br>confirmado sin conflicto.</h2><p class="medium muted">Desconocido sigue “por validar”.<br>No demuestra que sea un prospecto listo.</p><div class="study-metrics" style="grid-template-columns:1fr 1fr"><div><strong>3/21</strong><span>Cobertura individual</span></div><div><strong>5/21</strong><span>Señal relacional utilizable</span></div></div></div><div>${checkList(['Puntos descendentes; ID público ascendente.','Reportar empates en la frontera del Top 5.','Sucursales adicionales: tope 5. Vecinos: tope 4.','Deduplicar vecinos, no borrar evidencias.'])}<p class="small muted" style="margin-top:20px">La baja cobertura produce empates.<br>Desempatar por ID no agrega valor comercial.</p></div></div>`;
 case 'doubles': return `<div class="split"><div>${code('memory',true)}</div><div><span class="eyebrow">Solo operaciones usadas por el código</span><h2 style="margin-top:16px">Diccionarios, copias<br>y consultas registradas.</h2><div class="proof-steps"><div><strong>83</strong><span>primera carga en memoria</span></div><b>→</b><div><strong>0</strong><span>nuevas al repetir</span></div></div><p class="medium muted">Protege base, propiedad de colecciones<br>y documentos existentes.</p><p class="small orange">No prueba red, permisos, índices reales<br>ni concurrencia de MongoDB.</p></div></div>`;
 case 'apptest': return `<div class="split"><div>${code('apptest',true)}<p class="small muted" style="margin-top:20px">Offline bloquea configuración y cliente MongoDB.<br>Los controles cambian resultados verificables.</p></div><div class="stack"><div class="fact"><h2>AppTest</h2><p class="medium">Métricas · tablas · opciones · errores.<br><span class="muted">Sin renderizar el navegador.</span></p></div><div class="fact"><h2>Chromium real</h2><p class="medium">Filtros · gráficos · apariencia visible.<br><span class="muted">Capturas auténticas en Linux.</span></p></div><p class="small muted">Ninguno acredita por sí solo escala,<br>seguridad integral o ejecución nativa Windows.</p></div></div>`;
 case 'atlas': return `<div class="atlas-steps"><div><strong>01 · Referencia local</strong><p>Construye contexto<br>del ledger aprobado.</p></div><div><strong>02 · Base dedicada</strong><p>Valida configuración<br>sin mostrar secretos.</p></div><div><strong>03 · Leer al corte</strong><p>Consulta available_at.<br>Reconstruye contexto.</p></div><div><strong>04 · Comparar huella</strong><p>SHA-256 distinto:<br>bloquea la demo comparable.</p></div></div><div class="pending-box"><p><strong>Sin conexión remota en esta misión.</strong><br>Configuración y red pendientes. Se decidió continuar offline.</p></div><p class="medium muted">atlas_context() no hace ping ni carga datos.<br>La integración histórica que sí carga quedó excluida. Sin respaldo silencioso.</p>`;
 case 'finance-detail': return `<div class="split wide"><div class="math-lines">ΔV = plazas × Δp × margen
     − plazas × Δc + ΔU − F − ΔO

Base 500:    80,000 − 25,000
             − 10,000 − 6,000 = <strong>+39,000</strong>
Nulo 500:         0 − 25,000
             − 10,000 − 6,000 = <strong>−41,000</strong>

Reserva aparte: 20% × 16,000 = 3,200
Base después de reserva: <strong>+35,800 MXN</strong></div><div class="centered"><h2>Δp = 2 pp<br><span class="muted">10% → 12% supuesto</span></h2><p class="medium">Margen: $8,000 por activación.<br>Costo adicional: $50 por plaza.</p><div class="fact"><h3>Equilibrio base · 500 plazas</h3><p><b class="accent">1.025 pp</b> sin reserva<br><b class="accent">1.105 pp</b> con reserva</p></div><p class="small muted">Importes ya en valor presente.<br>12 meses · descuento mensual 1%.</p></div></div>`;
 case 'causal-detail': return `<div class="split"><div><span class="eyebrow">Intención de tratar (ITT)</span><h2 style="margin-top:20px">Conservar a todas las<br>elegibles asignadas.</h2><p class="medium muted">Seleccionadas y no seleccionadas.<br>Contactadas y no contactadas.<br>Incumplimientos y cruces registrados.</p><div class="knowledge-rule" style="display:block;margin-top:25px"><strong>Faltante ≠ cero</strong><p class="small" style="margin:10px 0 0">Si no puedo verificar el resultado,<br>no invento ausencia de venta.</p></div></div><div>${checkList(['Asignar bolsas completas antes de seleccionar.','Respetar bolsas y bloques en el análisis.','Medir contaminación y resultados por otros canales.','No fijar muestra sin varianza, ICC y unidades suficientes.'])}<p class="small muted" style="margin-top:20px">Objetivos propuestos: IC 95% y potencia 80%.<br>No son precisión ni potencia alcanzadas.</p></div></div>`;
 case 'change-detail': return `<div class="split"><div><span class="eyebrow">Antes · comparar texto</span><div style="margin:18px 0 25px">${code('timezone_original')}</div><span class="eyebrow">Después · comparar instantes</span><div style="margin-top:18px">${code('timezone_fixed')}</div></div><div><h2>Experimento preparado por Codex.</h2>${checkList(['Fixture aislado; observaciones originales intactas.','Dos pruebas rojas en original.','Dos pruebas verdes en copia en memoria.','Motor original sin modificación.'])}<p class="small orange" style="margin-top:20px">Mi práctica pendiente: reproducirlo, explicar la causa<br>y modificar una copia por mi cuenta.</p></div></div>`;
 case 'roadmap': return `<div class="roadmap"><div><div class="step">01</div><h2>Datos confiables</h2><p>Identidad, cobertura y permisos.<br>Activaciones y márgenes reales.<br>Costos con fuentes verificables.</p></div><div><div class="step">02</div><h2>Evaluación válida</h2><p>Baseline comercial real.<br>Bolsas y capacidad comparables.<br>Seguimiento y análisis definidos.</p></div><div><div class="step">03</div><h2>Medir antes de crecer</h2><p>Benchmark aislado.<br>Más datos antes de entrenar ML.<br>Comparar modelos contra reglas.</p></div></div><p class="line-note">Sin ML entrenado, MLOps o rendimiento probado a 1,000 / 10,000 / 50,000 empresas. MongoDB no es la única opción.</p>`;
 case 'map': return `<div class="map-grid">${[['01','Business Framing','Problema y capacidad fija','problema'],['02','Economic Graph','Observaciones, tiempo y conflictos','tiempo'],['03','AI/ML Approach','Reglas, baseline y límites','reglas'],['04','Architecture','Entradas, funciones y dependencias','arquitectura'],['05','Economic Case','Supuestos y validación futura','economia'],['06','Control Tower','Cinco vistas en ejecución','torre']].map(a=>`<div class="map-item"><span>${a[0]}</span><strong>${a[1]}</strong><p>${a[2]}</p><button class="text-button" data-goto="${a[3]}">Ir a la evidencia →</button></div>`).join('')}</div><div class="resources"><a href="docs/guia-estudio.html" target="_blank" rel="noopener">Guion y preguntas →</a><a href="docs/auditoria.html" target="_blank" rel="noopener">Auditoría →</a><a href="docs/trazabilidad.csv" download>Matriz CSV ↓</a><a href="evidence/screenshots/manifest.json" target="_blank" rel="noopener">Capturas y parámetros →</a><a href="README.md" target="_blank" rel="noopener">Cómo ejecutar →</a></div>`;
 default: return '';
 }
}

const darkKinds = ['cover','problem','rules','tests','economics','closing','calltree','atlas','map'];
$('#stage').innerHTML = slides.map((s,i) => `<section class="slide ${darkKinds.includes(s.kind)?'dark':''} ${s.kind==='debug'?'warm':''}" id="slide-${s.id}" data-index="${i}" aria-label="${i+1}. ${esc(s.title)}" aria-hidden="true"><div class="slide-head"><span>${esc(s.chapter)}</span><span class="status-pill">${esc(s.status)}</span></div>${s.kind!=='cover' && s.kind!=='closing' ? `<h1>${esc(s.title)}</h1>` : ''}<div class="slide-content">${template(s)}</div><div class="slide-foot"><span>ConectaPyME / ${s.annex?'Anexo técnico':'Defensa con evidencia'} · Fuente ${D.sourceCommit.slice(0,7)} · Offline</span><button data-evidence="${i}">Fuentes, reproducción y límites →</button><span>${s.annex?'A'+String(i-mainCount+1).padStart(2,'0'):String(i+1).padStart(2,'0')}</span></div></section>`).join('');
// Small links retain the presentation's visual language without being navigation chrome.
const extraStyle = document.createElement('style');
extraStyle.textContent = '.text-button{background:none;color:var(--teal);font-size:13px;text-align:left;text-decoration:underline;text-underline-offset:5px;padding:7px 0;align-self:flex-start}.dark .text-button{color:var(--mint)}';
document.head.append(extraStyle);

function setFilter(filter) {
 const selected = filter==='all' ? ctx.ranking.companies : filter==='industry' ? ctx.ranking.companies.filter(c => D.industryIds.includes(c.company_id)) : [cafe];
 // Display at most five rows to keep the slide readable; all counts remain explicit.
 const shown = filter==='all' ? [ctx.ranking.companies[0],ctx.ranking.companies[1],cafe] : selected;
 $('#filter-table').innerHTML = `<table class="ranking-mini"><thead><tr><th>Empresa</th><th>Baseline global</th><th>Grafo global</th></tr></thead><tbody>${shown.map(c=>`<tr class="${c.company_id===cafe.company_id?'highlight':''}"><td>${esc(c.display_name)}</td><td>#${c.baseline_position}</td><td>#${c.graph_position}</td></tr>`).join('')}</tbody></table>`;
 $('#filter-state').textContent = `${selected.length} elegibles en el segmento.${filter==='all'?' Se muestran tres filas para explicar el caso.':''} Posiciones copiadas del ranking completo.`;
 $$('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===filter)));
}
const towerViews = [
 ['01-resumen-t2-viewport.png','23 → 21 → 5','Resumen','Empresas conocidas, elegibles y priorizadas. El cambio de selección aparece separado de los escenarios económicos.'],
 ['02-graph-cafe-viewport.png','83','Graph Health','Observaciones en T2. Red focal, historial, dos conflictos y dos registros candidatos sin fusión.'],
 ['07-ai-global-viewport.png','3 cambios','AI Performance','Compara reglas explicables. Conserva puntos, posiciones y Top 5 globales al filtrar.'],
 ['12-business-funnel-viewport.png','No observado','Business Funnel','Las etapas posteriores a priorizar no tienen eventos. No se convierten en ceros ni ventas simuladas.'],
 ['15-economic-500-viewport.png','Hipótesis','Economic Impact','Cuatro escenarios, escala y sensibilidad. Los supuestos no están calibrados con ventas reales.']
];
function setTower(i) {
 const v=towerViews[i];
 $('#tower-image').innerHTML = screenshot(v[0],v[2]);
 $('#tower-description').innerHTML=`<span class="eyebrow">${v[2]}</span><div class="number" style="font-size:${i===3?'40':'60'}px;margin:20px 0">${v[1]}</div><p class="medium muted">${v[3]}</p><p class="tiny muted">Captura auténtica · ${D.captureDate}<br>Fuente ${D.sourceCommit.slice(0,7)} · Offline</p>`;
 $$('[data-tower]').forEach(b=>b.setAttribute('aria-selected',String(Number(b.dataset.tower)===Number(i))));
}
function setScope(scope) {
 const names={conservative:'Conservador',base:'Base',optimistic:'Optimista',null:'Nulo'};
 const rows=D.summary.finance.filter(r=>r.scope===scope);
 $('#economic-cases').innerHTML=rows.map(r=>`<div class="economic-case"><h3>${names[r.scenario]}</h3><div class="amount ${Number(r.net_present_value_mxn)<0?'negative':''}">${money(r.net_present_value_mxn)}</div><p>Saldo antes de reserva · MXN</p><p>Δ activación: ${Number(r.activation_rate_increment)*100} pp<br>Reserva: $${Number(r.reserve_mxn).toLocaleString('es-MX')}<br>Tras reserva: ${money(r.net_after_reserve_mxn)}</p></div>`).join('');
 const base=rows.find(r=>r.scenario==='base');
 $('#economic-details').innerHTML=`<div><span class="eyebrow">Equilibrio del supuesto base</span><div class="number" style="margin-top:12px">${base.break_even.delta_pp} <small>pp</small></div><p>Mejora necesaria, no conseguida.</p></div><div style="padding-top:15px"><code>${scope==='hypothetical'?'500 × 0.02 × $8,000 = $80,000':'5 × 0.02 × $8,000 = $800'}<br>− costo comercial adicional − costos fijos y operación</code><p style="margin-top:13px">90 días para activar · horizonte 12 meses · reserva separada.</p></div>`;
 $$('[data-scope]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scope===scope)));
}
setFilter('all');setTower(0);setScope('hypothetical');
let index = Math.max(0,slides.findIndex(s=>s.id===location.hash.slice(1)));
const params = new URLSearchParams(location.search);
const isPresenter = params.has('presenter');
const isPreview = params.has('preview');
if(isPreview) document.body.classList.add('preview-only');
let channel;
try { channel = new BroadcastChannel('conectapyme-evidence-deck'); } catch { /* URL hash navigation works without this optional API. */ }
function resize() {
 const box=$('#viewport');
 const scale=Math.min(box.clientWidth/1440,box.clientHeight/810);
 document.documentElement.style.setProperty('--stage-scale',String(scale));
}
function goto(value, broadcast=true) {
 const n=typeof value==='string'?slides.findIndex(s=>s.id===value):value;
 if(n<0||n>=slides.length)return;
 index=n;
 $$('.slide').forEach((el,i)=>{el.classList.toggle('active',i===n);el.setAttribute('aria-hidden',String(i!==n));el.inert=i!==n;});
 // Printing restores every slide regardless of the current presentation state.
 history.replaceState(null,'','#'+slides[index].id);
 const s=slides[index];
 $('#counter').textContent=s.annex?`A${String(index-mainCount+1).padStart(2,'0')} / ${slides.length-mainCount}`:`${String(index+1).padStart(2,'0')} / ${mainCount}`;
 $('#nav-section').textContent=s.annex?'Anexo técnico · '+s.chapter.split('·')[0].trim():'Presentación principal';
 $('#progress').style.width=((s.annex?(index-mainCount+1)/(slides.length-mainCount):(index+1)/mainCount)*100)+'%';
 $$('[data-action=prev]').forEach(b=>b.disabled=index===0);
 $$('[data-action=next]').forEach(b=>b.disabled=index===slides.length-1);
 $('#status').textContent=s.title;
 if(isPresenter)renderPresenter();
 if(broadcast && channel)channel.postMessage({type:'slide',index,source:isPresenter?'presenter':'deck'});
 resize();
}
window.addEventListener('resize',resize);
window.addEventListener('hashchange',()=>goto(location.hash.slice(1)));
if(channel)channel.onmessage=e=>{if(e.data.type==='slide'&&!isPreview)goto(e.data.index,false);};
function openPanel(title,body) {$('#overlay-title').textContent=title;$('#overlay-body').innerHTML=body;$('#overlay').showModal();}
function openIndex() {
 const grid = list => `<div class="index-grid">${list.map(s=>{const i=slides.indexOf(s);return `<button data-goto="${s.id}" class="${i===index?'current':''}"><span>${s.annex?'A'+String(i-mainCount+1).padStart(2,'0'):String(i+1).padStart(2,'0')}</span>${esc(s.title)}</button>`;}).join('')}</div>`;
 openPanel('Elige dónde continuar',`<p>Principal: 16 diapositivas · aproximadamente 14–18 minutos. Anexo: consulta por preguntas.</p><h3>Presentación principal</h3>${grid(slides.filter(s=>!s.annex))}<h3>Anexo técnico</h3>${grid(slides.filter(s=>s.annex))}`);
}
function notesHtml(s) {
 const words=s.speech.split(/\s+/).length;
 return `<p class="tiny muted">${words} palabras · ~${Math.round(words/140*60)} segundos a 140 palabras/minuto. Ajusta el ritmo al ensayar.</p><p class="note-speech">${esc(s.speech)}</p><h3>Qué señalar</h3><p>${esc(s.point)}</p><h3>Pregunta posible</h3><p><strong>${esc(s.question)}</strong></p><div class="answer-box">${esc(s.answer)}</div><h3>Si profundizan</h3><p>${esc(s.deep)}</p><p class="warning-text">${esc(s.warning)}</p>`;
}
function openNotes(){openPanel(slides[index].title,notesHtml(slides[index]));}
function sourceLinks(s) {
 return `<ul class="source-links">${s.sources.map(r=>`<li><a href="${r.url}" target="_blank" rel="noopener">${esc(r.path)}${r.start?':'+r.start+'–'+r.end:''} →</a><small>${esc(r.symbol||'Documento de referencia')} · ${r.original?'Fuente '+D.sourceCommit.slice(0,7):'Creado por Codex en esta misión'}</small></li>`).join('')}</ul>`;
}
function openEvidence(n=index) {
 const s=slides[n];const capture=D.captures.find(c=>c.id===s.capture);
 openPanel('Evidencia · '+s.title,`<p class="tiny muted">Implementación auditada: ${D.sourceCommit}<br>Auditoría nueva de Codex · fuente principal offline · datos sintéticos.</p><table class="claim-table"><thead><tr><th>Afirmación</th><th>Tipo</th></tr></thead><tbody>${s.claims.map(c=>`<tr><td>${esc(c[0])}</td><td>${esc(c[1])}</td></tr>`).join('')}</tbody></table><h3>Verificar en código o documento</h3>${sourceLinks(s)}<h3>Reproducción</h3><pre class="code-path">${esc(s.command)}</pre>${capture?`<h3>Captura auténtica</h3><div class="evidence-images"><img src="evidence/${capture.file}" data-zoom="${capture.file.replace('screenshots/','')}" alt="${esc(capture.screen)}"></div><p class="tiny muted">${esc(capture.captured_at)} · ${esc(capture.mode)} · corte ${esc(capture.cut)}<br>Parámetros: ${esc(JSON.stringify(capture.parameters))}<br>${esc(capture.demonstrates)}</p>`:''}<h3>Límite de esta evidencia</h3><p class="warning-text">${esc(s.warning)}</p><div class="resources" style="color:var(--teal)"><a style="color:inherit" href="docs/trazabilidad.csv" download>Matriz completa ↓</a><a style="color:inherit" href="docs/guia-estudio.html" target="_blank" rel="noopener">Guion y defensa →</a><a style="color:inherit" href="evidence/results/pytest.txt" target="_blank" rel="noopener">Resultado de pruebas →</a></div>`);
}
function zoom(file) {
 if($('#overlay').open)$('#overlay').close();
 const viewer=$('#image-viewer');const entry=D.captures.find(c=>file.startsWith(c.id));
 $('img',viewer).src='evidence/screenshots/'+file;
 $('p',viewer).textContent=entry?`${entry.screen} · ${entry.captured_at} · Offline · ${entry.cut} · fuente ${entry.source_commit.slice(0,7)}. ${entry.demonstrates} ${entry.limitations}`:'Captura auténtica de la Control Tower offline · corte T2 · '+D.sourceCommit.slice(0,7);
 viewer.hidden=false;$('button',viewer).focus();
}
let presenterFrame;
function renderPresenter(){
 const s=slides[index];
 const host=$('#presenter-view');
 if(!presenterFrame){
  host.innerHTML=`<div class="presenter-toolbar"><strong>ConectaPyME · Presentador</strong><span id="presenter-counter"></span><span class="timer" id="timer">00:00</span><div><button data-action="prev">← Anterior</button><button data-action="next">Siguiente →</button><button data-action="timer">Reiniciar reloj</button></div></div><div class="presenter-layout"><div><iframe title="Diapositiva actual" class="presenter-preview"></iframe><p class="small muted" id="presenter-next"></p></div><div class="presenter-notes"></div></div>`;
  presenterFrame=$('iframe',host);
 }
 presenterFrame.src='index.html?preview=1#'+s.id;
 $('#presenter-counter').textContent=`${index+1} / ${slides.length}`;
 $('#presenter-next').textContent='Siguiente: '+(slides[index+1]?.title||'Fin del anexo');
 $('.presenter-notes').innerHTML=`<h2>${esc(s.title)}</h2>${notesHtml(s)}<h3>Archivo o prueba para verificar</h3>${sourceLinks(s)}`;
}
let started=Date.now();
if(isPresenter){document.body.classList.add('presenter-mode');$('#presenter-view').hidden=false;setInterval(()=>{const t=Math.floor((Date.now()-started)/1000);if($('#timer'))$('#timer').textContent=String(Math.floor(t/60)).padStart(2,'0')+':'+String(t%60).padStart(2,'0');},1000);}
function action(name){
 if(name==='prev')goto(index-1);if(name==='next')goto(index+1);if(name==='index')openIndex();if(name==='notes')openNotes();if(name==='evidence')openEvidence();
 if(name==='presenter'){const url=new URL(location.href);url.search='?presenter=1';window.open(url.href,'conectapyme-presenter','width=1400,height=900');}
 if(name==='fullscreen'){if(!document.fullscreenElement)document.documentElement.requestFullscreen?.().catch(()=>{});else document.exitFullscreen?.();}
 if(name==='timer')started=Date.now();
}
document.addEventListener('click',e=>{
 const t=e.target.closest('button,a,img');if(!t)return;
 if(t.matches('[data-action]'))action(t.dataset.action);
 if(t.matches('[data-goto]')){if($('#overlay').open)$('#overlay').close();goto(t.dataset.goto);}
 if(t.matches('[data-evidence]'))openEvidence(Number(t.dataset.evidence));
 if(t.matches('[data-zoom]'))zoom(t.dataset.zoom);
 if(t.matches('[data-open-capture]'))zoom(t.dataset.openCapture);
 if(t.matches('[data-filter]'))setFilter(t.dataset.filter);
 if(t.matches('[data-tower]'))setTower(Number(t.dataset.tower));
 if(t.matches('[data-scope]'))setScope(t.dataset.scope);
 if(t.matches('.close')){if(t.closest('#image-viewer'))$('#image-viewer').hidden=true;else $('#overlay').close();}
});
document.addEventListener('keydown',e=>{
 if(e.key==='Escape'){if(!$('#image-viewer').hidden){$('#image-viewer').hidden=true;e.preventDefault();}else if($('#overlay').open)$('#overlay').close();return;}
 if(e.target.dataset.zoom && ['Enter',' '].includes(e.key)){e.preventDefault();zoom(e.target.dataset.zoom);return;}
 if(['BUTTON','A'].includes(e.target.tagName)&&['Enter',' '].includes(e.key))return;
 if($('#overlay').open||!$('#image-viewer').hidden||/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)||e.altKey||e.ctrlKey||e.metaKey)return;
 const key=e.key.toLowerCase();
 if(['arrowright','pagedown',' '].includes(key)){e.preventDefault();goto(index+1);}
 if(['arrowleft','pageup'].includes(key)){e.preventDefault();goto(index-1);}
 if(key==='home'){e.preventDefault();goto(0);}if(key==='end'){e.preventDefault();goto(mainCount-1);}
 if(key==='i')openIndex();if(key==='n')openNotes();if(key==='p')action('presenter');if(key==='f')action('fullscreen');if(key==='e')openEvidence();
});
let touchX=0;
$('#viewport').addEventListener('touchstart',e=>{touchX=e.changedTouches[0].clientX;},{passive:true});
$('#viewport').addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-touchX;if(Math.abs(d)>70)goto(index+(d<0?1:-1));},{passive:true});
goto(index,false);
window.addEventListener('beforeprint',()=>{$$('.slide').forEach(el=>{el.inert=false;el.setAttribute('aria-hidden','false');});});
window.addEventListener('afterprint',()=>goto(index,false));
window.DECK_API={goto,setFilter,setScope,setTower,slides};
