# Catálogo de empresas de Distrito Centro — v1.0

**Proyecto:** ConectaPyME Economic Intelligence\
**Misión:** 002A — Diseño del Economic Graph\
**Fecha:** 15 de octubre de 2026\
**Estado:** Catálogo aprobado para misión 002B; verdad sintética restringida, no perfil comercial\
**Naturaleza:** 30 empresas totalmente ficticias; perfiles y tamaños construidos para una simulación, no estimaciones del mercado real.

## 1. Propósito

Especificar **exactamente 30 empresas canónicas** que constituyen el universo privado de Distrito Centro. Este catálogo describe el **mundo sintético**; **no equivale al CRM ni a lo que puede observar la Telco**. Ninguna necesidad, restricción, tamaño, sucursal o madurez digital aquí indicada se convierte automáticamente en un dato disponible para el ranking comercial.

Los sectores mantienen la distribución definida en `docs/06-economic-graph-design.md` (3 panaderías, 2 logística, 7 tecnología, 4 fintech, 8 restaurantes y cafeterías y 6 comercio minorista).

## 2. Reglas de lectura del catálogo

- `EMP-001` a `EMP-030` son identificadores canónicos estables, exclusivos del universo sintético. No son RFC ni IDs públicos.
- `size_truth`, empleados y sucursales son **atributos privados del simulador**. Micro/pequeña/mediana son etiquetas internas operativas de diseño, **no clasificación oficial regulatoria mexicana**.
- `microzone_truth` es una de seis microzonas ficticias dentro de Distrito Centro: Barrio Alameda, Corredor Mercado, Parque Productivo, Plaza Tecnológica, Distrito Oficinas y Terminal Norte. No implica coordenadas reales.
- `connectivity_use_case_truth` describe un posible caso de uso tecnológico, **no intención de compra ni prueba de que la empresa necesite cambiar de proveedor**.
- `commercial_constraint_truth` introduce barreras o contexto de compra que evitan inferir ventas a partir del grado del grafo.
- `seed_crm_t0=1` indica pertenencia **preseleccionada para sembrar 12 entidades conocidas en T0**. No autoriza importar todos sus atributos; los registros CRM se diseñarán por separado y estarán incompletos.
- El presente archivo **no contiene aristas, observaciones, calificaciones/reseñas, eventos comerciales, cobertura de red ni resultados de conversión**; se diseñarán por separado siguiendo reglas de temporalidad y procedencia.

## 3. Distribución sectorial

| Sector | Empresas |
|---|---:|
| Panaderías | 3 |
| Logística | 2 |
| Tecnología | 7 |
| Fintech | 4 |
| Restaurantes y cafeterías | 8 |
| Comercio minorista | 6 |
| **Total** | **30** |

## 4. Catálogo completo

| ID | Empresa ficticia | Sector | Tamaño* | Personal* | Sucursales* | Microzona* | CRM T0 |
|---|---|---|---|---:|---:|---|---|
| EMP-001 | La Espiga del Barrio | Panaderías | Micro | 5 | 1 | Barrio Alameda | Sí |
| EMP-002 | Hornos del Centro | Panaderías | Pequeña | 24 | 3 | Corredor Mercado | Sí |
| EMP-003 | Panificadora Valle Claro | Panaderías | Mediana | 92 | 6 | Parque Productivo | No |
| EMP-004 | Ruta Corta Mensajería | Logística | Micro | 8 | 1 | Terminal Norte | Sí |
| EMP-005 | Carga Urbana del Centro | Logística | Pequeña | 38 | 2 | Parque Productivo | No |
| EMP-006 | Nodo Azul Soporte TI | Tecnología | Micro | 6 | 1 | Plaza Tecnológica | Sí |
| EMP-007 | Bitácora Software | Tecnología | Pequeña | 19 | 1 | Plaza Tecnológica | Sí |
| EMP-008 | Nube Sencilla Sistemas | Tecnología | Micro | 9 | 1 | Barrio Alameda | No |
| EMP-009 | Taller de Datos Centro | Tecnología | Pequeña | 27 | 2 | Distrito Oficinas | No |
| EMP-010 | Enlace Punto POS | Tecnología | Micro | 7 | 1 | Corredor Mercado | Sí |
| EMP-011 | Vector Local Ciberseguridad | Tecnología | Pequeña | 21 | 1 | Distrito Oficinas | No |
| EMP-012 | Mapa Digital Studio | Tecnología | Micro | 5 | 1 | Plaza Tecnológica | No |
| EMP-013 | Cobro Ágil Pagos | Fintech | Pequeña | 31 | 2 | Distrito Oficinas | Sí |
| EMP-014 | Caja Vecina Digital | Fintech | Micro | 8 | 1 | Corredor Mercado | No |
| EMP-015 | Saldo Claro Finanzas | Fintech | Pequeña | 25 | 1 | Distrito Oficinas | No |
| EMP-016 | Fondo Marea Capital | Fintech | Micro | 10 | 1 | Plaza Tecnológica | No |
| EMP-017 | Café Jacaranda | Restaurantes y cafeterías | Micro | 7 | 1 | Barrio Alameda | Sí |
| EMP-018 | Comedor del Andén | Restaurantes y cafeterías | Micro | 9 | 1 | Terminal Norte | Sí |
| EMP-019 | Mesa de Barrio | Restaurantes y cafeterías | Pequeña | 18 | 2 | Barrio Alameda | No |
| EMP-020 | Brasa y Huerto | Restaurantes y cafeterías | Pequeña | 26 | 2 | Corredor Mercado | Sí |
| EMP-021 | Café Estación Nueve | Restaurantes y cafeterías | Micro | 6 | 1 | Terminal Norte | No |
| EMP-022 | Sazón de Patio | Restaurantes y cafeterías | Micro | 11 | 1 | Barrio Alameda | No |
| EMP-023 | Terraza del Reloj | Restaurantes y cafeterías | Pequeña | 23 | 1 | Distrito Oficinas | No |
| EMP-024 | Almuerzo Punto Cero | Restaurantes y cafeterías | Micro | 8 | 1 | Corredor Mercado | No |
| EMP-025 | Papelería Horizonte | Comercio minorista | Micro | 4 | 1 | Barrio Alameda | Sí |
| EMP-026 | Ferretería Cinco Calles | Comercio minorista | Pequeña | 16 | 2 | Corredor Mercado | Sí |
| EMP-027 | Moda Prisma Local | Comercio minorista | Micro | 7 | 1 | Plaza Tecnológica | No |
| EMP-028 | Botica del Parque | Comercio minorista | Pequeña | 14 | 2 | Barrio Alameda | No |
| EMP-029 | Mercado Verde Insumos | Comercio minorista | Pequeña | 20 | 2 | Parque Productivo | No |
| EMP-030 | Bici Centro Taller y Tienda | Comercio minorista | Micro | 6 | 1 | Terminal Norte | No |

*Atributos privados del mundo sintético; no necesariamente observables por ConectaPyME.*

## 5. Perfil operativo individual

Los casos de uso y restricciones siguientes constituyen **verdad sintética de diseño**, no recomendaciones comerciales confirmadas.

### EMP-001 — La Espiga del Barrio
- **Actividad:** Venta en mostrador y encargos.
- **Madurez digital simulada:** Baja.
- **Posible uso de conectividad:** TPV y mensajería comercial.
- **Condicionante comercial:** Presupuesto restringido.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-002 — Hornos del Centro
- **Actividad:** Producción y distribución a puntos de venta.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Sincronización de TPV entre sucursales.
- **Condicionante comercial:** Contratos actuales por sede.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-003 — Panificadora Valle Claro
- **Actividad:** Planta, mayoristas y distribución.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Conectividad de planta y continuidad de ERP.
- **Condicionante comercial:** Proceso de compra formal.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-004 — Ruta Corta Mensajería
- **Actividad:** Última milla en motocicleta.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Despacho y seguimiento móvil.
- **Condicionante comercial:** Alta variación diaria de operaciones.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-005 — Carga Urbana del Centro
- **Actividad:** Almacén y rutas de reparto B2B.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Conexión entre almacén y oficina.
- **Condicionante comercial:** Dependencia de proveedor existente.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-006 — Nodo Azul Soporte TI
- **Actividad:** Soporte y mantenimiento a negocios.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Acceso remoto estable y videollamadas.
- **Condicionante comercial:** Ingresos por proyecto.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-007 — Bitácora Software
- **Actividad:** Desarrollo de software a medida.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Conectividad simétrica y respaldo.
- **Condicionante comercial:** Equipo híbrido.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-008 — Nube Sencilla Sistemas
- **Actividad:** Implementación de herramientas SaaS.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Enlaces confiables para demos.
- **Condicionante comercial:** Presupuesto acotado.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-009 — Taller de Datos Centro
- **Actividad:** Integración y análisis de datos.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Transferencia segura y videocolaboración.
- **Condicionante comercial:** Demanda estacional de proyectos.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-010 — Enlace Punto POS
- **Actividad:** Instalación y soporte de TPV.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Soporte remoto y gestión de tickets.
- **Condicionante comercial:** Dependencia de visitas de campo.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-011 — Vector Local Ciberseguridad
- **Actividad:** Consultoría de seguridad informática.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Baja latencia y redundancia.
- **Condicionante comercial:** Requisitos de seguridad de clientes.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-012 — Mapa Digital Studio
- **Actividad:** Diseño web y marketing digital.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Subida de archivos y trabajo remoto.
- **Condicionante comercial:** Variabilidad de contratos.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-013 — Cobro Ágil Pagos
- **Actividad:** Servicios de aceptación de pagos.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Disponibilidad y canales redundantes.
- **Condicionante comercial:** Cumplimiento y evaluación de proveedores.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-014 — Caja Vecina Digital
- **Actividad:** Herramienta de conciliación para comercios.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Integraciones estables y soporte remoto.
- **Condicionante comercial:** Presupuesto por crecimiento.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-015 — Saldo Claro Finanzas
- **Actividad:** Software financiero para PyMEs.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Acceso seguro y continuidad operativa.
- **Condicionante comercial:** Políticas de compra estrictas.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-016 — Fondo Marea Capital
- **Actividad:** Plataforma de gestión de crédito comercial.
- **Madurez digital simulada:** Alta.
- **Posible uso de conectividad:** Videoconferencia y continuidad de servicio.
- **Condicionante comercial:** Escala operativa reducida.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-017 — Café Jacaranda
- **Actividad:** Cafetería de mostrador.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** TPV y pedidos por aplicaciones.
- **Condicionante comercial:** Sensibilidad a precio.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-018 — Comedor del Andén
- **Actividad:** Comidas corridas y servicio a oficinas.
- **Madurez digital simulada:** Baja.
- **Posible uso de conectividad:** Cobros con terminal y pedidos.
- **Condicionante comercial:** Horarios limitados.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-019 — Mesa de Barrio
- **Actividad:** Restaurante familiar con dos locales.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** TPV, reservas y enlace entre sedes.
- **Condicionante comercial:** Administración familiar.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-020 — Brasa y Huerto
- **Actividad:** Restaurante con reparto propio.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Pedidos, reparto y CCTV.
- **Condicionante comercial:** Estacionalidad de ventas.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-021 — Café Estación Nueve
- **Actividad:** Café para viajeros y empleados.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Wi-Fi visitantes y TPV.
- **Condicionante comercial:** Alta rotación de personal.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-022 — Sazón de Patio
- **Actividad:** Cocina local y servicio a domicilio.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Apps de entrega y mensajería.
- **Condicionante comercial:** Capacidad operativa limitada.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-023 — Terraza del Reloj
- **Actividad:** Restaurante con reservas y eventos.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Reservas, cámaras y Wi-Fi de invitados.
- **Condicionante comercial:** Picos en fines de semana.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-024 — Almuerzo Punto Cero
- **Actividad:** Desayunos y ventas para llevar.
- **Madurez digital simulada:** Baja.
- **Posible uso de conectividad:** TPV y pedidos móviles.
- **Condicionante comercial:** Presupuesto restringido.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-025 — Papelería Horizonte
- **Actividad:** Papelería y copias.
- **Madurez digital simulada:** Baja.
- **Posible uso de conectividad:** Cobros y pedidos a proveedores.
- **Condicionante comercial:** Flujo de caja variable.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-026 — Ferretería Cinco Calles
- **Actividad:** Ferretería y entrega local.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Inventario compartido y TPV.
- **Condicionante comercial:** Sistemas antiguos.
- **Conocimiento al inicio:** Identidad presente en CRM T0, atributos por observar; no copiar el perfil completo.

### EMP-027 — Moda Prisma Local
- **Actividad:** Ropa y ventas por redes.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Catálogo, pagos y publicaciones.
- **Condicionante comercial:** Dependencia de temporadas.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-028 — Botica del Parque
- **Actividad:** Comercio de cuidado personal.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Inventario y terminales.
- **Condicionante comercial:** Normativa y compras planificadas.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-029 — Mercado Verde Insumos
- **Actividad:** Venta de empaques y suministros.
- **Madurez digital simulada:** Media.
- **Posible uso de conectividad:** Inventario y pedidos B2B.
- **Condicionante comercial:** Alto volumen en temporadas.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

### EMP-030 — Bici Centro Taller y Tienda
- **Actividad:** Refacciones y reparación de bicicletas.
- **Madurez digital simulada:** Baja.
- **Posible uso de conectividad:** Citas, TPV y mensajería.
- **Condicionante comercial:** Ventas dependientes del clima.
- **Conocimiento al inicio:** No identificada en el CRM T0; solo el simulador conoce su existencia.

## 6. Selección inicial de 12 empresas CRM (T0)

La selección aprobada incluye seis empresas de servicios/comercio de barrio, algunas de tecnología y una fintech, evitando restringir el CRM únicamente a empresas grandes. La selección **no se basa en la propensión real a comprar ni garantiza resultados favorables a las señales del grafo**.

**IDs seleccionados:** EMP-001, EMP-002, EMP-004, EMP-006, EMP-007, EMP-010, EMP-013, EMP-017, EMP-018, EMP-020, EMP-025, EMP-026.

**Advertencia:** se trata de una lista de *identidades iniciales*, no de 12 perfiles totalmente conocidos. El plan aprobado `09-observability-plan.md` define qué campos conoce el CRM, cuáles provienen de otras fuentes y sus fechas. Solo las observaciones autorizadas `recorded_at <= T0` podrán usarse como features.

## 7. Reglas para conectar posteriormente a las 30 empresas

1. Crear vínculos económicos dirigidos `SUPPLIES_TO` solo cuando exista plausibilidad operacional (por ejemplo, insumos entre comercio y restaurante; servicios tecnológicos a un negocio). Las relaciones verdaderas del simulador pueden ser desconocidas para la Telco.
2. Crear `PARTNERS_WITH` solo para colaboraciones simuladas con sentido empresarial, sin duplicar los extremos por orientación.
3. Crear `REFERS_TO` solo como una **observación de recomendación** con emisor, receptor, fecha y procedencia; no cuenta como evidencia de suministro.
4. Permitir empresas aisladas, vínculos de baja relevancia Telco, relaciones vencidas y referencias equivocadas: **no construir una red donde los nodos más conectados siempre sean mejores prospectos**.
5. Mantener duplicados y alias como registros de origen; no aumentar el universo de 30 empresas canónicas.
6. No asignar a todas las empresas reseñas o ratings; si se simulan, reflejar solo una observación parcial, con procedencia y fecha. Las ratings no deben determinar automáticamente un ranking.
7. Nunca usar la pertenencia a T0 o la identidad canónica privada como etiqueta de resultado comercial o como una proxy de la conversión.

## 8. Seguimiento de decisiones del diseño original

- Establecer fechas concretas T0, T1 y T2.
- Determinar límites de cobertura de red y existencia de competidores/contratos como factores independientes.
- Elegir reglas y cantidades de relaciones verdaderas y referencias reportadas, incluyendo relaciones con negocios fuera de la localidad (si se requiere, representar solo como texto o abstenerse: **no ampliar el universo por accidente**).
- Definir tasas de omisión y error por fuente y resolver cómo simular el CRM T0 incompleto.
- Preparar esquema de observaciones y eventos con la separación técnica entre oráculo y producto.
- Revisar la generación de perfiles frente a las reglas del reto antes de implementar.

## 9. Validaciones de este documento

- Exactamente 30 IDs distintos.
- Conteos por sector: 3 + 2 + 7 + 4 + 8 + 6 = 30.
- Exactamente 12 identidades marcadas para el CRM T0.
- Ninguna empresa representa una persona física real o ubicación real.
- No se presentan probabilidades ni resultados de conversión inventados.
- El catálogo se puede revisar o modificar sin escribir código ni alterar MongoDB.


**Actualización 002B:** las listas de trabajo de 002A se conservan como contexto histórico. Para este alcance están aprobados catálogo, 48 relaciones, 3 afirmaciones falsas, 3 referencias y 83 observaciones. No se crean eventos comerciales ni se resuelven alias sin evidencia. Las rutas `design-data/` citadas en el diseño corresponden ahora a `design-data/restricted/`; el visor usa exclusivamente `data/observable/observations.json`. Véase `10-design-validation.md` para implementación y discrepancias.
