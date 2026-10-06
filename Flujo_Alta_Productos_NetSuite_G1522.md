# Flujo de trabajo para alta de productos en NetSuite

Procedimiento único de alta de productos bajo el Estándar de catálogo G1522.

- Empresa: Grupo Quince 22 SA de CV
- Instancia: NetSuite `7913364` (producción) · sandbox `7913364-sb1` para pruebas de importación
- Estándar de referencia: Estándar de producto G1522 (25 campos) y su Guía de llenado
- Fecha del documento: 22 de septiembre de 2026 · versión 1.0
- Método de carga estándar: Asistente de importación CSV (Configuración → Importar/Exportar → Importar registros CSV → Artículos). El alta manual queda para 1 a 3 productos.

Documentos que acompañan a este procedimiento:

| Documento | Para qué |
|---|---|
| `Flujo_Alta_Productos_NetSuite_G1522.svg` | Diagrama del flujo, con las fronteras y el detalle de las dos pasadas (padre → hijos) |
| `Validador_Carga_NetSuite_G1522.xlsx` | Valida el archivo antes de cargarlo y arma los dos CSV de importación (padres e hijos). **Por construir**, con la misma lógica del validador de Odoo (ver 7.2) |
| `Flujo_Alta_Productos_Odoo_G1522.md` | Alta en Odoo. Está **aguas abajo** de este flujo: Odoo recibe lo que NetSuite ya tiene |
| `Control_Datos_Shopify_WB.md` | Catálogo Shopify WB. También aguas abajo: se alimenta del export "Productos Catalogo Estandar" de NetSuite |

---

## 1. Resumen ejecutivo

**Qué se entrega.** Un procedimiento único para dar de alta productos en NetSuite, con el mapeo de los 25 campos del Estándar G1522 a los campos reales de la instancia, la ruta de importación CSV en dos pasadas (padre y subartículos), la ruta manual, y los controles antes y después de cada carga.

**Por qué este flujo va primero.** NetSuite es la **fuente de verdad** del grupo. El flujo de Odoo y el procedimiento de Shopify WB ya lo dicen: *cuando NetSuite y el archivo del proveedor difieren, gana NetSuite*. Eso solo funciona si lo que entra a NetSuite entra limpio. Un error aquí se replica en Odoo, en Shopify, en el POS y en la plataforma B2B.

**Lo que se verificó en la instancia (22-sep-2026).**

| Hallazgo | Detalle |
|---|---|
| Los campos del estándar ya existen | Subpestaña **WB Atributos** de la ficha de artículo: 18 campos `custitem70` a `custitem87` |
| Modelo de producto | **Padre + subartículos** (campo *Subartículo de*), no artículos de matriz. El padre es el estilo; cada hijo es una talla con su UPC |
| Convención de nombre | Hijo: *Nombre/número del artículo* = **UPC**. Padre: `<No. Estilo> : <nombre corto del proveedor>` (p. ej. `10063824 : YTH BOOKER CHELSEA DSTSD BRN`) |
| Precios | Nivel **Base Price** + niveles calculados: **MAYOREO −42%** y **RETAIL +16%** ya configurados. Coincide exacto con la guía G1522 |
| Listas cerradas | División (4), Género (5) y Color (13) coinciden con el estándar. Categoría tiene **42** valores contra 39 del estándar. Marca tiene 15 valores, con dos errores de captura |
| Campos de texto libre | **Temporada, Lifecycle y País de origen** son texto libre. NetSuite acepta cualquier cosa ahí; solo el validador los protege |
| Campos que se duplican | Coexisten los campos viejos de *Atributos del Producto* (`CATEGORY` con 94 valores, `GENDER` con `JOVEN`, `CLASS`, `LINE`, `SIZE`…) con los WB. Mismo hecho, dos lugares |
| Pendiente confirmado | El estilo `10063824` (Booker Chelsea juvenil) tiene **WB Talla = 0**; la talla real solo está en WB Talla US (`8 M`). Es el caso que ya bloqueaba el alta en Shopify |
| Unidades | Padre en `Pieza`, hijos en `Par` dentro del mismo estilo. No hay regla escrita |

**Lo que este flujo cambia.**

1. Una sola puerta: el archivo del proveedor se normaliza a la plantilla G1522 antes de tocar NetSuite.
2. Validación bloqueante antes de cargar, con énfasis en los tres campos de texto libre que NetSuite no protege.
3. **UPC como Nombre/número del artículo del hijo.** NetSuite exige que ese campo sea único, así que la base rechaza un UPC repetido por sí sola. Es la misma protección que en Odoo da el código de barras.
4. ID externo estable en cada carga, para que reimportar actualice en lugar de duplicar.
5. Primero en sandbox, después en producción.
6. Bitácora de cada lote, que es el acta de entrega para Odoo, Shopify, Compras y Almacén.

**Decisiones que requieren visto bueno.** Ver sección 13.1 (seis decisiones, N1 a N6).

---

## 2. Alcance y fronteras del flujo

### 2.1 Qué cubre

- Alta de estilos nuevos, mono-talla y multi-talla.
- Alta de tallas faltantes en estilos que ya existen.
- Completar campos WB vacíos en artículos existentes (actualización por ID interno).
- Preparación del entorno que el alta necesita (listas, formulario, campos viejos).

### 2.2 Qué no cubre, y dónde entrega

NetSuite está **arriba** de todos los demás sistemas, así que aquí las fronteras son más que en Odoo: todo lo que sale de este flujo alimenta a alguien.

| Frontera | Dónde termina este flujo | Quién recoge | Precondición que este flujo garantiza |
|---|---|---|---|
| **Inventario** | Artículo creado **sin existencias**. Este flujo nunca captura cantidades | Almacén y Compras, por recepción de orden de compra o ajuste | Todo hijo tiene UPC: se recibe con lector |
| **Proveedor y precio de compra** | Queda el **Precio de compra** si el proveedor lo mandó y la moneda está confirmada. No se crean proveedores | Compras, en la subpestaña Proveedores y el maestro de proveedores | WB No. Estilo y UPC capturados: es con lo que el proveedor factura |
| **Odoo (GQ22-WMS)** | NetSuite queda completo bajo el estándar. Este flujo no escribe en Odoo | El flujo `Flujo_Alta_Productos_Odoo_G1522.md` (y la integración NetSuite–Celigo–Odoo cuando opere) | UPC = código de barras de Odoo; WB No. Estilo = `x_studio_no_estilo`; listas con los mismos valores |
| **Shopify (WB, Stetson)** | No se publica nada | `Control_Datos_Shopify_WB.md`, vía el export *Productos Catalogo Estandar* y Matrixify | Los 8 metacampos (`no_estilo`, `categoria`, `division`, `genero`, `temporada`, `lifecycle`, `composicion`, `licencia`) salen poblados y normalizados; Base Price listo para ×1.16 |
| **Precios de cliente** | Queda el Base Price; MAYOREO y RETAIL los calcula NetSuite | Comercial, en niveles especiales (Departamental, CASA, Consignación…) | Base Price mayor a cero |
| **GTIN propio** | Una pieza sin UPC del proveedor **no entra** | Proceso GS1 del grupo | Lista de filas rechazadas por falta de UPC, por estilo |

Regla que amarra todo: **la bitácora del lote (7.7) es el acta de entrega.** Nadie aguas abajo actúa sobre un lote que no esté registrado como cerrado, y un lote se cierra nombrando también las filas rechazadas.

---

## 3. Arquitectura de datos

### 3.1 Padre y subartículos

| Nivel | Registro NetSuite | Qué es | Qué se captura |
|---|---|---|---|
| Estilo | Artículo de inventario **padre** (sin *Subartículo de*) | Agrupa las tallas. No se compra ni se vende directo | Nombre/número, Nombre para mostrar, WB No. Estilo, subsidiaria, tipo de unidades, Clave SAT |
| Talla | Artículo de inventario **hijo** (*Subartículo de* = el padre) | La pieza que se compra, recibe y vende | **Todo el estándar**: UPC, WB Talla, los 18 campos WB, precios, Clave SAT, unidades |

Por qué los campos WB van en el hijo: el export *Productos Catalogo Estandar* que alimenta Shopify es **una fila por UPC**, y el hijo verificado (`197318660764`) ya los trae así. El padre verificado tiene la clasificación vacía.

Regla de oro: **un estilo = un padre; una talla = un hijo con su UPC.**

Estilo mono-talla (gorra, cartera, bolso): **un solo artículo, sin padre** (ver decisión N2). Crear un padre para un hijo único duplica registros sin agrupar nada.

### 3.2 Llaves

| Llave | Campo | Para qué |
|---|---|---|
| UPC | `upccode` (Código UPC) **y** `itemid` del hijo | Identificador único de pieza. Cruce con Odoo (`barcode`), Shopify (SKU y Barcode) y transferencias. Al ser también el `itemid`, NetSuite rechaza el repetido |
| WB No. Estilo | `custitem81` | Llave de agrupación; cruce con el archivo del proveedor |
| ID externo | `externalid` | Llave técnica de importación. Hijo: `g1522.<UPC>`. Padre: `g1522.est_<No. Estilo>` |
| ID interno | `internalid` | Lo asigna NetSuite. Es la llave para actualizar (4.3 del documento Shopify) |

### 3.3 Fuentes

1. **Archivo del proveedor.** Instrucción vigente de dirección. Fuente del dato comercial.
2. **Plantilla estándar G1522** (`Wrangler_CatalogoEstandar_ES2.xlsx` y equivalentes). Una fila por UPC. Único formato que entra.
3. **Hoja Criterios** de la plantilla: listas cerradas y mapa palabra clave → Categoría → División.
4. **NetSuite mismo**, para el cruce: lo que ya existe no se vuelve a crear.

---

## 4. Diccionario de campos: Estándar G1522 → NetSuite

Verificado contra *Personalización → Campos de artículo* y la ficha de artículo de inventario el 22-sep-2026.

| # | Campo del estándar | Campo NetSuite (ID) | Nivel | Tipo | Regla de captura |
|---|---|---|---|---|---|
| 1 | No. Estilo | WB No. Estilo `custitem81` | Padre e hijo | Texto | Tal cual el proveedor. En el padre también forma el nombre |
| 2 | Talla | WB Talla `custitem82` · WB Talla US `custitem86` | Hijo | Texto | WB Talla en **MX estándar** (5.3), nunca `0` ni vacío. Talla US solo como referencia |
| 3 | SKU | WB SKU `custitem87` | Hijo | Texto | SKU del estándar. Si el proveedor no manda uno distinto, = UPC (igual que en Shopify) |
| 4 | Código de barras | Código UPC `upccode` + Nombre/número `itemid` | Hijo | Texto | UPC/GTIN completo, con ceros. Como texto en Excel y en el CSV |
| 5 | Marca | WB Marca `custitem73` | Hijo | Lista *WB Brand* | Solo valores de la lista (6.2) |
| 6 | Nombre | WB Descripcion `custitem83` | Hijo | Texto | `Tipo + Marca + Modelo + Color`. Ej. verificado: `Bota Ariat Booker Chelsea Western Cafe`. La etiqueta dice "Descripcion" pero guarda el Nombre del estándar |
| 7 | Descripción | Descripción de ventas `salesdescription` | Hijo | Texto | Una línea comercial |
| 8 | División | WB Division `custitem70` | Hijo | Lista *Division* | Accesorios, Ropa, Denim, Calzado |
| 9 | Género | WB Genero `custitem71` | Hijo | Lista *Genero* | Hombre, Mujer, Niño, Niña, Unisex |
| 10 | Categoría | WB Categoria `custitem72` | Hijo | Lista *Categoria* | Valor **plano** (`Gorras`, no `Accesorios / Gorras`). Debe ser consistente con División por el mapa de Criterios |
| 11 | Temporada | WB Temporada `custitem75` | Hijo | **Texto libre** | SS26, FW26, SS27, FW27, SS28, FW28. Mayúsculas, sin espacios |
| 12 | Licencia | WB Licencia `custitem80` | Hijo | Lista *WB Brand* | Igual a la marca salvo licenciado (`Yellowstone`) |
| 13 | Composición | WB Composicion `custitem84` | Hijo | Texto | Como lo declara el proveedor |
| 14 | Color | WB Color `custitem74` | Hijo | Lista *Color* | 13 valores del estándar. Nombre comercial del color va en el Nombre |
| 15 | Fit | WB Fit `custitem78` | Hijo | Texto | Solo denim y ropa |
| 16 | Silueta | WB Silueta `custitem77` | Hijo | Texto | Ej. `Estructurada de 5 paneles` |
| 17 | Lifecycle | WB Lifecycle `custitem76` | Hijo | **Texto libre** | `Seasonal` o `CORE`, exactamente así |
| 18 | Descripción detallada | WB Descripcion larga `custitem85` | Hijo | Texto largo | Formato de la plantilla, con el bloque de características al final |
| 19 | Unidad de medida | Tipo de unidades `unitstype` = `Unidades` + unidades de stock/compra/venta | Padre e hijo | Lista | `Pieza` (base `PZ`). Calzado: ver decisión N4 |
| 20 | País de origen | WB País de origen `custitem79` | Hijo | **Texto libre** | Nombre del país en español: `China`, `México`, `Vietnam` |
| 21 | Clave SAT | SAT Clave Producto Servicio `custitem_mx_txn_item_sat_item_code` | Padre e hijo | Lista | 8 dígitos. Se hereda por categoría (Odoo usa las mismas: `53102516` gorras, `53102503` sombreros…) |
| 22 | Unidad SAT | Sin campo en el artículo: sale de la **unidad** (PZ → H87) en la localización México | — | — | Verificar el mapeo de unidades SAT antes del primer lote (pendiente 13.2) |
| 23 | WSP → MAYOREO | Nivel de precio **MAYOREO** (−42% sobre Base Price) | Hijo | Calculado | No se captura: lo calcula el nivel |
| 24 | Pist → Base Price | Nivel **Base Price** (`price_1_`) | Hijo | Moneda MXN | **Sin IVA**. Único precio que se captura |
| 25 | MSAP → RETAIL | Nivel **RETAIL** (+16% sobre Base Price) | Hijo | Calculado | No se captura. En WB debe terminar en 9 (5.5) |

Campos operativos que se llenan en el alta sin ser del estándar: **Subsidiaria** `GRUPO QUINCE 22 SA de CV`, **Subartículo de** (`parent`), **Image link** `custitem37` (enlace de imagen del ERP que usa Shopify), **Precio de compra** (costo del proveedor), **Clase** contable (`MERCANCÍA <MARCA>`, lo define Contabilidad), cuentas y método de costeo según el formulario de Compras.

> **Campos viejos de "Atributos del Producto"** (`custitem8` CLASS, `custitem9` LINE, `custitem10` CATEGORY, `custitem11` PRODUCT GROUP, `custitem12` STYLE NAME, `custitem15` SKU, `custitem16`/`17` SIZE, `custitem19` GENDER, `custitem20` SEASON, `custitem22` a `custitem26`…). Guardan los mismos hechos que los WB con otras listas (CATEGORY tiene 94 valores; GENDER incluye `JOVEN`). **En altas nuevas no se capturan.** Ver decisión N1.

---

## 5. Reglas y convenciones

El incumplimiento de cualquiera es un hallazgo de auditoría y se corrige antes de cerrar el lote.

### 5.1 Padre, hijo o artículo único

| Caso | Estructura |
|---|---|
| Estilo con 2 o más tallas | Padre + un hijo por talla |
| Estilo de una sola pieza (accesorio) | Un artículo, sin padre, `WB Talla = Unitalla / OS` |
| Mismo estilo en varios colores con **el mismo** No. de Estilo | Un padre; cada combinación color-talla es un hijo |
| Colores con No. de Estilo **distinto** | Padres distintos. Manda el No. de Estilo |

### 5.2 Nombre del artículo y UPC

- Hijo: `itemid` = UPC. Nada más: sin prefijos, sin talla.
- Padre: `<No. Estilo> : <nombre corto del proveedor>`, que es la convención verificada en la base. NetSuite muestra al hijo como `Padre : UPC`.
- `upccode` = el mismo UPC.
- El No. de Estilo **nunca** va en el UPC ni en el `itemid` del hijo (error típico heredado, documentado en Shopify WB 5.1).
- Nombre para mostrar del hijo: `<No. Estilo> : <nombre corto> : <talla>`, como el verificado (`… : 8 M`).

### 5.3 Tallas

Mismas reglas que el flujo de Odoo y que Shopify, porque las tres bases deben decir lo mismo:

- Ropa en código: XS, S, M, L, XL, 2XL, 3XL. Nunca deletreado.
- Calzado en **MX**: `MX = US + 20` (8.5 US → 28.5 MX). La talla US se guarda aparte en WB Talla US.
- Sombreros en fracción US: `6 3/4` … `8`, sin comillas.
- Jeans hombre: `29 x 32` (cintura × largo).
- Jeans dama: sin la `R`.
- Niño/Niña: por edad (2 a 16).
- Accesorio de una pieza: `Unitalla / OS`.
- **WB Talla nunca queda en `0` ni vacío.** Hoy hay casos (`10063824`, `A442002902`, `AR2829400`, `AR2829650`, `AR2830200`) y son exactamente los que no se pueden dar de alta en Shopify.

### 5.4 Color

13 valores de la lista: Rojo, Azul, Amarillo, Verde, Naranja, Morado, Rosa, Negro, Blanco, Gris, Beige, Cafe, Varios. `Distressed Brown` o `Café Oscuro` van en el Nombre, no aquí.

### 5.5 Precios

- Se captura **solo el Base Price, sin IVA**.
- MAYOREO (−42%) y RETAIL (+16%) los calcula NetSuite por nivel. **No se sobrescriben a mano**: si el WSP o MSAP del proveedor no cuadra con la fórmula, se anota en la bitácora y decide Comercial.
- Política WB: el RETAIL (Base × 1.16) debe dar un entero terminado en 9. Ej. `559.48 × 1.16 = 649`. El Base Price se calcula hacia atrás: `RETAIL objetivo / 1.16`, con 2 decimales.
- Precio de compra: del archivo del proveedor, **solo con la moneda confirmada** (Wrangler manda USD). Si no está confirmada, se deja vacío y lo valoriza la recepción (decisión N5).
- Ningún artículo vendible con Base Price en cero.

### 5.6 Categoría y División

- WB Categoria es lista plana; la jerarquía la da WB Division. Las dos deben coincidir con el mapa de Criterios (`Gorras → Accesorios`, `Botas → Calzado`, `Jeans → Denim`).
- Valores a mano: `Sueteres` va **sin acento** en NetSuite (Shopify lo mapea a `Suéteres` al cargar). `Chamarras`, no `Chaquetas`.
- Si un producto no cae en ninguna categoría, la fila sale del lote y se solicita el valor (5.8).

### 5.7 Unidad y SAT

- Tipo de unidades `Unidades`; stock, compra y venta en `Pieza` salvo lo que decida N4 para calzado. **El padre y sus hijos llevan la misma unidad.**
- Clave SAT por categoría, 8 dígitos, en padre e hijo.

### 5.8 Gobierno de listas cerradas

Cinco listas cerradas: Marca, Categoría, Color, División, Género. Más tres campos de texto que se gobiernan **como si fueran lista**: Temporada, Lifecycle, País de origen.

Si el archivo trae un valor fuera:

1. La fila no se carga.
2. Se registra como "valor pendiente de autorización".
3. El responsable de datos decide: agregar a la lista o mapear a uno existente. Agregar un valor a una lista de NetSuite requiere el permiso *Listas personalizadas*, que el rol Compras no tiene: es un control, no un estorbo.
4. Se recarga la fila.

---

## 6. Preparación del entorno (una sola vez)

### 6.1 Formulario de artículo

- Formulario de alta con la subpestaña **WB Atributos** visible y los campos viejos de *Atributos del Producto* ocultos o de solo lectura (según N1).
- Marcar como obligatorios en el formulario: WB No. Estilo, WB Talla, WB Marca, WB Division, WB Categoria, UPC. Es el equivalente al candado L2 de Odoo.

### 6.2 Listas: diferencias contra el estándar

| Lista | En NetSuite | Contra el estándar | Acción |
|---|---|---|---|
| Division | Accesorios, Ropa, Denim, Calzado | Igual | Ninguna |
| Genero | Hombre, Mujer, Niño, Niña, Unisex | Igual | Ninguna |
| Color | 13 valores | Igual | Ninguna |
| Categoria | 42 valores | Sobran **Accesorios de Sombrero, Toquillas, Pines de Sombrero** | Decisión N3: se agregan al estándar (y a Odoo y Shopify) o se retiran |
| WB Brand (Marca y Licencia) | 15 valores | `Jony Lama` (debe ser `Tony Lama`), `Justin Boots ` con **espacio al final**; `Generico` y `Sin Marca` conviven | Corregir los dos errores; decidir un solo valor para "sin marca" (N6) |

El espacio final de `Justin Boots ` es invisible y hace que el CSV no encuentre el valor. Hay que corregirlo antes de cargar esa marca.

### 6.3 Mapeo de importación guardado

Crear en **sandbox** y luego en producción dos asignaciones guardadas del asistente CSV:

- `G1522 - Padres` (Agregar)
- `G1522 - Hijos` (Agregar)
- `G1522 - Actualizar WB` (Actualizar, por ID interno)

Guardarlas evita remapear columnas en cada lote, que es donde se cuelan errores.

---

## 7. Procedimiento A — Alta masiva por CSV

Un lote = un archivo del proveedor, una marca, una temporada.

### 7.1 Paso 0 — Normalizar

1. Pasar el archivo del proveedor a la plantilla G1522, **una fila por UPC**.
2. UPC como texto.
3. Tallas y colores al estándar (5.3, 5.4).
4. Categoría y División con el mapa de Criterios.
5. Temporada, Lifecycle y País de origen escritos exactamente como la lista de 5.8.

### 7.2 Paso 1 — Validador (bloqueante)

Mismo principio que en Odoo: **el archivo se valida contra sí mismo antes de abrir NetSuite.** El validador `Validador_Carga_NetSuite_G1522.xlsx` (por construir) reusa las 15 validaciones del de Odoo y agrega cuatro propias de NetSuite:

| # | Revisa | Por qué |
|---|---|---|
| V1–V15 | Las mismas del validador de Odoo (UPC texto 12–14 dígitos, UPC único en el archivo, No. Estilo, SKU único, listas cerradas, Categoría ↔ División, precio > 0, Clave SAT 8 dígitos, Talla, Composición y País) | Ver 7.2 del flujo Odoo |
| **N1** | Temporada ∈ {SS26 … FW28}, Lifecycle ∈ {Seasonal, CORE}, País de origen en la lista de países permitidos | Son texto libre en NetSuite: nada más los detiene |
| **N2** | WB Talla ≠ `0` y en formato MX estándar | Es el defecto que hoy bloquea el alta en Shopify |
| **N3** | Todas las filas de un mismo No. Estilo traen la misma Marca, División, Género, Categoría, Temporada y Clave SAT | En NetSuite estos campos van en cada hijo; si difieren entre tallas, el estilo queda partido en los filtros |
| **N4** | Base Price × 1.16 da entero terminado en 9 (solo marcas con esa política) | Política de precio WB |

El validador arma dos hojas de salida: **CSV PADRES** (solo estilos multi-talla) y **CSV HIJOS**, con los encabezados que usan las asignaciones guardadas y el `externalid` construido por fórmula.

Semáforo en rojo: se corrige el archivo o se devuelve al proveedor. No se toca NetSuite.

### 7.3 Paso 2 — Cruce contra NetSuite

Búsqueda guardada de artículos (tipo Artículo de inventario) con columnas: ID interno, Nombre/número, Código UPC, WB No. Estilo, Subartículo de. Exportar a CSV y cruzar cada fila **por UPC**:

| Resultado | Situación | Qué se hace |
|---|---|---|
| El UPC ya existe | La pieza ya está | No se da de alta. Solo se completan campos WB vacíos con `G1522 - Actualizar WB`, por ID interno |
| El UPC no existe, el No. Estilo sí | Falta una talla | Ruta 7.6 |
| Ni UPC ni No. Estilo existen | Estilo nuevo | 7.4 (mono-talla) o 7.5 (multi-talla) |

Este cruce evita el caso Ariat de Shopify: 69 productos cargados, 59 eran duplicados.

### 7.4 Paso 3a — Mono-talla (una pasada)

Asignación `G1522 - Hijos`, sin columna *Subartículo de*. Encabezados del CSV:

```
externalid, itemid, upccode, displayname, subsidiary, unitstype,
stockunit, purchaseunit, saleunit, custitem_mx_txn_item_sat_item_code,
salesdescription, custitem81, custitem82, custitem86, custitem87,
custitem73, custitem80, custitem83, custitem70, custitem71, custitem72,
custitem74, custitem75, custitem76, custitem77, custitem78, custitem79,
custitem84, custitem85, custitem37, price_Base, purchaseprice
```

Reglas:

- `externalid` obligatorio: `g1522.<UPC>`. Con eso, reimportar el mismo archivo en modo *Agregar o actualizar* actualiza y no duplica.
- Listas por **nombre exacto** del valor (el asistente permite mapear por nombre o por ID interno; por nombre es legible y el validador ya garantizó que existe).
- **Siempre primero en sandbox** (`7913364-sb1`), con el mismo archivo. Si pasa limpio, producción.
- En producción, primero **5 filas**, revisar las fichas contra el checklist (12) y luego el resto.

### 7.5 Paso 3b — Multi-talla (dos pasadas)

NetSuite no puede ligar un hijo a un padre que todavía no existe, y el asistente procesa filas en paralelo: si padre e hijos van en el mismo archivo, algunos hijos llegan antes que su padre y truenan.

**Pasada 1 — Padres.** Asignación `G1522 - Padres`. Columnas mínimas:

```
externalid, itemid, displayname, subsidiary, unitstype, stockunit,
purchaseunit, saleunit, custitem_mx_txn_item_sat_item_code, custitem81
```

- `externalid` = `g1522.est_<No. Estilo>`.
- `itemid` = `<No. Estilo> : <nombre corto>`.
- Sin UPC, sin precio, sin talla.

**Pasada 2 — Hijos.** Mismo CSV de 7.4 más la columna `parent`, que referencia al padre **por su ID externo** (`g1522.est_<No. Estilo>`). Referenciar por ID externo y no por nombre evita que un nombre de padre parecido ligue al hijo equivocado.

Regla dura: **la columna `externalid` no se edita ni se reescribe entre cargas.** Si cambia, NetSuite crea un registro nuevo.

### 7.6 Paso 3c — Talla faltante en estilo existente

1. Del cruce (7.3), tomar el ID interno o ID externo del padre existente.
2. Cargar el hijo nuevo con la pasada 2, con `parent` apuntando a ese padre.
3. Si el padre existente no tiene ID externo (altas viejas), referenciarlo por ID interno.

A diferencia de Odoo, agregar un hijo **no recrea** los demás. Es una operación segura.

### 7.7 Paso 4 — Cierre del lote

- Sin existencias; entran por recepción.
- Registrar el lote en la bitácora (13.3): archivo, marca, temporada, padres, hijos, rechazadas y motivo, valores pendientes.
- Avisar aguas abajo según 2.2.

---

## 8. Procedimiento B — Alta manual (1 a 3 productos)

1. Listas → Contabilidad → Artículos → **Nuevo** → Artículo de inventario.
2. Si es multi-talla, crear primero el **padre** (solo Información principal y WB No. Estilo) y guardar.
3. Crear el hijo: **Nombre/número** = UPC, **Código UPC** = UPC, **Subartículo de** = el padre, unidades, subsidiaria, SAT Clave.
4. Subpestaña **WB Atributos**, de arriba abajo: División, Género, Categoría, Marca, Color, Temporada, Lifecycle, Silueta, Fit, País de origen, Licencia, No. Estilo, Talla, SKU, Descripción, Talla US, Composición, Descripción larga.
5. **Ventas/Fijación de precios** → MXN → solo **Base Price**. Revisar que MAYOREO y RETAIL se calcularon.
6. **Compras/Inventario** → Precio de compra si la moneda está confirmada.
7. Guardar y correr el checklist (12).

Los campos de la subpestaña *Atributos del Producto* no se tocan.

---

## 9. Corrección de lo ya cargado

Mismo método que Odoo: **búsqueda guardada → exportar con ID interno → llenar → importar en modo Actualizar**. Nunca sin respaldo del subconjunto.

| Hallazgo | Acción | Prioridad |
|---|---|---|
| WB Talla en `0` o vacío (`10063824`, `A442002902`, `AR2829400`, `AR2829650`, `AR2830200` y los que salgan en la medición) | Capturar talla MX contra el ID interno de cada UPC | Alta: bloquea Shopify |
| Temporada, Lifecycle, País con variantes de escritura (`ss26`, `Seasonal `, `CHINA`) | Búsqueda agrupada por valor → normalizar | Alta |
| Padre e hijos con unidad distinta | Homologar según N4 | Media |
| Hijos con WB vacío en estilos que tienen otros hijos llenos | Copiar del hermano por No. Estilo | Media |
| Valores de Marca/Categoría fuera del estándar (6.2) | Reasignar tras decidir N3 y N6 | Media |

**Medición pendiente.** Esta versión no incluye el conteo de artículos con campos WB vacíos, porque el rol Compras no permite crear las búsquedas agrupadas necesarias en producción. Primer entregable de E2: el tablero de 10.

---

## 10. Tablero de salud del catálogo NetSuite

Búsquedas guardadas, una por métrica, favoritas del responsable de datos.

| # | Métrica | Criterio de la búsqueda | Meta |
|---|---|---|---|
| S1 | Hijos sin UPC | Tipo inventario, Subartículo de ≠ vacío, UPC vacío | 0 |
| S2 | UPC repetido en `upccode` | Agrupar por Código UPC, conteo > 1 | 0 |
| S3 | Artículos con WB Talla `0` o vacío | WB Talla vacío o = 0 | 0 |
| S4 | Artículos con WB No. Estilo vacío | — | 0 |
| S5 | Temporada/Lifecycle/País fuera de lista | Agrupar por valor, comparar | 0 |
| S6 | Base Price en cero en artículos vendibles | — | 0 |
| S7 | Estilos con Marca/División/Categoría distinta entre hermanos | Agrupar por No. Estilo, contar valores distintos | 0 |
| S8 | Padre y hijo con unidad distinta | — | 0 |

Semanal: S1, S3, S6. Mensual: todas.

---

## 11. Riesgos y controles

| Riesgo | Cómo pasa | Control |
|---|---|---|
| Duplicar al reimportar | Cargar sin `externalid` | `externalid` obligatorio y estable |
| Hijo huérfano o ligado al padre equivocado | Padre e hijos en el mismo CSV; referencia por nombre | Dos pasadas; `parent` por ID externo |
| Texto libre mal escrito | `ss26`, `CHINA`, `Seasonal ` | Validación N1; tablero S5 |
| UPC sin ceros | Excel lo vuelve número | Columna texto, V1 |
| Talla en cero | Proveedor manda US o nada | Validación N2 |
| Hecho en dos lugares | Capturar CATEGORY viejo y WB Categoria | N1: congelar campos viejos |
| Carga directa en producción | Rol con pocos permisos, error sin vuelta atrás | Sandbox primero, 5 filas después |
| Costo en moneda equivocada | Archivo en USD | N5, bitácora por lote |
| Valor de lista con espacio invisible | `Justin Boots ` | Corrección en 6.2 |

---

## 12. Checklist de cada carga

**Antes de importar**

- [ ] Validador en verde (V1–V15 y N1–N4).
- [ ] Cruce contra NetSuite hecho: cada fila clasificada (ya existe / talla faltante / estilo nuevo).
- [ ] CSV PADRES y CSV HIJOS generados, con `externalid` completo.
- [ ] Moneda del costo confirmada o costo vacío.
- [ ] Valores pendientes resueltos o fuera del lote.
- [ ] Importación probada en sandbox sin errores.
- [ ] Respaldo exportado, si es actualización.

**Después de importar**

- [ ] Padres creados = estilos multi-talla del lote.
- [ ] Hijos + mono-talla creados = UPC del lote.
- [ ] Todo hijo tiene *Subartículo de* correcto y UPC = Nombre/número.
- [ ] WB Talla sin ceros ni vacíos.
- [ ] 5 fichas revisadas contra la plantilla (subpestaña WB Atributos completa).
- [ ] Base Price > 0; MAYOREO y RETAIL calculados; RETAIL termina en 9 donde aplica.
- [ ] Campos viejos de *Atributos del Producto* vacíos en lo nuevo.
- [ ] Sin existencias.
- [ ] Lote en bitácora con rechazadas y motivo.
- [ ] Aviso aguas abajo: Almacén/Compras, Odoo, Shopify, Comercial, GS1.

---

## 13. Bitácora y pendientes

### 13.1 Decisiones abiertas

| # | Decisión | Recomendación | Bloquea |
|---|---|---|---|
| N1 | Campos viejos de *Atributos del Producto* (CATEGORY, GENDER, CLASS, LINE, SIZE, SEASON…) | Congelar: no se capturan en altas nuevas, se ocultan del formulario de alta. Antes, confirmar con TI/Celigo qué integración o reporte los lee todavía | Formulario (6.1) |
| N2 | Mono-talla con o sin padre | Sin padre: un solo artículo | Ruta 7.4 |
| N3 | `Accesorios de Sombrero`, `Toquillas`, `Pines de Sombrero` en la lista de Categoría | Si hay producto real, agregarlas al estándar (y a Odoo y Shopify); si no, retirarlas | Lotes de sombrero |
| N4 | Unidad del calzado: `Par` o `Pieza` | Una sola regla por división, aplicada a padre e hijos por igual | Lotes de calzado |
| N5 | Moneda del costo en archivos de proveedor | Igual que D5 de Odoo: una sola regla para los dos sistemas | Todo alta con costo |
| N6 | `Generico` vs `Sin Marca`; corregir `Jony Lama` y `Justin Boots ` | Un solo valor para "sin marca"; corregir los dos errores | Lotes de esas marcas |

Además, las decisiones de Odoo aplican aquí: **D3** (responsable único de listas, Enrique) y **D4** (Trinity West / Trinity Ranch: hoy **no** existen en la lista WB Brand de NetSuite, así que no se pueden cargar a NetSuite hasta decidir).

### 13.2 Pendientes técnicos

- Construir `Validador_Carga_NetSuite_G1522.xlsx` (V1–V15 + N1–N4, dos hojas CSV).
- Crear las tres asignaciones CSV guardadas en sandbox y producción.
- Formulario de alta con WB obligatorios y campos viejos ocultos.
- Verificar el mapeo de unidad SAT (PZ → H87, Par → PR) en la localización México.
- Corregir `Jony Lama` y `Justin Boots ` en la lista WB Brand.
- Definir quién ejecuta la importación en producción (el rol Compras no tiene permiso de listas personalizadas; confirmar permiso de importación CSV).
- Crear las 8 búsquedas del tablero (10) y tomar la primera medición.
- Capturar WB Talla de los 5 estilos pendientes.

### 13.3 Registro de lotes

| Fecha | Archivo | Marca | Temporada | Padres | Hijos | Rechazadas | Notas |
|---|---|---|---|---|---|---|---|
| | `Wrangler_CatalogoEstandar_ES2.xlsx` | Wrangler | FW26 | 0 | 51 | | Piloto. Gorras mono-talla, sin padre. Costo en USD por confirmar. Se carga a NetSuite **antes** que a Odoo |

---

## Anexo A — Referencias verificadas en la instancia

Tomadas de NetSuite `7913364` el 22-sep-2026, rol *Grupo Quince 22 - Compras*.

- Subpestañas de la ficha de artículo: Atributos del Producto, CAPSLAB Attributes, REFLO Attributes, HAPPY SOCKS Attributes, MBRANDS Data, **WB Atributos**.
- Campos WB: `custitem70` División · `71` Género · `72` Categoría · `73` Marca · `74` Color · `75` Temporada · `76` Lifecycle · `77` Silueta · `78` Fit · `79` País de origen · `80` Licencia · `81` No. Estilo · `82` Talla · `83` Descripción · `84` Composición · `85` Descripción larga · `86` Talla US · `87` SKU.
- Otros: `custitem37` Image link · `custitem_mx_txn_item_sat_item_code` SAT Clave Producto Servicio · `upccode` Código UPC.
- Niveles de precio: Base Price, MAYOREO −42%, MAYOREO + 10% DESC −48%, RETAIL +16%, DEPARTAMENTAL −45%, CASA −50%, CONSIGNACION −36%, ENGLISH −36%, PATROCINIO −99.99%, más CAPS LAB y HAPPY SOCKS.
- Ejemplo de estructura: padre `10063824 : YTH BOOKER CHELSEA DSTSD BRN` (unidad Pieza) → hijo `197318660764`, UPC `197318660764`, WB Talla `0`, WB Talla US `8 M`, unidad Par, SAT `53111500`.

## Anexo B — Validación por script

La lógica del anexo B del flujo Odoo aplica tal cual para V1–V15. Las validaciones propias de NetSuite se agregan así:

```python
TEMPORADAS = {'SS26','FW26','SS27','FW27','SS28','FW28'}
LIFECYCLE  = {'Seasonal','CORE'}

def motivos_netsuite(r, grupo):
    m = []
    if str(r['WB Temporada']).strip() not in TEMPORADAS:
        m.append('Temporada fuera de lista (texto libre en NetSuite)')
    if str(r['WB Lifecycle']).strip() not in LIFECYCLE:
        m.append('Lifecycle debe ser Seasonal o CORE')
    if str(r['WB Talla']).strip() in ('', '0', 'nan'):
        m.append('WB Talla en cero o vacía')
    for c in ['WB Marca','WB División','WB Género','WB Categoría','WB Temporada','SAT Clave de producto']:
        if grupo[c].nunique() > 1:
            m.append(f'{c} distinto entre tallas del mismo estilo')
    return m

# grupo = df[df['WB N.º de estilo'] == r['WB N.º de estilo']]
```
