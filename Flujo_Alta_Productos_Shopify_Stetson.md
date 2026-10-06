# Flujo de trabajo para alta de productos en Shopify · Stetson México

Procedimiento único de alta de productos en la tienda Shopify de Stetson México, bajo el Estándar de catálogo G1522.

- Empresa: Grupo Quince 22
- Tienda: `stetsonmexico` (dominio público `stetson.mx`)
- Estándar de referencia: Estándar de producto G1522 (25 campos) y su Guía de llenado
- Fecha del documento: 22 de septiembre de 2026 · versión 1.0
- Método de carga estándar: **Matrixify** (la app ya está instalada en la tienda). El importador CSV nativo de Shopify no se usa. El alta manual queda para casos de 1 a 3 productos.

Documentos que acompañan a este procedimiento:

| Documento | Para qué |
|---|---|
| `Flujo_Alta_Productos_Shopify_Stetson.svg` | Diagrama del flujo, con las fronteras y el detalle de cómo Matrixify identifica productos |
| `Flujo_Alta_Productos_Odoo_G1522.md` | El alta en Odoo, aguas arriba de este flujo. Aquí se recoge su lote cerrado |
| `Flujo_Alta_Productos_Shopify_WB.md` | El mismo flujo para Western Brothers. Ver la sección 3.4 para las diferencias entre las dos tiendas |

---

## 1. Resumen ejecutivo

**Qué se entrega.** Un procedimiento único para dar de alta productos en la tienda Shopify de Stetson México: de dónde sale el dato, cómo se normaliza al estándar, cómo se valida, cómo se cruza contra lo que ya existe, cómo se carga con Matrixify y cómo se verifica.

**Por qué hace falta.** La tienda se ha alimentado sin un camino único y el catálogo lo refleja. Medición del 22 de septiembre de 2026 sobre lo publicado en la tienda en línea (153 productos, 884 variantes):

| Indicador | Estado actual |
|---|---|
| Metacampos del estándar G1522 (`custom.no_estilo`, `custom.categoria`, etc.) | **No existen** en la tienda |
| Productos duplicados (mismo estilo en dos handles) | 1 caso confirmado: Skyline 6X, con 18 SKU repetidos entre los dos productos |
| Variantes sin SKU | 21 (todas en el producto Skyline duplicado) |
| Handles creados con el botón "Duplicar" (`-copy`, `-copia`) | 4 |
| Nombres de opción de talla distintos para lo mismo | 7 combinaciones (`Talla`, `Talla MX`, `Color / Talla`, `Talla / Color`, `Color / Perfil / Talla`…) |
| Sombreros con tallas fuera del estándar | `S`, `M`, `L`, `XL`, `CH`, `MED`, `GDE` mezclados con fracciones US |
| Tallas en minúscula | Cinturón dama, blusa dama y camisa niños (`s`, `m`, `l`) |
| Formatos de SKU distintos | 38 patrones. El dominante (código Stetson, tipo `SFPALC-48400766`) cubre 296 de 884 variantes |
| Tipos de producto (Type) | 15 valores de texto libre (`Sombrero`, `Cinturón Caballero`, `Gorra Trucker`…) y 2 vacíos |
| Etiquetas (Tags) | Sin patrón. Conviven etiquetas de colección (`ingreso-accesorios`) con frases de SEO (`stetson hecho en usa.`) |
| Variante de ejemplo revisada (Texana Palacio II 6X) | Sin código de barras |

El dato de fondo es el mismo que en Odoo: lo comercial está razonablemente bien (precio, título, imagen), pero **lo que sirve para identificar, clasificar y filtrar no tiene un estándar**. Y hay una diferencia que vuelve esto más urgente que en Odoo:

> **Shopify no valida la unicidad del SKU ni la del código de barras.** Odoo rechaza un código de barras repetido; Shopify lo acepta sin avisar. En esta tienda, todo lo que en Odoo protege el sistema lo tiene que proteger el procedimiento.

**Lo que este flujo cambia.**

1. Una sola puerta de entrada: el producto nace de un lote ya cerrado del estándar G1522 (o de la lista de una transferencia), normalizado a la plantilla Matrixify. Nada se crea a mano desde una foto o un correo, y nunca con el botón **Duplicar**.
2. Validación bloqueante *antes* de cargar, incluida la unicidad de SKU y código de barras, dentro del archivo y contra la tienda.
3. El código de barras (UPC) como llave de cruce con Odoo, NetSuite y las transferencias; el SKU como código operativo Stetson; el No. de Estilo como llave de agrupación.
4. Identificación estable en cada carga: `ID` de Shopify para actualizar, `Handle` con convención fija para crear. Es lo que impide que una recarga duplique.
5. Paridad con Western Brothers: los mismos ocho metacampos del estándar, el mismo patrón de etiquetas y la misma lógica de validación.

**Cuatro decisiones que requieren visto bueno.**

| # | Decisión | Recomendación |
|---|---|---|
| S1 | ¿Qué va en el SKU? En Western Brothers el SKU es el UPC; en Stetson el SKU es el código de artículo Stetson, que es con lo que llegan las transferencias y las listas del proveedor. | Mantener el código Stetson en el SKU (es el `default_code` del estándar) y hacer **obligatorio** el UPC en el código de barras. La llave de cruce entre sistemas es el código de barras, no el SKU. |
| S2 | Crear en Stetson los ocho metacampos del estándar que ya usa Western Brothers (`custom.no_estilo`, `custom.categoria`, etc.). | Crearlos, con la misma clave y el mismo tipo que en WB. Sin ellos, el estándar no tiene dónde vivir en esta tienda. |
| S3 | Qué va en el campo Type. Hoy es texto libre con 15 valores y probablemente alimenta colecciones automáticas y el filtro de la tienda. | Adoptar la regla de WB (`Type = División`) **solo después** de revisar qué colecciones y filtros dependen del Type (6.4). Mientras tanto, los productos nuevos llevan el Type vigente de su familia. |
| S4 | Regla de precio. Hoy todos los precios con IVA son múltiplos de 50 (563 de 884 son múltiplos de 100). | Confirmar con Comercial: `Precio Shopify = Base Price × 1.16`, redondeado al múltiplo de 50 superior. Sin regla escrita, el validador no puede revisarlo. |

---

## 2. Alcance y fronteras del flujo

### 2.1 Qué cubre

- Alta de productos nuevos (estilo nuevo), mono-talla y multi-talla.
- Alta de variantes faltantes en productos que ya existen (típico de una transferencia que trae una talla nueva).
- Completar campos vacíos de productos existentes que llegan en un lote.
- Preparación del entorno de la tienda (metacampos, nombres de opción, listas) que el alta necesita para funcionar.

### 2.2 Qué no cubre, y dónde entrega

Igual que en Odoo, cada frontera es un punto de entrega: el alta **termina** ahí y otro proceso **recoge**.

| Frontera | Dónde termina este flujo | Quién recoge | Precondición que este flujo garantiza |
|---|---|---|---|
| **Inventario** | El producto queda creado con **existencias en cero** en las tres sucursales (Eventos, Stetson Americas, Stetson México). Este flujo nunca captura cantidades. | Almacén, al recibir la transferencia (TO) en Shopify | Cada variante tiene SKU Stetson y código de barras, que es con lo que se recibe la transferencia sin captura manual |
| **Canales y colecciones** | El producto queda `Active` y publicado en Tienda online y Point of Sale | Comercial / e-commerce, para colecciones manuales, otros canales (Shop, Google) y orden de vitrina | Las etiquetas del estándar y el Type están puestos, que es de lo que cuelgan las colecciones automáticas |
| **Precios y promociones** | Queda el precio público con IVA; `Compare at price` vacío | Comercial, para rebajas y precios por mercado | El precio está cargado, es mayor a cero y cumple la regla de redondeo (S4) |
| **Contenido e imagen** | Queda la descripción y la imagen oficial si existen. Si no hay imagen, el producto se carga en `Draft` | E-commerce, para fotografía propia y textos de campaña | Está identificado qué productos quedaron en `Draft` por falta de imagen, en la bitácora del lote |
| **Corrección en origen** | Si un dato del estándar viene mal (talla vacía, color incorrecto), la fila **no entra** | Responsable de datos, que corrige en Odoo / NetSuite | La lista de filas rechazadas con su motivo |

Regla que amarra las cinco fronteras: **la bitácora del lote (7.7) es el acta de entrega.** Nadie aguas abajo actúa sobre un lote que no esté registrado como cerrado, y un lote se cierra nombrando también las filas rechazadas.

---

## 3. Arquitectura de datos

### 3.1 Los dos niveles de Shopify

Shopify, como Odoo, separa producto y variante, pero con una diferencia importante: **las variantes se crean en la misma fila de carga**, no hay que esperar a que el sistema las genere. Por eso en Shopify el alta es de **una sola pasada**, aun en estilos multi-talla.

| Nivel | Objeto | Qué es | Qué se captura aquí |
|---|---|---|---|
| Producto | Product (una o varias filas con el mismo `Handle`) | El estilo comercial. Es lo que ve el cliente en la tienda | Handle, Título, Descripción, Vendor, Type, Tags, Categoría Shopify, imagen, estado, metacampos del estándar |
| Variante | Variant (una fila por variante) | La pieza vendible: este estilo en esta talla | **SKU, código de barras, precio, valores de opción, inventario por sucursal** |

Regla de oro, la misma que en Odoo: **un estilo = un producto; una talla = una variante.** Un sombrero en 7 tallas es un producto con 7 filas, no siete productos.

### 3.2 Llaves

| Llave | Dónde vive | Para qué sirve | ¿Shopify la valida? |
|---|---|---|---|
| Código de barras (UPC) | Variante (`Variant Barcode`) | Identificador único de pieza. Llave de cruce contra Odoo, NetSuite y las TO | **No** |
| SKU (código Stetson) | Variante (`Variant SKU`) | Código operativo. Es con lo que llegan las listas del proveedor y las transferencias | **No** |
| No. de Estilo | Producto (`custom.no_estilo`, por crear) | Agrupa las variantes. Llave de cruce con el archivo del proveedor | No aplica |
| Handle | Producto | Llave de creación. Shopify **sí** exige que sea único | Sí |
| `ID` / `Variant ID` | Producto / Variante | Llave técnica de actualización. Es el equivalente del `id` externo de Odoo | Sí (lo asigna Shopify) |

Patrón observado en los texanos: el SKU Stetson codifica el estilo y la talla. `SFPALC-48400766` = modelo `SFPALC` + perfil `4840` + color `07` + talla `66` (6 3/4). Las tallas vistas: `66` = 6 3/4, `67` = 6 7/8, `72` = 7 1/4, `74` = 7 1/2. Es decir, **en sombrero el No. de Estilo es el SKU sin los dos últimos dígitos** (`SFPALC-484007`). Es una regla útil para cruzar, pero hay que confirmarla con el proveedor antes de usarla para derivar datos: hoy solo 296 de 884 variantes siguen este patrón.

### 3.3 Fuentes de datos

1. **Lote cerrado del alta en Odoo** bajo el estándar G1522. Es la fuente del dato de catálogo (No. de Estilo, División, Categoría, Color, Composición, etc.). El flujo de Odoo declara a Shopify como su frontera de publicación: aquí se recoge.
2. **Lista del proveedor o de la transferencia (TO)**: SKU, código de barras y cantidad de lo que llega. Es la fuente de *qué* hay que dar de alta. La cantidad **no** se carga (frontera de inventario).
3. **Fuentes oficiales de Stetson** (catálogo del proveedor y sitio de Stetson) para descripción e imagen cuando el lote no las trae. Nunca se inventa un dato comercial.
4. **Export de la tienda** con Matrixify: el catálogo actual con `ID`, `Handle`, `Variant ID`, `Variant SKU`, `Variant Barcode` y metacampos. Es contra lo que se cruza.
5. **Hoja "Criterios"** de la plantilla estándar: listas cerradas de División, Género, Categoría, Color, Temporada.

Cuando el lote de Odoo y la lista del proveedor difieren en un dato de catálogo, gana el estándar (Odoo / NetSuite) y se levanta la corrección con el proveedor.

### 3.4 Diferencias con Western Brothers

Las dos tiendas siguen el mismo estándar y el mismo flujo. Las diferencias son de convención y están decididas a propósito:

| Tema | Stetson México | Western Brothers |
|---|---|---|
| SKU | Código de artículo Stetson (decisión S1) | UPC |
| Código de barras | UPC | UPC (el mismo valor que el SKU) |
| Precio con IVA | Múltiplo de 50 (regla por confirmar, S4) | Termina en 9 |
| Metacampos del estándar | Por crear (S2) | Existen los ocho |
| Type | Texto libre por familia, por migrar (S3) | División |
| Sucursales | Eventos, Stetson Americas, Stetson México | Eventos WB, Western Brothers Mexico, Western Brothers Outlet Lerma |
| Matrixify | Desde la app en el admin (sin conector para Claude) | App y conector "Matrixify WB" |

---

## 4. Diccionario de campos: Estándar G1522 → Shopify (Matrixify)

Correspondencia de los 25 campos del estándar con las columnas de la plantilla Matrixify. "Nivel" dice si la columna va en la primera fila del producto o en cada fila de variante.

| # | Campo del estándar | Columna Matrixify | Nivel | Regla de captura |
|---|---|---|---|---|
| 1 | No. Estilo | `Metafield: custom.no_estilo [single_line_text_field]` | Producto | Tal cual viene del estándar. Nunca en el SKU ni en el título |
| 2 | Talla | `Option1 Name` = `Talla` · `Option1 Value` | Variante | Valor estándar de la familia (5.3). Mono-talla: `Option1 Name` = `Title`, `Option1 Value` = `Default Title` |
| 3 | SKU | `Variant SKU` | Variante | Código de artículo Stetson (S1). Sin espacios. Único en la tienda |
| 4 | Código de barras | `Variant Barcode` | Variante | UPC completo, **como texto**, con ceros a la izquierda. Obligatorio. Único en la tienda |
| 5 | Marca | `Vendor` | Producto | `Stetson` (ver 6.3: hoy dice `Stetson México`, que es el nombre de la tienda, no la marca) |
| 6 | Nombre | `Title` | Producto | Ver 5.8 |
| 7 | Descripción | `Body HTML` (primer párrafo) | Producto | Una línea comercial |
| 8 | División | `Metafield: custom.division` (y `Type`, según S3) | Producto | Accesorios, Ropa, Denim, Calzado |
| 9 | Género | `Metafield: custom.genero` | Producto | Hombre, Mujer, Niño, Niña, Unisex |
| 10 | Categoría | `Metafield: custom.categoria` | Producto | Lista cerrada, igual a la del estándar (39 categorías). Solo el nombre de la categoría, sin la división: `Sombreros`, no `Accesorios / Sombreros` |
| 11 | Temporada | `Metafield: custom.temporada` | Producto | SS26 … FW28 |
| 12 | Licencia | `Metafield: custom.licencia` | Producto | Normalmente `Stetson` |
| 13 | Composición | `Metafield: custom.composicion` | Producto | Como la declara el proveedor. En fieltro, incluir la calidad (`Fieltro de pelo 6X`) |
| 14 | Color | Etiqueta del estándar + metacampo de categoría Shopify `Color` | Producto | Color normalizado del estándar (13 valores). El nombre comercial (`Silver Sand`, `Acorn`) va en el título, no aquí |
| 15 | Fit | — | — | No aplica en la tienda. Se omite |
| 16 | Silueta | `Body HTML` (bloque de características) | Producto | En sombrero: copa y ala (`Copa Cattleman 4 5/8", ala 4"`) |
| 17 | Lifecycle | `Metafield: custom.lifecycle` | Producto | `Seasonal` por omisión; `CORE` en línea permanente |
| 18 | Descripción detallada | `Body HTML` | Producto | Texto de venta largo con el bloque de características al final, igual que en Odoo |
| 19 | Unidad de medida | — | — | No aplica en Shopify |
| 20 | País de origen | `Variant Country of Origin` | Variante | Código ISO de dos letras (`US`, `MX`). Shopify pide código, no nombre |
| 21 | Clave SAT | — | — | Vive en Odoo / NetSuite. Shopify no factura |
| 22 | Unidad SAT | — | — | Igual |
| 23 | MAYOREO | — | — | No se publica |
| 24 | Base Price (sin IVA) | — | — | Sirve para calcular el precio; no se carga |
| 25 | RETAIL (con IVA) | `Variant Price` | Variante | Precio público con IVA, con la regla de redondeo de S4 |

Columnas operativas que no son del estándar pero se llenan en el alta (valores fijos, sección 7.4): `Handle`, `Command`, `Tags`, `Tags Command`, `Status`, `Published`, `Published Scope`, `Image Src`, `Image Command`, `Variant Command`, `Variant Taxable`, `Variant Inventory Tracker`, `Variant Inventory Policy`, `Variant Fulfillment Service`, `Variant Requires Shipping`, `Variant Weight`, `Variant Weight Unit`, las tres columnas `Inventory Available: <sucursal>` y la categoría de la taxonomía de Shopify (columna `Category`, que acepta el nombre, la ruta completa o el ID de la taxonomía).

> **Categoría de Shopify ≠ Categoría del estándar.** Shopify tiene su propia taxonomía (por ejemplo `Sombreros de vaquero`), con metacampos propios (Color, Tejido, Sexo objetivo, Grupo de edad). Sirve para impuestos, Google y filtros. Se asigna por categoría del estándar con una tabla fija (6.5), no producto por producto.

---

## 5. Reglas y convenciones

El incumplimiento de cualquiera es un hallazgo de auditoría y se corrige antes de cerrar el lote.

### 5.1 Producto con variantes vs. productos independientes

- Un estilo en varias **tallas** es un producto con la opción `Talla`. Nunca un producto por talla.
- Un estilo en varios **colores**: si el proveedor le da un No. de Estilo (o código) distinto a cada color, es un producto por color, con el color en el título. En Stetson es lo normal: el color va dentro del código (`…07…` en el ejemplo de 3.2). Por eso la opción `Color` **no** se usa en productos nuevos, salvo que el estándar agrupe los colores bajo un mismo No. de Estilo.
- El producto mono-talla (gorra, cartera, hebilla, pluma) lleva `Option1 Name = Title` y `Option1 Value = Default Title`.

### 5.2 SKU y código de barras

- SKU = código de artículo Stetson; código de barras = UPC. Nunca al revés, nunca el No. de Estilo en ninguno de los dos.
- Los dos son únicos en toda la tienda. Como Shopify no lo impide, lo revisa el validador (7.2) y el cruce (7.3).
- Una variante sin código de barras no entra al lote: se registra en la bitácora para el proceso de GTIN (frontera de corrección en origen).

### 5.3 Tallas

El nombre de la opción es siempre **`Talla`**. No `Talla MX` (los sombreros no se miden en MX), no `Size`, no `Tamaño`.

| Familia | Valores estándar | Hoy se ve también |
|---|---|---|
| Sombreros (fieltro y palma) | `6 1/2` … `8` en fracción US, con espacio: `7 1/4` | `S`, `M`, `L`, `XL`, `CH`, `MED`, `GDE`, `Unitalla`, y la opción llamada `Talla MX` |
| Ropa (camisa, blusa, playera, sudadera) | `XS`, `S`, `M`, `L`, `XL`, `2XL`, `3XL` | Minúsculas (`s`, `m`, `l`) |
| Cinturones | `32` … `46` en caballero; `S`, `M`, `L`, `XL` en dama | Minúsculas en dama |
| Calzado | Talla MX (`MX = US + 20`) | — |
| Accesorio de una pieza | `Default Title` | `Unitalla` como valor de opción |

Mapa de equivalencias para normalizar lo que llega:

| Llega así | Valor estándar |
|---|---|
| `CH` / `Chica` · `MED` / `Mediana` · `GDE` / `Grande` | `S` · `M` · `L` |
| `s`, `m`, `l`, `xl` | `S`, `M`, `L`, `XL` |
| `7 1/4"` o `7-1/4` | `7 1/4` |
| `Unitalla`, `Talla única`, `O/S` en accesorio | `Default Title` |
| Sombrero en `S`/`M`/`L` (tallas de palma o gorra flexible) | Se deja en alfa **solo** si el proveedor no da fracción; se anota en la bitácora |

### 5.4 Color

- La etiqueta y el metacampo de categoría `Color` llevan el color **normalizado** del estándar: Rojo, Azul, Amarillo, Verde, Naranja, Morado, Rosa, Negro, Blanco, Gris, Beige, Cafe, Varios.
- El nombre comercial Stetson (`Silver Sand`, `Acorn`, `Chocolate`, `Visón`) va en el **título**. Si se quiere mostrar en inglés y español, así: `Bellota (Acorn)`, que ya es la práctica en la tienda.

### 5.5 Precios

- `Variant Price` es el precio público **con IVA**: `Base Price × 1.16`, redondeado según S4.
- El `Base Price` del estándar es sin IVA y no se carga en Shopify.
- `Compare at price` se deja vacío en el alta. Las rebajas son de Comercial (frontera de precios).
- `Variant Taxable = TRUE` siempre.
- Todas las variantes de un estilo llevan el mismo precio, salvo indicación de Comercial (hoy solo 2 productos tienen precios distintos por talla).
- Ningún producto se publica con precio en cero.

### 5.6 Type, Categoría y División

- `custom.categoria` es lista cerrada con los mismos valores que la Categoría del estándar. Si llega un valor que no está, la fila truena: se levanta con el responsable de datos y la fila queda fuera del lote (igual que en Odoo, 5.9).
- `custom.division` es lista cerrada de cuatro valores.
- `Type`: ver decisión S3. Mientras no se migre, un producto nuevo toma el Type **ya existente** de su familia (`Sombrero`, `Cinturón Caballero`, `Gorra Trucker`…). No se crean Types nuevos.

### 5.7 Etiquetas (Tags)

Patrón del estándar, idéntico a Western Brothers, con `Tags Command = MERGE`:

`No.Estilo, Categoría, Color, Género, Temporada, Marca`

Ejemplo: `SFPALC-484007, Sombreros, Negro, Unisex, FW26, Stetson`

- `MERGE` agrega sin borrar: las etiquetas que hoy usan las colecciones (`ingreso-accesorios`, `western`, `fieltro`) se conservan.
- No se usan frases de SEO como etiqueta (`stetson hecho en usa.`). El SEO va en el título SEO y la descripción, no en las etiquetas.
- Antes de agregar una etiqueta de colección nueva, se revisa que no dispare una colección automática que no se quería (6.4).

### 5.8 Título, handle y descripción

- **Título**: `Tipo + Stetson + Modelo + Calidad + Color`. Ejemplo: `Texana Stetson Palacio II 6X Negro`. Es el patrón que ya siguen los texanos recientes. Sin el No. de Estilo, sin `| Stetson®`, sin códigos.
- **Handle**: slug del título + No. de Estilo. Ejemplo: `texana-stetson-palacio-ii-6x-negro-sfpalc-484007`. Nunca `-copy`, `-copia`, `-1`, `-2`: esos sufijos delatan un duplicado.
- **Descripción** (`Body HTML`): párrafo comercial + bloque de características al final (Marca, Modelo, Color, Copa y ala o Silueta, Composición, Talla, País de origen), el mismo formato que la Descripción detallada de Odoo.

### 5.9 Imagen y estado

- `Image Src` = enlace de imagen oficial del lote, en la primera fila del producto, `Image Command = MERGE`.
- Producto sin imagen: `Status = Draft`. Se anota en la bitácora (frontera de contenido). Un producto sin foto no se publica.
- Producto completo: `Status = Active`, `Published = TRUE`, `Published Scope = global` (Tienda online y Point of Sale).

### 5.10 Lo que nunca se hace

- **Nunca el botón "Duplicar"** de Shopify para crear un producto parecido. Copia SKU, código de barras y etiquetas, y genera handles `-copy`. Es el origen de los 4 handles `-copy/-copia` que hay hoy.
- **Nunca `Command = REPLACE` ni `Variant Command = REPLACE`.** Borran y recrean el producto o sus variantes: se pierde el `Variant ID`, el historial de ventas por variante y las existencias por sucursal.
- **Nunca `NEW` para completar un alta que falló a medias.** Se usa `MERGE` con el mismo Handle.

---

## 6. Preparación del entorno (una sola vez, antes del primer lote)

### 6.1 Metacampos del estándar (decisión S2)

Ruta: Configuración → Metacampos y metaobjetos → Productos → Agregar definición.

La tienda hoy solo tiene definiciones de apps y de Google (`Tipo de producto`, `Stockyphi Meta`, `Stockyphi Managed`, `Related products`…). Se crean las ocho del estándar, con **la misma clave que en Western Brothers**, para que un mismo archivo y un mismo validador sirvan para las dos tiendas:

| Nombre | Clave | Tipo | Validación |
|---|---|---|---|
| No. de Estilo | `custom.no_estilo` | Texto de una sola línea | — |
| Categoría | `custom.categoria` | Texto de una sola línea | **Lista de valores** = las 39 categorías del estándar |
| División | `custom.division` | Texto de una sola línea | Lista: Accesorios, Ropa, Denim, Calzado |
| Género | `custom.genero` | Texto de una sola línea | Lista: Hombre, Mujer, Niño, Niña, Unisex |
| Temporada | `custom.temporada` | Texto de una sola línea | Lista: SS26 … FW28 |
| Lifecycle | `custom.lifecycle` | Texto de una sola línea | Lista: Seasonal, CORE |
| Composición | `custom.composicion` | Texto de una sola línea | — |
| Licencia | `custom.licencia` | Texto de una sola línea | — |

Antes de crearlas, exportar las definiciones de WB y copiar exactamente el tipo y los valores de lista. Lección ya aprendida en WB: la lista tenía `Chaquetas` y el estándar decía `Chamarras`, y la carga tronó. Aquí se crean desde el principio con los valores del estándar, **con acento** donde el estándar lo lleva (`Suéteres`).

El metacampo `Tipo de producto` que hoy existe (159 productos) queda como está; no es del estándar. Se revisa en la limpieza (sección 9).

### 6.2 Plantilla de exportación guardada

En Matrixify, crear y guardar una exportación de Productos llamada `CruceStetson` con las columnas: `ID`, `Handle`, `Title`, `Type`, `Tags`, `Status`, `Variant ID`, `Variant SKU`, `Variant Barcode`, `Option1 Name`, `Option1 Value`, `Option2 Name`, `Option2 Value`, `Variant Price` y los metacampos `custom.*`. Es el archivo del paso 2 y el respaldo de cada carga. Conviene programarla diaria, como ya se hace en WB.

### 6.3 Vendor

Todos los productos dicen `Stetson México` (151) o `Generico` (2): es el nombre de la tienda, no la marca. El estándar pide la marca: `Stetson`. Se cambia en bloque con una carga de `ID` + `Vendor` (verificar antes que ninguna colección automática filtre por Vendor).

### 6.4 Colecciones, filtro y apps que leen el catálogo

Antes de tocar Type, Tags o Vendor en productos existentes, y antes del primer lote:

1. Exportar con Matrixify las **Colecciones** (automáticas) con sus condiciones. Anotar cuáles filtran por Type, Tag o Vendor.
2. Revisar el filtro de la tienda (el índice "Smart Products Filter", que aparece como colección y dice *Do not delete*): qué campos usa para filtrar.
3. Revisar la app **Stockyphi**: marca 440 productos como gestionados (`Stockyphi Managed`). Hay que confirmar qué sincroniza (inventario, precio, catálogo). Si escribe precio o inventario, puede sobrescribir lo que se cargue; si crea productos, es una segunda puerta de entrada que rompe la regla 1 de este flujo.

Hasta cerrar este punto, las cargas **solo agregan** (Tags con `MERGE`, Type existente de la familia) y no cambian nada de lo que ya usan colecciones y apps.

### 6.5 Tabla Categoría del estándar → Categoría Shopify

Una tabla fija, por categoría del estándar, con la categoría de la taxonomía Shopify que le corresponde. Ejemplos: `Sombreros → Sombreros de vaquero`, `Gorras → Gorras de béisbol`, `Cinturones → Cinturones`, `Carteras → Carteras y tarjeteros`, `Camisas → Camisas`. Se arma una vez con las 39 categorías y se usa en todo lote.

### 6.6 Nombres de opción

Todo producto nuevo usa `Talla` (5.3). Los productos existentes con `Talla MX`, `Talla / Color` o `Color / Perfil / Talla` se corrigen en la limpieza (sección 9), no en el alta.

---

## 7. Procedimiento A — Alta masiva con Matrixify

Es el camino principal. Un lote es un lote cerrado de Odoo o una transferencia: una marca, un origen.

### 7.1 Paso 0 — Armar el archivo del lote

1. Partir del lote cerrado del estándar G1522 (la plantilla o el export de Odoo) y, si el alta viene de una transferencia, de la lista de la TO con SKU y código de barras.
2. Filtrar solo los códigos de barras que hay que dar de alta. Si la lista de la TO trae SKU que no están en el estándar, **no se dan de alta con datos inventados**: se piden al proveedor o se completan de la fuente oficial Stetson, y se pasan primero por el estándar.
3. Pasar a la plantilla Matrixify: **una fila por variante** (por código de barras). La primera fila de cada producto lleva los datos de producto; las demás pueden repetirlos.
4. Código de barras como **texto**. Tallas y colores al estándar (5.3, 5.4). Precio con IVA según S4.

### 7.2 Paso 1 — Validación previa (bloqueante)

**El problema.** En Odoo, un código de barras repetido detiene la carga. En Shopify es peor: **no la detiene**. Si el archivo trae dos filas con el mismo código de barras, o un código que ya está en otro producto de la tienda, Shopify lo acepta y el error se descubre semanas después, cuando una transferencia se recibe en el producto equivocado o el punto de venta escanea una pieza y aparece otra. Es exactamente lo que pasó con Skyline 6X: dos productos del mismo estilo, 18 SKU repetidos, y 21 variantes sin SKU en uno de ellos.

**La solución.** Una validación que corre siempre, antes de abrir Matrixify, con dos mitades:

- **Interna** (el archivo contra sí mismo): lo que hace el validador de Odoo.
- **Externa** (el archivo contra el export de la tienda del paso 2): lo que en Odoo hace el sistema y aquí no hace nadie.

Las 16 validaciones:

| # | Revisa | Por qué importa |
|---|---|---|
| V1 | Código de barras presente, texto de 12 a 14 dígitos | Sin ceros perdidos, coincide con la etiqueta y con Odoo |
| V2 | Código de barras único **dentro del archivo** | Shopify no lo detiene |
| V3 | Código de barras que **no existe en otro producto** de la tienda | Es el duplicado silencioso. Si existe en el mismo Handle, es actualización (7.3) |
| V4 | SKU presente y único dentro del archivo | Igual |
| V5 | SKU que no existe en otro producto de la tienda | Igual |
| V6 | No. de Estilo presente | Es la llave de agrupación y va en `custom.no_estilo` |
| V7 | Todas las filas de un mismo Handle tienen el mismo No. de Estilo | Evita pegar variantes de dos estilos en un producto (el caso "Camisa REAL Billie" de WB) |
| V8 | `custom.categoria` en la lista cerrada, **escrita exactamente igual** (acentos incluidos) | Valor fuera de lista = fila rechazada por Shopify |
| V9 | `custom.division`, `custom.genero`, `custom.temporada`, `custom.lifecycle` en su lista | Igual |
| V10 | Categoría consistente con División | Mismo mapa de la hoja Criterios que en Odoo |
| V11 | `Option1 Name` = `Talla` (o `Title` en mono-talla) y valor en la lista de la familia | Evita `Talla MX`, `CH`, minúsculas |
| V12 | Combinación de opciones única dentro del Handle | Shopify rechaza dos variantes con la misma talla |
| V13 | Precio mayor a cero, con la regla de redondeo S4 | Evita precios sin IVA o sin redondeo |
| V14 | Handle con la convención 5.8 y **sin** sufijo `-copy`, `-copia`, `-1` | Detecta duplicados de origen |
| V15 | Handle nuevo que no existe ya en la tienda con otro estilo | `NEW` fallaría; `MERGE` sobrescribiría otro producto |
| V16 | `Image Src` presente; si no, `Status = Draft` | Ningún producto sin foto se publica |

El validador puede ser la misma hoja de Excel del flujo de Odoo, con una pestaña adicional para el export de la tienda, o el script del Anexo B. El resultado es el mismo: semáforo `LISTO PARA CARGAR` / `NO CARGAR` y una columna `MOTIVO` por fila.

### 7.3 Paso 2 — Cruce contra la tienda: tres rutas

Correr la exportación guardada `CruceStetson` (6.2). Cruzar cada fila del archivo por **código de barras** y, si no hay coincidencia, por **SKU**:

| Resultado del cruce | Situación | Qué se hace | Command |
|---|---|---|---|
| El código de barras (o SKU) ya existe | La pieza ya está en la tienda | **No se da de alta.** Solo se completan campos vacíos (metacampos, etiquetas), usando el `ID` y el `Variant ID` del export | `UPDATE` |
| No existe la pieza, pero el No. de Estilo sí (mismo producto) | Falta una talla | Se agrega la variante al Handle existente | `MERGE` + `Variant Command = MERGE` |
| Ni la pieza ni el estilo existen | Estilo nuevo | Producto nuevo | `NEW` |

Dos detalles del cruce en esta tienda:

- Como hoy no existe `custom.no_estilo`, el "estilo ya existe" se detecta por el **prefijo del SKU** (en sombrero, el SKU sin los dos últimos dígitos, ver 3.2) y por el título. Cuando la limpieza cargue el No. de Estilo en el catálogo, el cruce pasa a ser directo.
- Si el código de barras aparece en **dos** productos de la tienda, la fila no entra: es un duplicado previo y se resuelve primero con el árbol de decisión de la sección 9.

### 7.4 Paso 3 — Estructura del archivo

Columnas, en este orden (plantilla idéntica a la de WB, con las sucursales de Stetson):

```
ID, Handle, Command, Title, Body HTML, Vendor, Type, Tags, Tags Command,
Status, Published, Published Scope, Category,
Image Src, Image Command,
Variant ID, Variant Command, Option1 Name, Option1 Value,
Variant SKU, Variant Barcode, Variant Price, Variant Taxable,
Variant Inventory Tracker, Variant Inventory Policy,
Variant Fulfillment Service, Variant Requires Shipping,
Variant Weight, Variant Weight Unit, Variant Country of Origin,
Inventory Available: Eventos, Inventory Available: Stetson Americas,
Inventory Available: Stetson México,
Metafield: custom.no_estilo [single_line_text_field],
Metafield: custom.categoria [single_line_text_field],
Metafield: custom.division [single_line_text_field],
Metafield: custom.genero [single_line_text_field],
Metafield: custom.temporada [single_line_text_field],
Metafield: custom.lifecycle [single_line_text_field],
Metafield: custom.composicion [single_line_text_field],
Metafield: custom.licencia [single_line_text_field]
```

Valores fijos por omisión: `Vendor` = `Stetson`, `Tags Command` = `MERGE`, `Image Command` = `MERGE`, `Status` = `Active` (o `Draft` sin imagen), `Published` = `TRUE`, `Published Scope` = `global`, `Variant Taxable` = `TRUE`, `Variant Inventory Tracker` = `shopify`, `Variant Inventory Policy` = `deny`, `Variant Fulfillment Service` = `manual`, `Variant Requires Shipping` = `TRUE`, `Variant Weight` = `0`, `Variant Weight Unit` = `kg`, inventario `0` en las tres sucursales.

Reglas del archivo:

- **En altas nuevas, `ID` y `Variant ID` van vacíos.** Shopify los asigna.
- **En actualizaciones, `ID` y `Variant ID` salen del export y no se editan.** Es la regla equivalente a la columna `id` de Odoo: con el `ID`, Matrixify encuentra el producto aunque cambie el Handle o el título; sin él, lo busca por Handle y luego por Título, y si no lo encuentra con `MERGE`, **crea uno nuevo**.
- Los nombres de las columnas de inventario deben coincidir **exactamente** con el nombre de la sucursal en Shopify (`Inventory Available: Stetson México`, con acento).

> Nota sobre el inventario en cero: la columna `Inventory Available` con `0` en una **actualización** pone en cero las existencias reales. Solo se incluye en filas `NEW` y en variantes nuevas. En filas `UPDATE` las columnas de inventario **se quitan del archivo**: ni en cero ni vacías, porque una celda vacía en `Inventory Available` le quita esa sucursal a la variante.

### 7.5 Paso 4 — Carga en tres tiempos

Ruta: Apps → Matrixify → Import → subir el archivo.

1. **Dry run.** En las opciones de la importación, marcar *Dry Run* y ejecutar. Matrixify revisa la estructura y simula la carga sin escribir nada. Revisar el archivo de resultados. (El dry run no detecta todo: los errores de validación de Shopify, como un valor fuera de la lista del metacampo, aparecen hasta la carga real. Por eso el paso 1 es bloqueante.)
2. **Muestra.** Cargar solo 5 productos (de preferencia uno multi-talla y uno mono-talla). Revisarlos en el admin y en la tienda contra el checklist (sección 12).
3. **Resto del lote**, en este orden: primero los `NEW`, luego las variantes faltantes (`MERGE`), al final las actualizaciones (`UPDATE`).

Después de cada importación, descargar el **archivo de resultados** de Matrixify. Cada fila trae su resultado y su comentario. Lo que falló se corrige y se reimporta **con `MERGE` y el mismo Handle**, nunca con `NEW`.

### 7.6 Variantes faltantes en un producto existente

Es el caso más común de las transferencias: llega una talla que el producto no tenía.

1. Del export, tomar el `Handle` del producto (o su `ID`).
2. Una fila por talla nueva: `Handle`, `Command = MERGE`, `Variant Command = MERGE`, `Option1 Name = Talla`, `Option1 Value`, `Variant SKU`, `Variant Barcode`, `Variant Price` y los valores fijos de variante. Sin columnas de producto que no se quieran cambiar.
3. El nombre de la opción debe ser **idéntico** al del producto existente. Si el producto usa `Talla MX` y la fila dice `Talla`, la carga falla o crea un desorden de opciones. En esos productos primero se corrige el nombre de opción (limpieza) y luego se agrega la variante.
4. Matrixify busca la variante por `Variant ID`, SKU, código de barras o valores de opción; si no la encuentra, la agrega. Por eso el paso 1 exige que el SKU y el código de barras no existan en otro lado.

### 7.7 Paso 5 — Cierre del lote

- Inventario en cero en las tres sucursales.
- Estado `Active` y publicado en Tienda online y POS, o `Draft` con motivo.
- Registrar el lote en la bitácora (sección 13): origen (lote de Odoo o TO), productos nuevos, variantes nuevas, actualizaciones, filas rechazadas con motivo, productos en `Draft` y por qué, número del job de Matrixify.
- Guardar junto a la bitácora el archivo cargado y el archivo de resultados de Matrixify.

---

## 8. Procedimiento B — Alta manual (1 a 3 productos)

La regla es la misma: los datos salen del estándar o de la fuente oficial Stetson, no de la memoria. **Nunca se parte de "Duplicar"**.

1. Productos → **Agregar producto**.
2. Título (5.8), Descripción con el bloque de características, Multimedia (imagen oficial).
3. Categoría (taxonomía Shopify, tabla 6.5) y sus metacampos de categoría (Color, Tejido, Sexo objetivo).
4. Tipo de producto (S3), Proveedor = `Stetson`, Etiquetas con el patrón 5.7.
5. Variantes: **Agregar opción** → nombre `Talla` → los valores de la familia. Shopify genera una variante por valor.
6. Abrir cada variante y capturar **SKU**, **Código de barras**, precio y País de origen. Este es el paso que más se olvida: la Texana Palacio II 6X revisada tiene SKU pero no código de barras.
7. Inventario en cero; "Vender sin existencias" desactivado.
8. Metacampos del estándar en la parte inferior de la ficha (una vez creados, 6.1).
9. Revisar la vista de búsqueda (título SEO y URL = handle con la convención 5.8) y guardar.
10. Correr el checklist de la sección 12 y anotar en la bitácora.

---

## 9. Corrección del catálogo ya cargado

El alta nueva sale limpia desde el primer lote. Lo ya cargado se corrige por barrido (plan completo en `Propuesta_Limpieza_Catalogo_Shopify.md`), con el mismo método: **exportar con `ID` y `Variant ID` → corregir → reimportar con `UPDATE`**, y respaldo antes de cada carga.

| Hallazgo | Volumen | Acción | Prioridad |
|---|---|---|---|
| Skyline 6X duplicado (`skyline-6x-7240-stetson-r` y `sombrero-skyline-6x-cowboy-stetson-r`) | 2 productos, 18 SKU repetidos, 21 variantes sin SKU | Árbol de decisión abajo | Alta |
| Handles `-copy` / `-copia` | 4 | Revisar si son duplicado real. Si no, corregir el handle (Matrixify crea la redirección del viejo al nuevo) | Alta |
| Variantes sin código de barras | Por medir con el export completo | Cruzar por SKU contra la lista del proveedor / Odoo y cargar con `Variant ID` | Alta |
| Metacampos del estándar vacíos | Todos (se acaban de crear) | Carga por `ID`, desde Odoo por código de barras | Media |
| Nombres de opción distintos a `Talla` | ~50 productos (`Talla MX`, `Color / Talla`…) | Renombrar la opción por producto. Renombrar **no** recrea variantes; quitar o agregar una opción sí | Media |
| Tallas fuera del estándar (`CH`, `MED`, `GDE`, minúsculas) | Sombreros, cinturón dama, blusa, camisa niños | Cambiar el **valor** de la opción por `Variant ID` | Media |
| Vendor `Stetson México` | 151 | Carga por `ID` a `Stetson` (6.3) | Media |
| Etiquetas sin patrón | Casi todo el catálogo | Agregar las del estándar con `MERGE`. Retirar las frases SEO con `Tags Command = DELETE`, después de revisar colecciones | Baja |
| Type sin estándar | 15 valores | Según S3, después de 6.4 | Baja |

**Árbol de decisión para duplicados** (mismo criterio que WB y que Odoo):

1. ¿Comparten código de barras? → Duplicado real.
2. ¿Tienen códigos de barras distintos y el mismo SKU? → No es duplicado: error de captura. Se corrige el SKU equivocado.
3. En duplicado real, se conserva el producto por este orden: estructura de datos correcta → existencias → ventas → el más antiguo.
4. **Antes de borrar el otro, se mueven sus existencias** con un ajuste o transferencia documentada. Un producto borrado se lleva su inventario.
5. El duplicado con ventas o historial se **archiva** (`Archived`) con SKU y código de barras prefijados `Z-`, igual que en Odoo; solo un borrador sin ventas ni existencias se borra. Se crea una redirección de su handle al que se conserva.
6. Se registra en la bitácora: los dos `ID`, cuál se conservó y por qué.

El plan completo de limpieza, con olas, tablero de métricas y rutina de mantenimiento, va en `Propuesta_Limpieza_Catalogo_Shopify.md`.

---

## 10. Riesgos y controles

| Riesgo | Cómo se materializa | Control |
|---|---|---|
| Duplicar un producto | Crear con `NEW` o `MERGE` un estilo que ya estaba con otro handle; o usar "Duplicar" | Cruce del paso 2 (V3, V5, V15); nunca "Duplicar" |
| Código de barras o SKU repetido | Shopify no lo valida | V2 a V5, bloqueantes |
| Borrar variantes e historial | `REPLACE`, o quitar/agregar una opción a un producto con ventas | Prohibido `REPLACE`; opciones solo se **renombran** en productos existentes |
| Poner inventario en cero sin querer | Dejar `Inventory Available: … = 0` en una actualización | Las columnas de inventario solo en filas `NEW` y variantes nuevas |
| Valor fuera de lista en metacampo | El estándar trae una categoría que la lista de Shopify no tiene, o sin acento | V8, listas creadas con los valores exactos del estándar (6.1) |
| Romper una colección o el filtro | Cambiar Type, Vendor o etiquetas de las que cuelga una colección automática | Revisión de 6.4 antes; Tags siempre con `MERGE` |
| Una app sobrescribe lo cargado | Stockyphi u otra app sincroniza precio, inventario o catálogo | Confirmar su alcance (6.4) antes del primer lote |
| Publicar sin foto o sin precio | Carga con `Active` por omisión | V13, V16: sin imagen va `Draft` |
| Opción con nombre distinto al del producto | Agregar una talla con `Talla` a un producto con `Talla MX` | 7.6, paso 3 |

---

## 11. Plan de trabajo y tiempos

| Etapa | Contenido | Estimado |
|---|---|---|
| E1. Documento y visto bueno | Este procedimiento; decisiones S1 a S4 | Esta semana |
| E2. Preparación del entorno | Export completo de la tienda y medición; 8 metacampos; exportación guardada; revisión de colecciones, filtro y Stockyphi; tabla de categorías Shopify | 1.5 días |
| E3. Lote piloto | El siguiente lote o transferencia de sombreros (multi-talla), completo con dry run, muestra y bitácora | 0.5 día |
| E4. Correcciones de prioridad alta | Skyline duplicado, handles `-copy`, variantes sin código de barras | 1 a 2 días |
| E5. Barrido del estándar | Metacampos, opciones y tallas, Vendor, etiquetas, Type | Continuo, por familia |

El flujo queda operativo al terminar E2. E4 y E5 corren en paralelo a las altas nuevas.

---

## 12. Checklist de cada carga

**Antes de importar (sobre el archivo)**

- [ ] Los productos vienen de un lote cerrado del estándar (o de una TO pasada por el estándar), no de datos sueltos.
- [ ] Validador corrido, semáforo en verde (las 16 validaciones de 7.2).
- [ ] Cruce contra el export de la tienda hecho: cada fila clasificada como ya existe / variante faltante / estilo nuevo.
- [ ] Código de barras presente y único, en el archivo y en la tienda.
- [ ] SKU = código Stetson, único, en el archivo y en la tienda.
- [ ] `Option1 Name` = `Talla` (o `Title` / `Default Title` en mono-talla), valores de la familia.
- [ ] Precio con IVA según la regla S4.
- [ ] Metacampos del estándar llenos y dentro de sus listas.
- [ ] Etiquetas con el patrón, `Tags Command = MERGE`.
- [ ] Handle con la convención, sin `-copy`.
- [ ] Inventario en cero solo en filas nuevas; sin columnas de inventario en actualizaciones.
- [ ] Dry run sin errores.
- [ ] Respaldo (export) del subconjunto a tocar, si es actualización.

**Después de importar (en Shopify)**

- [ ] Archivo de resultados de Matrixify descargado; cero filas fallidas o todas explicadas.
- [ ] Productos creados = estilos del lote; variantes creadas = códigos de barras del lote.
- [ ] Ninguna variante sin SKU ni sin código de barras.
- [ ] Ningún código de barras ni SKU repetido en la tienda (export nuevo, agrupar y contar).
- [ ] 5 fichas revisadas en el admin y en la tienda: título, precio, tallas, imagen, metacampos.
- [ ] Los productos nuevos aparecen en las colecciones y el filtro donde deben.
- [ ] Inventario en cero.
- [ ] Lote en la bitácora, con filas rechazadas, productos en `Draft` y número de job.
- [ ] Aviso de entrega aguas abajo: Almacén (ya se puede recibir la TO), Comercial (precios y promociones), e-commerce (colecciones, fotos pendientes).

---

## 13. Bitácora y pendientes

### 13.1 Decisiones abiertas

| # | Decisión | Estado |
|---|---|---|
| S1 | SKU = código Stetson; código de barras obligatorio como llave de cruce | Por autorizar |
| S2 | Crear los 8 metacampos del estándar con las claves de WB | Por autorizar |
| S3 | Type = División, después de revisar colecciones y filtro | Por autorizar |
| S4 | Regla de precio con IVA (múltiplo de 50) | Por confirmar con Comercial |
| S5 | Alcance de la app Stockyphi (440 productos gestionados) | Por investigar |
| S6 | Conectar Matrixify de Stetson a Claude, como ya está el de WB | Opcional; acelera cruce y validación |

### 13.2 Pendientes técnicos

- Export completo de la tienda (admin, no solo lo publicado) para medir: productos totales, variantes sin código de barras, códigos de barras repetidos.
- Crear los 8 metacampos y la exportación guardada `CruceStetson`.
- Tabla Categoría del estándar → Categoría Shopify.
- Resolver Skyline 6X y los 4 handles `-copy/-copia`.
- Confirmar con el proveedor la estructura del código Stetson (modelo, perfil, color, talla).

### 13.3 Registro de lotes

| Fecha | Origen (lote Odoo / TO) | Job Matrixify | Productos nuevos | Variantes nuevas | Actualizados | Rechazadas | En Draft | Notas |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

---

## Anexo A — Referencias verificadas en la tienda

Datos tomados de `stetsonmexico` y de `stetson.mx` el 22 de septiembre de 2026.

- Apps instaladas relevantes: Matrixify (en el menú del admin), Stockyphi (metacampos `Stockyphi Meta` y `Stockyphi Managed`, 440 productos), Smart Products Filter (índice como colección).
- Definiciones de metacampo de producto: `Disclosures`, `Tipo de producto` (159 productos), `Calificación del producto`, `Número de calificaciones`, `Stockyphi Meta`, `Stockyphi Managed`, `Google: Custom Product`, y metacampos de productos relacionados. **Ninguna** `custom.*` del estándar.
- Sucursales en la ficha de variante: Eventos, Stetson Americas, Stetson México.
- Canales: Point of Sale, Shop y otros dos; Tienda online.
- Ficha revisada: Texana Stetson Palacio II 6X Negro. Opción `Talla MX` con 6 3/4, 6 7/8, 7 1/4, 7 1/2. SKU `SFPALC-48400766`… sin código de barras. Precio 7,800.00. Categoría Shopify `Sombreros de vaquero`, con metacampos de categoría Color, Tejido, Grupo de edad, Sexo objetivo.
- Catálogo publicado: 153 productos, 884 variantes. Vendor `Stetson México` 151 y `Generico` 2. Precios de 150 a 123,000, todos múltiplos de 50. Ningún `Compare at price`.
- Comportamiento de Matrixify (documentación oficial): identifica productos por `ID`, luego `Handle`, luego `Title`; las variantes por `Variant ID`, SKU, código de barras o valores de opción. `NEW` falla si el producto existe; `MERGE` actualiza o crea; `UPDATE` falla si no existe; `REPLACE` borra y recrea. El *Dry Run* simula sin escribir, pero no atrapa los errores de validación que devuelve Shopify.

---

## Anexo B — Validación por script

La misma lógica del paso 1, en Python. Lee el archivo de carga y el export de la tienda, y escribe el archivo con `MOTIVO` y `RESULTADO`. Sirve igual para WB cambiando el bloque `CONFIG`.

```python
import sys, re
import pandas as pd

# ---- CONFIG (Stetson) ----
REGLA_PRECIO = lambda p: p > 0 and p % 50 == 0          # S4, por confirmar
OPCION_TALLA = {'Talla', 'Title'}
SUFIJOS_MALOS = r'-(copy|copia|\d+)$'
CATEGORIAS = set(pd.read_excel('Criterios.xlsx', sheet_name='Criterios', dtype=str).iloc[:, 2].dropna())
# --------------------------

carga  = pd.read_excel(sys.argv[1], dtype=str)   # archivo del lote (plantilla Matrixify)
tienda = pd.read_csv(sys.argv[2], dtype=str)     # export CruceStetson

bc, sku, h = 'Variant Barcode', 'Variant SKU', 'Handle'
est = 'Metafield: custom.no_estilo [single_line_text_field]'
cat = 'Metafield: custom.categoria [single_line_text_field]'

dup_bc  = carga[bc].duplicated(keep=False)
dup_sku = carga[sku].duplicated(keep=False)
bc_tienda  = tienda.dropna(subset=[bc]).groupby(bc)[h].apply(set).to_dict()
sku_tienda = tienda.dropna(subset=[sku]).groupby(sku)[h].apply(set).to_dict()
handles_tienda = set(tienda[h].dropna())
estilos_por_handle = carga.groupby(h)[est].nunique()

def motivos(i, r):
    m = []
    v = str(r[bc]) if pd.notna(r[bc]) else ''
    if not re.fullmatch(r'\d{12,14}', v):             m.append('V1 código de barras faltante o mal formado')
    if dup_bc.iloc[i]:                                m.append('V2 código de barras DUPLICADO en el archivo')
    otros = bc_tienda.get(v, set()) - {r[h]}
    if otros:                                         m.append(f'V3 código de barras ya existe en {sorted(otros)}')
    if pd.isna(r[sku]) or dup_sku.iloc[i]:            m.append('V4 SKU faltante o duplicado en el archivo')
    otros = sku_tienda.get(r[sku], set()) - {r[h]}
    if otros:                                         m.append(f'V5 SKU ya existe en {sorted(otros)}')
    if pd.isna(r[est]):                               m.append('V6 falta No. de Estilo')
    if estilos_por_handle.get(r[h], 0) > 1:           m.append('V7 el Handle mezcla varios No. de Estilo')
    if r[cat] not in CATEGORIAS:                      m.append('V8 Categoría fuera de la lista (revisar acentos)')
    if r.get('Option1 Name') not in OPCION_TALLA:     m.append('V11 nombre de opción distinto de Talla')
    try:
        if not REGLA_PRECIO(float(r['Variant Price'])): raise ValueError
    except (TypeError, ValueError):                   m.append('V13 precio en cero o fuera de la regla')
    if re.search(SUFIJOS_MALOS, str(r[h])):           m.append('V14 Handle con sufijo de duplicado')
    if r.get('Command') == 'NEW' and r[h] in handles_tienda:
                                                      m.append('V15 Handle ya existe: NEW fallaría')
    if pd.isna(r.get('Image Src')) and r.get('Status') != 'Draft':
                                                      m.append('V16 sin imagen: debe ir en Draft')
    return ' · '.join(m)

carga['MOTIVO'] = [motivos(i, r) for i, (_, r) in enumerate(carga.iterrows())]
carga['RESULTADO'] = carga['MOTIVO'].apply(lambda s: 'PASA' if s == '' else 'REVISAR')
print(carga['RESULTADO'].value_counts().to_string())
carga.to_excel('validado.xlsx', index=False)
```

Notas de uso:

- `dtype=str` es obligatorio en los dos archivos, por la misma razón que en Odoo: sin eso se pierden los ceros del código de barras.
- V9, V10 y V12 se agregan con la misma forma (listas y mapa de la hoja Criterios; combinación `Handle + Option1 Value` duplicada).
- El export de la tienda debe ser del mismo día. Un export viejo no ve lo que se cargó ayer.
