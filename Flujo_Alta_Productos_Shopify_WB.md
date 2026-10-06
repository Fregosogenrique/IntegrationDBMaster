# Flujo de trabajo para alta de productos en Shopify · Western Brothers

Procedimiento único de alta de productos en la tienda Shopify de Western Brothers (WB Ecommerce), bajo el Estándar de catálogo G1522 y alimentada desde NetSuite.

- Empresa: Grupo Quince 22
- Tienda: Western Brothers (WB Ecommerce)
- Estándar de referencia: Estándar de producto G1522 y catálogo estándar de NetSuite ("Productos Catalogo Estandar")
- Fecha del documento: 22 de septiembre de 2026 · versión 1.0 (reemplaza como procedimiento de alta a la sección 4.1 de `Control_Datos_Shopify_WB.md`, que sigue vigente como documento de auditoría)
- Método de carga estándar: **Matrixify** (app y conector "Matrixify WB"). El importador tradicional de Shopify está prohibido: no llena metacampos. El alta manual queda para casos de 1 a 3 productos.

Documentos que acompañan a este procedimiento:

| Documento | Para qué |
|---|---|
| `Flujo_Alta_Productos_Shopify_WB.svg` | Diagrama del flujo, con las fronteras y el detalle de cómo Matrixify identifica productos |
| `Control_Datos_Shopify_WB.md` | Reglas de datos, bitácora de auditoría y pendientes de la tienda |
| `Flujo_Alta_Productos_Odoo_G1522.md` | El alta en Odoo bajo el mismo estándar |
| `Flujo_Alta_Productos_Shopify_Stetson.md` | El mismo flujo para Stetson México (sección 3.4: diferencias entre tiendas) |

---

## 1. Resumen ejecutivo

**Qué se entrega.** Un procedimiento único para dar de alta productos en Western Brothers, que convierte las reglas ya escritas en `Control_Datos_Shopify_WB.md` en un flujo con validación bloqueante, cruce, carga por etapas, verificación y bitácora.

**Por qué hace falta.** WB ya tiene reglas claras (SKU = UPC, metacampos, precio que termina en 9), pero **no tiene un camino que obligue a cumplirlas**. La bitácora de la semana del 15 de septiembre lo muestra:

| Evento | Qué pasó | Qué lo hubiera evitado |
|---|---|---|
| Lote Ariat del 15-sep | 69 productos cargados con el importador tradicional: SKU invertido en las 178 variantes, metacampos vacíos, tallas fuera del estándar, handles `ariat-<estilo>` | Carga solo por Matrixify, validador bloqueante |
| El mismo lote | **59 de 69 eran duplicados** de productos existentes; solo 10 eran nuevos | Cruce contra la tienda antes de cargar |
| Duplicados previos | 14 grupos (28 productos) con el mismo UPC en más de un handle, en su mayoría gemelos creados el 14-sep | Validación del UPC contra la tienda |
| Camisa REAL Billie | 6 variantes azules (estilo 10043452) pegadas en el producto rosa (10055210) | Validar que todas las filas de un handle tengan el mismo No. de Estilo |
| "Bota Sport Western Weathered Tan" | Producto falso: sus códigos de barras eran de la Booker Chelsea juvenil | Validación del UPC contra la tienda |
| Carga que tronó | El ERP traía `Chamarras` y la lista del metacampo solo tenía `Chaquetas` | Validar contra la lista antes de cargar |

Todos estos casos tienen una raíz común:

> **Shopify no valida la unicidad del SKU ni la del código de barras.** Odoo rechaza un código de barras repetido; Shopify lo acepta sin avisar. En WB el SKU y el código de barras son el mismo UPC, así que un UPC repetido es a la vez un SKU repetido y un código de barras repetido, y nada en Shopify lo detiene. Lo tiene que detener el procedimiento.

**Lo que este flujo cambia.**

1. Una sola puerta de entrada: el catálogo estándar de NetSuite. Nada se crea desde el importador tradicional, desde "Duplicar" ni a mano sin pasar por el estándar.
2. Validación bloqueante antes de cargar, en dos mitades: el archivo contra sí mismo y el archivo contra el export de la tienda.
3. Clasificación de cada UPC en tres rutas (ya existe / falta variante / producto nuevo), con el `Command` que le corresponde.
4. Carga en tres tiempos: dry run, muestra de 5, resto del lote. Nuevos primero, variantes después.
5. Verificación posterior y bitácora por lote como acta de entrega.

**Tres decisiones que requieren visto bueno.**

| # | Decisión | Recomendación |
|---|---|---|
| W1 | ¿Producto sin imagen en el ERP se publica? Hoy el default es `Active` + `Published TRUE`. | Sin `WB Image link` el producto entra en `Draft` y se anota en la bitácora. Un producto sin foto no se publica. |
| W2 | Precio que no termina en 9 al calcular `Sales Price × 1.16`. | La fila no entra; se corrige el Sales Price en NetSuite. No se redondea en Shopify, para que los dos sistemas no difieran. |
| W3 | Responsable único de agregar valores a la lista del metacampo `custom.categoria` (y demás listas). | El mismo responsable de datos que en Odoo (D3). Sin su autorización, la fila se rechaza. |

---

## 2. Alcance y fronteras del flujo

### 2.1 Qué cubre

- Alta de productos nuevos (estilo nuevo), mono-talla y multi-talla.
- Alta de variantes faltantes en productos existentes.
- Completar campos vacíos (metacampos, tags) de productos que aparecen en un lote.
- Altas originadas en transferencias (como TO2967 y TO2969) y en la hoja "Assortment & Allocation WB Ecom".

### 2.2 Qué no cubre, y dónde entrega

| Frontera | Dónde termina este flujo | Quién recoge | Precondición que este flujo garantiza |
|---|---|---|---|
| **Inventario** | El producto queda con **existencias en cero** en las tres sucursales (Eventos WB, Western Brothers Mexico, Western Brothers Outlet Lerma) | Almacén, al recibir la transferencia | Cada variante tiene su UPC como SKU y código de barras: la recepción se hace con lector |
| **Canales y colecciones** | El producto queda `Active` y `Published` en Tienda online y POS | E-commerce, para colecciones manuales, otros canales y orden de vitrina | Tags con el patrón estándar y Type = División, que es de lo que cuelgan las colecciones automáticas |
| **Precios y promociones** | Queda el precio con IVA terminado en 9; `Compare at price` vacío | Comercial | El precio cuadra con NetSuite (`Sales Price × 1.16`) |
| **Contenido e imagen** | Queda la imagen del ERP si existe; sin ella, `Draft` (W1) | E-commerce | Lista de productos en `Draft` por falta de imagen |
| **Corrección en NetSuite** | Un UPC con talla vacía o en cero, o con dato fuera de lista, **no entra** | Responsable de datos, que corrige contra el Internal ID en NetSuite | Lista de filas rechazadas con Internal ID y motivo |

La bitácora del lote (7.7) es el acta de entrega: nadie aguas abajo actúa sobre un lote no registrado como cerrado, y el cierre nombra también las filas rechazadas.

---

## 3. Arquitectura de datos

### 3.1 Los dos niveles de Shopify

Shopify separa producto y variante, pero a diferencia de Odoo **las variantes se crean en la misma carga**: cada fila del archivo es una variante, y las filas con el mismo `Handle` forman un producto. El alta es de **una sola pasada**, aun en estilos multi-talla.

| Nivel | Qué es | Qué se captura |
|---|---|---|
| Producto | El estilo | Handle, Title, Body HTML, Vendor, Type, Tags, imagen, estado, los 8 metacampos `custom.*` |
| Variante | La pieza: este estilo en esta talla | SKU, Barcode, precio, talla, inventario por sucursal |

Regla de oro: **un estilo = un producto; una talla = una variante.**

### 3.2 Llaves

| Llave | Dónde vive | Para qué | ¿Shopify la valida? |
|---|---|---|---|
| UPC Code (NetSuite) | `Variant SKU` **y** `Variant Barcode` | Identificador único de pieza y llave de cruce con NetSuite | **No** |
| WB No. Estilo | `custom.no_estilo` | Llave de agrupación de variantes | No aplica |
| Handle | Producto | Llave de creación. Único en la tienda | Sí |
| `ID` / `Variant ID` | Producto / Variante | Llave técnica de actualización (equivalente al `id` externo de Odoo) | Sí |
| Internal ID (NetSuite) | Variante en NetSuite | Llave para corregir en el ERP | No aplica |

En WB la llave es una sola: el UPC. Eso simplifica el cruce (no hay que decidir entre SKU y código de barras) pero concentra el riesgo: un UPC mal capturado rompe las dos cosas a la vez.

### 3.3 Fuentes de datos

1. **Catálogo estándar NetSuite** ("Productos Catalogo Estandar"): una fila por UPC. Es la fuente de verdad.
2. **Lista de UPC a dar de alta**: de la transferencia o de la hoja "Assortment & Allocation WB Ecom".
3. **Export de la tienda**: la exportación diaria `ProductsWB` que ya corre en Matrixify a las 03:00 (587 productos en la del 22-sep). Es contra lo que se cruza. Si el lote se arma después de una carga del mismo día, se corre una exportación nueva.
4. **Lista de valores del metacampo `custom.categoria`**, idéntica a WB Categoria del ERP.

### 3.4 Diferencias con Stetson México

| Tema | Western Brothers | Stetson México |
|---|---|---|
| SKU | UPC | Código de artículo Stetson |
| Código de barras | UPC (mismo valor que el SKU) | UPC |
| Fuente directa | NetSuite | Lote cerrado de Odoo / lista del proveedor |
| Precio con IVA | Termina en 9 | Múltiplo de 50 (por confirmar) |
| Metacampos del estándar | Existen los 8 | Por crear |
| Type | División | Texto libre por familia, por migrar |
| Conector Matrixify para Claude | Sí ("Matrixify WB") | No |

---

## 4. Diccionario de campos: NetSuite → Shopify (Matrixify)

| Columna Matrixify | Nivel | Origen NetSuite / valor | Regla |
|---|---|---|---|
| `Handle` | Producto | Slug del título + WB No. Estilo | `botas-wrangler-coyote-cafe-waca0213`. Nunca `marca-<estilo>` ni sufijos `-copy`, `-1` |
| `Command` | Producto | `NEW` / `MERGE` / `UPDATE` | Según la ruta del cruce (7.3) |
| `Title` | Producto | Nombre del ERP | `Tipo + Marca + Modelo + Color`. Sin No. de Estilo |
| `Body HTML` | Producto | Descripción del ERP | Párrafo comercial + bloque de características |
| `Vendor` | Producto | Marca (Ariat, Wrangler, Roper…) | Marca, no nombre de la tienda |
| `Type` | Producto | WB Division | Ropa, Calzado, Accesorios, Denim. Excepción histórica: Fragancias |
| `Tags` | Producto | No.Estilo, Categoria, Color, Genero, Temporada, Marca | `Tags Command = MERGE` |
| `Status` / `Published` | Producto | — | `Active` / `TRUE`; `Draft` sin imagen (W1) |
| `Image Src` | Producto | WB Image link | Solo si existe. `Image Command = MERGE`, en la fila principal |
| `Option1 Name` / `Option1 Value` | Variante | WB Talla | `Talla` + talla MX estándar. Mono-talla: `Title` / `Default Title` |
| `Variant SKU` | Variante | UPC Code | **Igual al barcode**. Como texto |
| `Variant Barcode` | Variante | UPC Code | Igual al SKU |
| `Variant Price` | Variante | Sales Price × 1.16 | Entero terminado en 9 |
| `Variant Weight` / `Unit` | Variante | — | `0` / `kg` |
| `Variant Taxable` | Variante | — | `TRUE` |
| `Variant Inventory Tracker` / `Policy` | Variante | — | `shopify` / `deny` |
| `Variant Fulfillment Service` / `Requires Shipping` | Variante | — | `manual` / `TRUE` |
| `Inventory Available: Eventos WB` | Variante | — | `0` solo en altas |
| `Inventory Available: Western Brothers Mexico` | Variante | — | `0` solo en altas |
| `Inventory Available: Western Brothers Outlet Lerma` | Variante | — | `0` solo en altas |
| `Metafield: custom.no_estilo` | Producto | WB No. Estilo | Nunca en el SKU |
| `Metafield: custom.categoria` | Producto | WB Categoria | Lista cerrada. `Sueteres` → `Suéteres` |
| `Metafield: custom.division` | Producto | WB Division | |
| `Metafield: custom.genero` | Producto | WB Genero | |
| `Metafield: custom.temporada` | Producto | WB Temporada | |
| `Metafield: custom.lifecycle` | Producto | WB Lifecycle | `Seasonal` por omisión |
| `Metafield: custom.composicion` | Producto | WB Composicion | |
| `Metafield: custom.licencia` | Producto | WB Licencia | |

Las columnas de metacampo se escriben con su tipo, como las exporta Matrixify (por ejemplo `Metafield: custom.categoria [single_line_text_field]`). Lo más seguro es copiar los encabezados de la exportación `ProductsWB`, no escribirlos a mano.

---

## 5. Reglas y convenciones

Son las de `Control_Datos_Shopify_WB.md`, sección 2. Aquí se resumen y se agregan las que el flujo necesita.

### 5.1 SKU y código de barras

- `Variant SKU` = `Variant Barcode` = UPC Code de NetSuite. Siempre los dos, siempre iguales.
- El No. de Estilo va en `custom.no_estilo`, nunca en el SKU. El error típico (estilo en el SKU, UPC en el barcode) es exactamente el del lote Ariat.
- El UPC es único en toda la tienda. Como Shopify no lo impide, lo revisan V2 y V3 (7.2).

### 5.2 Precios

- NetSuite trae el Sales Price **sin IVA**. Shopify lleva `Sales Price × 1.16`.
- El resultado debe ser un entero terminado en 9 (559.48 × 1.16 = 649). Si no lo es, el Sales Price está mal en el ERP (W2).

### 5.3 Tallas

| Familia | Valor estándar | Llega mal así |
|---|---|---|
| Ropa | `XS`, `S`, `M`, `L`, `XL`, `XXL` | `Chica`, `Mediana`, `Grande`, `Extra grande`, `Extra chica`, `Doble extra grande` |
| Botas | Talla MX numérica del ERP: `28.5` | `8.5` (US con etiqueta MX) → `28.5` (MX = US + 20) |
| Jeans | Con sufijo del ERP: `25 R` | `25` |
| Accesorio de una pieza | `Option1 Name = Title`, `Option1 Value = Default Title` | `Talla única`, `UNI` |

El nombre de la opción es `Talla`. Un UPC con talla vacía o en cero en NetSuite no se da de alta: se corrige primero contra su Internal ID (pendientes conocidos: 10063824, A442002902, AR2829400, AR2829650, AR2830200).

### 5.4 Type, categoría y listas cerradas

- `Type` = WB Division.
- `custom.categoria` valida contra una lista cerrada en Shopify que debe ser **idéntica** a WB Categoria del ERP. Excepción de captura conocida: `Sueteres` (ERP) → `Suéteres` (Shopify).
- Si llega una categoría que no está en la lista, **no se agrega al vuelo**: la fila sale del lote, se pide autorización (W3) y, si se aprueba, se agrega el valor a la lista **y** se confirma que NetSuite lo tenga igual. Así se resolvió `Chamarras`.

### 5.5 Tags

Patrón `No.Estilo, Categoria, Color, Genero, Temporada, Marca`, con `Tags Command = MERGE`. Ejemplo: `10046456, Chamarras, Negro, Hombre, SS26, Ariat`. `MERGE` agrega sin borrar las etiquetas que usan las colecciones.

### 5.6 Handle, título e imagen

- Handle: slug descriptivo del título + No. de Estilo. Nunca `marca-<estilo>` (genera choques y rompe la convención), nunca sufijos de duplicado.
- Image Src = WB Image link del ERP, una imagen por estilo, en la fila principal. Sin imagen: `Draft` (W1).

### 5.7 Lo que nunca se hace

- **Nunca el importador tradicional de Shopify.** No llena metacampos y fue el origen del lote Ariat.
- **Nunca "Duplicar"** para crear un producto parecido: copia SKU y barcode.
- **Nunca `REPLACE`** (ni `Command` ni `Variant Command`): borra y recrea, perdiendo IDs, historial por variante e inventario.
- **Nunca `NEW` para completar un alta fallida.** Se usa `MERGE` con el mismo Handle.

---

## 6. Preparación del entorno

WB ya tiene casi todo listo. Lo que falta:

| # | Qué | Cómo | Estado |
|---|---|---|---|
| 6.1 | Lista del metacampo `custom.categoria` idéntica a WB Categoria | Exportar la definición y compararla contra la lista del ERP, valor por valor, con acentos | Parcial: se agregó `Chamarras`; falta la revisión completa |
| 6.2 | Listas de `custom.division`, `custom.genero`, `custom.temporada`, `custom.lifecycle` | Misma comparación | Por revisar |
| 6.3 | Exportación de cruce | Ya existe: `ProductsWB`, diaria a las 03:00. Confirmar que incluye `ID`, `Handle`, `Variant ID`, `Variant SKU`, `Variant Barcode` y los 8 metacampos | Por confirmar columnas |
| 6.4 | Colecciones y filtros | Exportar las colecciones automáticas y anotar cuáles filtran por Type o Tag, antes de homologar etiquetas viejas | Por hacer |
| 6.5 | Tallas pendientes en NetSuite | Capturar la talla contra el Internal ID de los 5 estilos pendientes | Pendiente (Control de datos, sección 6) |

---

## 7. Procedimiento A — Alta masiva con Matrixify

Un lote es una transferencia o una lista de asignación: una fuente, una fecha.

### 7.1 Paso 0 — Armar el archivo del lote

1. Tomar la lista de UPC del lote (transferencia u hoja de asignación).
2. Cruzarla contra el catálogo estándar de NetSuite más reciente y traer todos los campos del diccionario (sección 4).
3. Un UPC que no esté en NetSuite, o que esté con talla vacía, **no entra**: va a la lista de rechazados con su motivo.
4. Armar el archivo Matrixify: una fila por UPC. UPC como **texto**.

### 7.2 Paso 1 — Validación previa (bloqueante)

**El problema.** El error más caro en WB no es un dato mal escrito: es un UPC que ya estaba en la tienda y se vuelve a cargar en otro handle. Shopify lo acepta, la tienda queda con dos productos que venden la misma pieza, y el inventario se reparte entre los dos. Fue lo que pasó con 59 de 69 productos del lote Ariat y con los 14 grupos de duplicados previos.

**La solución.** Una validación que corre siempre, antes de abrir Matrixify, con dos mitades: el archivo contra sí mismo y el archivo contra la exportación `ProductsWB` del día. Con el conector "Matrixify WB", Claude puede correr la exportación, cruzarla y devolver el archivo marcado.

| # | Revisa | Por qué importa |
|---|---|---|
| V1 | UPC presente, texto de 12 a 14 dígitos | Sin ceros perdidos |
| V2 | UPC único **dentro del archivo** | Shopify no lo detiene |
| V3 | UPC que **no existe en otro producto** de la tienda | El duplicado silencioso (lote Ariat, 14 grupos previos, Bota Sport) |
| V4 | `Variant SKU` = `Variant Barcode` | La regla 5.1; detecta el SKU invertido |
| V5 | El SKU no es un No. de Estilo (no coincide con `custom.no_estilo`) | El error del lote Ariat |
| V6 | No. de Estilo presente | Va en `custom.no_estilo` |
| V7 | Todas las filas de un Handle tienen el mismo No. de Estilo | Evita el caso Camisa REAL Billie |
| V8 | `custom.categoria` en la lista, escrita exactamente igual (acentos) | Evita el caso `Chamarras` / `Suéteres` |
| V9 | División, Género, Temporada y Lifecycle en su lista | Igual |
| V10 | Categoría consistente con División | Mismo mapa que la hoja Criterios |
| V11 | `Option1 Name` = `Talla` (o `Title`) y valor en el estándar de su familia (5.3) | Evita `Mediana`, `8.5` en botas, `25` sin `R` |
| V12 | Combinación Handle + talla única | Shopify rechaza dos variantes con la misma talla |
| V13 | `Variant Price` = `Sales Price × 1.16` y termina en 9 | Regla de precio WB |
| V14 | Handle con la convención, sin `marca-<estilo>` ni sufijos de duplicado | |
| V15 | Handle `NEW` que no exista ya en la tienda | `NEW` fallaría |
| V16 | `Image Src` presente; si no, `Draft` | W1 |

Resultado: semáforo `LISTO PARA CARGAR` / `NO CARGAR` y columna `MOTIVO` por fila. El script del Anexo B del flujo de Stetson sirve igual, cambiando la configuración (regla de precio "termina en 9", V4 y V5 agregadas).

### 7.3 Paso 2 — Cruce contra la tienda: tres rutas

Cruzar cada UPC contra la exportación `ProductsWB` por `Variant Barcode` (y `Variant SKU`, que en WB es lo mismo):

| Resultado | Situación | Qué se hace | Command |
|---|---|---|---|
| El UPC ya existe | La pieza ya está | No se da de alta. Solo se completan metacampos o tags vacíos, con `ID` y `Variant ID` del export | `UPDATE` |
| El UPC no existe, el estilo sí | Falta una talla | Se agrega la variante al Handle existente | `MERGE` + `Variant Command = MERGE` |
| Ni UPC ni estilo existen | Producto nuevo | Se crea | `NEW` |

Referencia de volumen: en las transferencias TO2967 y TO2969, de 1,005 UPC, 220 ya estaban en Shopify, 62 eran variantes faltantes (15 estilos) y 723 eran producto nuevo (169 estilos). Si ese cruce no se hubiera hecho, 220 piezas habrían nacido duplicadas.

Si un UPC aparece en **dos** productos de la tienda, la fila no entra: es un duplicado previo y se resuelve primero (sección 9).

### 7.4 Paso 3 — Estructura del archivo

Las 34 columnas de la plantilla estándar (más las de imagen), en este orden:

```
Handle, Command, Title, Body HTML, Vendor, Type, Tags, Tags Command,
Status, Published, Image Src, Image Position, Image Command,
Variant Command, Option1 Name, Option1 Value, Variant SKU, Variant Barcode,
Variant Weight, Variant Weight Unit, Variant Price, Variant Taxable,
Variant Inventory Tracker, Variant Inventory Policy,
Variant Fulfillment Service, Variant Requires Shipping,
Inventory Available: Eventos WB,
Inventory Available: Western Brothers Mexico,
Inventory Available: Western Brothers Outlet Lerma,
Metafield: custom.genero, Metafield: custom.categoria,
Metafield: custom.division, Metafield: custom.licencia,
Metafield: custom.temporada, Metafield: custom.lifecycle,
Metafield: custom.composicion, Metafield: custom.no_estilo
```

Para actualizaciones (`UPDATE`) se agregan al inicio `ID` y `Variant ID` del export y **se quitan** las tres columnas de inventario (ni en cero ni vacías: una celda vacía en `Inventory Available` le quita la sucursal a la variante, y un cero borra las existencias reales).

Reglas del archivo:

- En altas nuevas, sin `ID` ni `Variant ID`.
- En actualizaciones, `ID` y `Variant ID` salen del export y **no se editan**. Matrixify identifica el producto por `ID`, luego por `Handle`, luego por `Title`; con `MERGE`, si no lo encuentra, **crea uno nuevo**. El `ID` es lo que impide que una recarga duplique.
- Una variante nueva en un producto existente se identifica por `Variant ID`, SKU, código de barras o talla; si Matrixify no la encuentra, la agrega. Por eso V3 es bloqueante.

### 7.5 Paso 4 — Carga en tres tiempos

1. **Dry run.** Opción *Dry Run* en la importación (desde la app o con el conector). Simula la carga sin escribir. No atrapa todo: los errores que devuelve Shopify (valor fuera de la lista de un metacampo) salen hasta la carga real. Por eso el paso 1 es bloqueante.
2. **Muestra de 5 productos**, uno multi-talla y uno mono-talla. Revisarlos en el admin y en la tienda.
3. **Resto del lote**, en este orden: **NUEVOS primero, luego VARIANTES FALTANTES**, al final actualizaciones.

Después de cada importación, descargar el archivo de resultados de Matrixify. Lo que falló se corrige y se reimporta **con `MERGE`**, nunca con `NEW`.

### 7.6 Variantes faltantes

1. Del export, el `Handle` del producto.
2. Una fila por talla nueva: `Handle`, `Command = MERGE`, `Variant Command = MERGE`, `Option1 Name = Talla` (**idéntico** al del producto), talla, SKU, Barcode, precio, valores fijos de variante e inventario `0` en las tres sucursales (es variante nueva).
3. Sin columnas de producto que no se quieran cambiar.

### 7.7 Paso 5 — Cierre del lote

- Inventario en cero; estado `Active` o `Draft` con motivo.
- Bitácora (sección 13): origen, número de job de Matrixify, productos nuevos, variantes nuevas, actualizaciones, rechazadas con Internal ID y motivo, productos en `Draft`.
- Guardar el archivo cargado y el archivo de resultados junto a la bitácora.

---

## 8. Procedimiento B — Alta manual (1 a 3 productos)

1. Productos → Agregar producto. **Nunca** desde "Duplicar".
2. Título, descripción, imagen del ERP.
3. Proveedor (marca), Tipo = División, etiquetas con el patrón.
4. Agregar opción `Talla` con los valores MX del ERP.
5. En cada variante: **SKU = UPC** y **Código de barras = UPC**, precio con IVA terminado en 9.
6. Inventario en cero; vender sin existencias desactivado.
7. Los 8 metacampos al final de la ficha, desde NetSuite.
8. Checklist de la sección 12 y bitácora.

---

## 9. Corrección del catálogo ya cargado

Plan completo (olas, tablero y rutina): `Propuesta_Limpieza_Catalogo_Shopify.md`.

| Hallazgo | Acción | Estado |
|---|---|---|
| Duplicados por UPC en más de un handle | Árbol de decisión abajo | 14 grupos resueltos el 16–18 sep; volver a medir cada semana |
| Tags con patrón viejo (`A1109003, cat_bandanas`) | Agregar el patrón nuevo con `MERGE`; retirar el viejo con `Tags Command = DELETE` después de revisar colecciones (6.4) | Pendiente |
| Estilo 10063824: ERP dice "Café", Shopify decía "Distressed Brown" | Color normalizado en tags y metacampo; nombre comercial solo en el título | Pendiente |
| Estilos con talla vacía en NetSuite | Corregir en el ERP y dar de alta con este flujo | Pendiente |

Árbol de decisión para duplicados (el mismo de `Control_Datos_Shopify_WB.md`, 4.2):

1. Mismo UPC en dos handles → duplicado real.
2. Productos distintos que comparten un UPC → colisión de captura, no duplicado: se corrige el UPC equivocado.
3. Se conserva: primero estructura de datos correcta, luego existencias, luego antigüedad.
4. **Antes de retirarlo, se mueven sus existencias** al que se conserva. Nunca se archiva ni se borra con stock.
5. El que se retira: con ventas o historial se **archiva** con SKU y código de barras prefijados `Z-`; solo un borrador sin ventas ni existencias se borra. Redirección de su handle al conservado.
6. Registro en la bitácora con los dos `ID` y el motivo.

---

## 10. Riesgos y controles

| Riesgo | Cómo se materializa | Control |
|---|---|---|
| UPC duplicado en otro handle | Recargar un estilo que ya existía | V3 bloqueante y cruce del paso 2 |
| SKU invertido | Estilo en el SKU, UPC en el barcode | V4, V5 |
| Metacampos vacíos | Importador tradicional | Solo Matrixify |
| Carga que truena por valor fuera de lista | Categoría nueva o sin acento | V8, gobierno de listas (5.4) |
| Variantes pegadas en el producto equivocado | Filas de dos estilos con el mismo Handle | V7 |
| Borrar historial e inventario | `REPLACE` | Prohibido |
| Poner inventario en cero o quitar una sucursal | Columnas de inventario en una actualización | Solo en altas y variantes nuevas |
| Publicar sin foto | Default `Active` | W1: `Draft` sin imagen |
| Cruzar contra un export viejo | Usar la exportación de la madrugada después de una carga del día | Export nuevo si hubo carga ese día |

---

## 11. Plan de trabajo y tiempos

| Etapa | Contenido | Estimado |
|---|---|---|
| E1. Visto bueno | Este procedimiento; decisiones W1 a W3 | Esta semana |
| E2. Entorno | Revisión de listas de metacampos (6.1, 6.2), columnas de `ProductsWB` (6.3), colecciones (6.4) | 0.5 día |
| E3. Primer lote bajo el flujo | La siguiente transferencia, con validador, dry run, muestra y bitácora | 0.5 día |
| E4. Pendientes | Tallas en NetSuite, homologación de tags, color de 10063824 | Continuo |

---

## 12. Checklist de cada carga

**Antes de importar**

- [ ] Todos los UPC del lote existen en el catálogo estándar de NetSuite, con talla.
- [ ] Validador en verde (16 validaciones de 7.2).
- [ ] Cruce contra `ProductsWB` del día: cada UPC clasificado (ya existe / variante faltante / nuevo).
- [ ] SKU = Barcode = UPC en todas las variantes.
- [ ] No. de Estilo en `custom.no_estilo`, no en el SKU.
- [ ] Precio = Sales Price × 1.16, termina en 9.
- [ ] Tallas MX estándar del ERP; `Default Title` en accesorios de una pieza.
- [ ] Los 8 metacampos poblados y dentro de sus listas (`Sueteres` → `Suéteres`).
- [ ] Tags con patrón `No.Estilo, Categoria, Color, Genero, Temporada, Marca`, `MERGE`.
- [ ] Handle descriptivo + No. de Estilo, que no choque con uno existente.
- [ ] Image Src del ERP si existe; si no, `Draft`.
- [ ] Carga por Matrixify, dry run sin errores.

**Después de importar**

- [ ] Archivo de resultados revisado; fallidos corregidos con `MERGE`.
- [ ] Productos creados = estilos nuevos del lote; variantes = UPC del lote.
- [ ] Nueva exportación: ningún UPC en más de un handle.
- [ ] Ninguna variante con SKU distinto de su barcode.
- [ ] 5 fichas revisadas en admin y tienda.
- [ ] Inventario en cero.
- [ ] Bitácora con número de job, rechazadas con Internal ID, productos en `Draft`.
- [ ] Aviso a Almacén (recepción), Comercial y e-commerce.

---

## 13. Bitácora y pendientes

### 13.1 Decisiones abiertas

| # | Decisión | Estado |
|---|---|---|
| W1 | Producto sin imagen entra en `Draft` | Por autorizar |
| W2 | Precio que no termina en 9 se corrige en NetSuite, no en Shopify | Por autorizar |
| W3 | Responsable único de las listas cerradas | Por designar (mismo que D3 de Odoo) |

### 13.2 Registro de lotes

| Fecha | Origen | Job Matrixify | UPC del lote | Ya existían | Variantes nuevas | Productos nuevos | Rechazados | En Draft | Notas |
|---|---|---|---|---|---|---|---|---|---|
| 16–18 sep | TO2967, TO2969 | | 1,005 | 220 | 56 (14 productos) | 165 (711 variantes) | | | Alta registrada en `Control_Datos_Shopify_WB.md`, 5.3 |

---

## Anexo A — Referencias verificadas

- Conector "Matrixify WB": exportaciones programadas diarias `ProductsWB` (03:00), `InventoryWB` y `SalesWB` (05:00). La `ProductsWB` del 22-sep exportó 587 productos.
- Comportamiento de Matrixify (documentación oficial): identifica productos por `ID` → `Handle` → `Title`; variantes por `Variant ID`, SKU, código de barras o valores de opción. `NEW` falla si existe; `MERGE` actualiza o crea; `UPDATE` falla si no existe; `REPLACE` borra y recrea. Una celda vacía en `Inventory Available: <sucursal>` quita la sucursal de la variante. El *Dry Run* no atrapa los errores de validación que devuelve Shopify.
- Reglas de datos, bitácora del 16–18 sep y pendientes: `Control_Datos_Shopify_WB.md`.
