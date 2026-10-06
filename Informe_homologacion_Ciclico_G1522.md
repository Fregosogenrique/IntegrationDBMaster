# Informe de homologación del Cíclico G1522 por marca

*Revisión de `Ciclico_1522_investigado.xlsx`, un Cíclico por marca con la estructura de `Ciclico_1522_Stetson.xlsx` e investigación en línea de los datos faltantes*

Resultado: un archivo `Ciclico_1522_<Marca>.xlsx` por marca en la raíz del repositorio, con el inventario actual de cada artículo. Se genera con `python3 homologar_ciclico_g1522.py` (≈8 minutos). La investigación se actualiza con `python3 investigar_web_g1522.py`.

## 1. Inventario actual por marca

Cada Cíclico por marca reúne el inventario de todas las fuentes del repositorio, homologado al mismo artículo:

| Fuente | Corte | Uso |
|----|----|----|
| `Catalogo_Estandar_Inventario_NetSuite_2026-10-06.xlsx` | 06/10/2026 14:25 | Inventario del sistema por ubicación: en mano, disponible, comprometido, en pedido, en tránsito y pendiente por surtir. Es el inventario oficial |
| `Ciclico_1522_investigado.xlsx`, hoja Stock por Ubicación | NetSuite 28/09/2026 | Corte anterior para medir el movimiento neto |
| `Products.csv` (Shopify Ariat) | 05/10/2026 | Existencia por tienda Ariat: en mano, disponible, comprometido y por llegar |
| `Ciclico_1522_investigado.xlsx`, hoja Stock por Ubicación | 01/10/2026 | Shopify Stetson México, Shopify Western Brothers y Odoo Universal Unique Brands |
| Hoja Escaneos del Cíclico | 09/09/2026 | Piezas contadas en rack |

**Cómo se integra en la estructura del Cíclico.**

- **Productos:** las columnas de existencia (Stock Sistema NetSuite, Disponible, ubicaciones con stock, ubicaciones en negativo, precios vigentes) quedan al corte del 06/10.
  - Se agregaron a su marca los 100 artículos nuevos de NetSuite que no estaban en el Cíclico.
  - Un campo vacío del Cíclico se completa con lo capturado en NetSuite; nunca se sobrescribe un valor.
  - La tienda Shopify Ariat se agregó a «📍 Ubicación en plataformas» y a «Ubicaciones con stock (plataformas)».
- **Stock por Ubicación:** se rehízo con el inventario actual, que alimenta solo a Bodega 25, Bodega 43 y Criterios:
  - NetSuite 06/10, todos los renglones con existencia distinta de 0.
  - Shopify Ariat por tienda.
  - Las plataformas del 01/10.
- **Hoja nueva «Inventario»:** lista para usarse en Sheets, con un renglón por artículo de la marca que tiene existencia, comprometido, tránsito, existencia en plataformas, conteo o que tenía existencia al 28/09. Trae:
  - Identificación del artículo y precios.
  - Totales NetSuite y en mano en ubicaciones inactivas.
  - Ubicaciones en negativo.
  - En mano al 28/09 y variación neta (fórmula).
  - Plataformas y conteo cíclico.
  - Valor a costo y a precio de venta (fórmula).
  - Estado del inventario.
  - Una columna por ubicación de NetSuite y por tienda Shopify Ariat.
  - Los artículos cuya única señal es una orden de compra abierta no entran; sus unidades se reportan en los KPIs.
- **Hoja nueva «KPIs Inventario»:** fórmulas sobre la hoja Inventario, que se recalculan al editarla en Sheets:
  - Existencia, disponible, comprometido, tránsito, en pedido, negativos y valor.
  - Movimiento neto 28/09 → 06/10: entradas, salidas, artículos que bajaron, subieron o se agotaron.
  - Existencia en plataformas y conteo cíclico.
  - Tabla por ubicación con bodega, entradas y salidas netas.
  - Tiendas Ariat: NetSuite contra Shopify.
  - Tablas por división y por categoría.
  - Los 15 artículos con más existencia y los 15 con más salida.

| Archivo | Artículos en Inventario | Con existencia | En mano 06/10 | Disponible | Comprometido | En negativo | En mano 28/09 | Entradas netas | Salidas netas | En plataformas | Valor a costo |
|----|----|----|----|----|----|----|----|----|----|----|----|
| Ariat | 9,557 | 8,544 | 47,524 | 46,594 | 778 | 168 | 41,794 | 6,848 | −1,118 | 21,020 | $15,403,622 |
| Happy Socks | 210 | 210 | 15,152 | 15,026 | 0 | 0 | 15,152 | 0 | 0 | 0 | $1,088,573 |
| CAPSLAB | 292 | 292 | 10,381 | 10,385 | 0 | 0 | 10,381 | 0 | 0 | 0 | $21,662 |
| REFLO | 275 | 275 | 3,886 | 3,885 | 0 | 0 | 3,886 | 0 | 0 | 0 | $72,261 |
| Stetson | 1,695 | 573 | 1,324 | 2,629 | 471 | 653 | 687 | 868 | −231 | 5,014 | $647,619 |
| Ranch & Corral | 19 | 19 | 946 | 251 | 695 | 0 | 4 | 942 | 0 | 4 | $260,415 |
| Denver | 124 | 115 | 291 | 296 | 0 | 5 | 299 | 3 | −11 | 300 | $128,538 |
| Generico | 10 | 9 | 254 | 258 | 0 | 0 | 259 | 0 | −5 | 63 | $35,390 |
| Montana West + Wrangler | 759 | 109 | 249 | 307 | 0 | 30 | 252 | 15 | −18 | 24,125 | $109,607 |
| Yellowstone | 11 | 7 | 182 | 42 | 140 | 0 | 0 | 182 | 0 | 10 | $55,930 |
| Willow Lane | 39 | 38 | 100 | 100 | 0 | 0 | 103 | 0 | −3 | 103 | $30,380 |
| Tru Western | 47 | 12 | 59 | 59 | 0 | 0 | 59 | 0 | 0 | 632 | $17,563 |
| Roper | 262 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2,596 | $0 |
| Sin marca | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 109 | $0 |
| **Total** | **13,306** | **10,203** | **80,348** | **79,832** | **2,084** | **856** | **72,876** | **8,858** | **−1,386** | **53,976** | **$17,871,560** |

**Controles que cuadran.**

| Comparación | Unidades | Fuente |
|----|----|----|
| En mano 06/10 de los 14 archivos (Inventario y Productos) | 80,348 | Mismo total que el Resumen de NetSuite |
| Corte 28/09 | 72,876 | Mismo total que el Stock por Ubicación NetSuite del Cíclico |
| Shopify Ariat | 19,023 | Mismo total que `Products.csv` |
| Plataformas del 01/10 | 34,953 | Mismo total que el Cíclico |

Los renglones de NetSuite y de Shopify Ariat quedaron ligados al 100 % a un artículo.

**Al leer las cifras.**

- **Entradas y salidas** son netas por artículo y ubicación entre los dos cortes de NetSuite. No son el detalle de transacciones, que no viene en los archivos.
- **Valor a costo:** usa el precio de compra de NetSuite. En Ariat hay costos que parecen estar en dólares (aviso en Notas), así que ese valor está subestimado.
- **Roper y Sin marca** no tienen existencia en NetSuite; su inventario está en Odoo y Shopify.
- **NetSuite contra Shopify Ariat:** la comparación por tienda empareja ubicaciones por nombre (p. ej. «Nogales Store» con «Ariat Ecuestre Nogales»). Hay que confirmar que correspondan.

**Hallazgos del Cíclico al integrar el inventario.**

- **Columna de existencia inflada:** en Happy Socks, CAPSLAB y REFLO, «Stock Sistema NetSuite» de Productos no cuadraba con su propio desglose por ubicación. Sumaba 58,978, 15,380 y 8,872 contra 15,152, 10,381 y 3,886. El corte anterior se tomó del desglose.
- **IDs en «0»:** 236 renglones de stock del 28/09 tenían código e ID en «0»; el ID real se recuperó del texto de origen.
- **Duplicados del ERP:** dos sombreros Stetson tienen el mismo código de barras con dos IDs en NetSuite. Su existencia se suma al mismo registro, como indica la hoja Duplicados de NetSuite.
- **Prioridad al integrar:** al fundir duplicados manda el artículo que existe en NetSuite, para que el código y la existencia del ERP queden en el registro principal.

## 2. Archivos por marca

Cada archivo repite la estructura de `Ciclico_1522_Stetson.xlsx`:

- **Hojas:** las mismas 12, más «Inventario» y «KPIs Inventario» al final: Escaneo Diario, Historial de Escaneos, Escaneos, Configuración, Productos, Productos_Resumen, Criterios, Revisión Duplicados, Stock por Ubicación, Bodega 25, Bodega 43 y Resumen Integración.
- **Productos:** las mismas 44 columnas, con una fila por variante, igual que la plantilla. Los padres o agrupadores no van en Productos.
- **Funcionamiento:** las mismas fórmulas, listas desplegables, formatos condicionales y tablas. Los rangos fijos de la plantilla (`$2502`, `$24792`, `65990`) se ajustan al tamaño de cada marca.

| Archivo | Variantes | Válido | Con avisos | Con incidencias | Integrados | Stock por ubicación |
|----|----|----|----|----|----|----|
| `Ciclico_1522_Ariat.xlsx` | 49,058 | 32,782 | 15,669 | 607 | 112 | 17,582 |
| `Ciclico_1522_Stetson.xlsx` | 2,508 | 1,451 | 233 | 824 | 0 | 3,970 |
| `Ciclico_1522_Montana_West_Wrangler.xlsx` | 1,062 | 186 | 611 | 265 | 76 | 1,012 |
| `Ciclico_1522_REFLO.xlsx` | 652 | 0 | 285 | 367 | 0 | 490 |
| `Ciclico_1522_Happy_Socks.xlsx` | 570 | 0 | 211 | 359 | 0 | 252 |
| `Ciclico_1522_CAPSLAB.xlsx` | 369 | 0 | 368 | 1 | 0 | 769 |
| `Ciclico_1522_Roper.xlsx` | 284 | 0 | 283 | 1 | 0 | 262 |
| `Ciclico_1522_Denver.xlsx` | 202 | 121 | 1 | 80 | 0 | 240 |
| `Ciclico_1522_Sin_Marca.xlsx` | 113 | 0 | 0 | 113 | 0 | 6 |
| `Ciclico_1522_Tru_Western.xlsx` | 51 | 3 | 24 | 24 | 25 | 96 |
| `Ciclico_1522_Willow_Lane.xlsx` | 40 | 40 | 0 | 0 | 0 | 78 |
| `Ciclico_1522_Ranch_Corral.xlsx` | 22 | 0 | 22 | 0 | 0 | 6 |
| `Ciclico_1522_Generico.xlsx` | 11 | 0 | 1 | 10 | 0 | 21 |
| `Ciclico_1522_Yellowstone.xlsx` | 4 | 0 | 0 | 4 | 0 | 7 |
| **Total** | **54,946** | | | | **213** | **24,791** |

Válido, con avisos y con incidencias corresponden a la validación G1522 completa. Su detalle está en «Notas de enriquecimiento / revisión».

**Marca de cada archivo.** Se usa la Marca principal. Si es Multimarca o está vacía, manda WB Licencia; si la licencia no es una marca, WB Marca. Las filas sin marca la toman del mismo estilo, del nombre en la descripción o del prefijo del código del proveedor. Montana West y Wrangler comparten archivo. Las 113 filas sin evidencia de marca están en `Sin_Marca`.

**Hojas derivadas por marca.**
- **Stock por Ubicación:** solo trae los renglones de la marca, ligados por código, ID o SKU (los 24,791 quedan repartidos).
- **Escaneos e Historial:** solo los folios con piezas de la marca (hoy solo Stetson).
- **Revisión Duplicados:** los grupos del Cíclico de la marca y los registros que se integraron en uno.
- **Productos_Resumen y Bodegas:** se calculan solas en Google Sheets.

**Ariat y la memoria del navegador.** En la plantilla, Detalle de Discrepancias compara cada fila contra toda la columna (`COUNTIF`, `XMATCH`). La fila de Stock por Ubicación también se busca en todo Productos. Con las 49 mil variantes de Ariat son miles de millones de comparaciones: eso era lo que agotaba la memoria. En Ariat esas dos columnas se escriben ya calculadas, con la misma lógica de la fórmula; el resto de las fórmulas sigue vivo. En las demás marcas todo queda en fórmulas. Con Ariat no conviene reordenar Productos, porque Stock por Ubicación apunta al número de fila: es mejor usar filtros.

**Los archivos son la versión de trabajo.** Lo que se corrija a mano en los 26 atributos de cualquier `Ciclico_1522_<Marca>.xlsx` se conserva al regenerar. Por ejemplo, se conservaron los SKU `2XL` → `XXL` y las licencias capturadas en Stetson. Existencias, ubicaciones y escaneos siempre se toman del Cíclico integrado.

## 3. Cómo se trató cada campo

Se respetan Criterios (hoja Criterios del Cíclico) y `Anatomia_productos_atributos_G1522.md`. El campo vacío queda realmente vacío, sin «No Aplica». Lo que no tiene evidencia no se inventa.

| Regla | Aplicación |
|----|----|
| Paso 1 Categoría y División | Palabra clave del nombre; División por la tabla de categorías |
| Paso 2 Género | Dama → Mujer, Caballero → Hombre; accesorio sin género → Unisex |
| Pasos 4 y 5 Tallas | CH/MED/GDE → S/M/L, 2XL → XXL; talla de EE. UU. de la misma fila del catálogo (Criterios 8), según la familia de la categoría (Criterios 3) |
| Paso 6 Color | Color base por la tabla de sinónimos |
| Paso 7 Unidad y listas | PRS en calzado, PZS lo demás; `CORE` → Core, `Pieza` → PZS |
| Pasos 8 y 9 Fit y Silueta | Fit solo en Ropa y Denim. Silueta solo en Sombreros, Calzado y Jeans, y solo de la lista de su categoría. Fuera de eso, vacío (p. ej. «Correa de 38 mm», «Bifold») |
| Otros | Ceros iniciales del UPC, clave SAT de 8 dígitos, coma decimal en costos, país escrito en español, licencia con una sola escritura, acentos en materiales, `(blank)` → vacío |
| Estilo desde el SKU | SKU con formato Karman (`01-001-0016-1076 BL-2XL`): el estilo es el prefijo de 4 bloques, convención que cumplen 564 de 601 filas. Completa los estilos de Roper |

Cada cambio queda en «Notas de enriquecimiento / revisión» de su fila con este formato: `Homologación G1522 06/10/2026: campo «antes» → «después» (tipo)`. La misma nota trae la validación G1522, por ejemplo dígito de control inválido o costo posiblemente en dólares, y el resultado de los validadores NetSuite/Odoo y Shopify cuando fallan.

## 4. Productos iguales integrados en uno

Se funden en un registro (213 integraciones):

1. El mismo código de barras, aunque uno haya perdido el cero inicial.
2. El mismo SKU con estilo, talla y color compatibles.
3. Una variante sin código igual en estilo, talla y color a una con código.

Si el SKU o el código coinciden pero el estilo, la talla o el color son distintos, no se funden: es una colisión de captura y queda anotada.

Se conserva el registro con código válido y mejor origen. Sus campos vacíos se completan con los otros, las existencias se suman y las ubicaciones se unen. En «🔍 Panel de Duplicados» del registro conservado se indica cuántos integró y los códigos alternos. Los registros originales quedan completos en la hoja Revisión Duplicados, con la fuente «registro conservado» o «registro integrado».

## 5. Investigación en línea

`investigar_web_g1522.py` descargó los catálogos públicos de las marcas y sus distribuidores y consultó ariat.com por número de estilo. Resultado: `Investigacion_web_G1522.csv`, con 33,562 datos de productos del catálogo; cada uno trae llave, campo, valor, URL y evidencia.

| Fuente | Cómo empata | Datos |
|----|----|----|
| ariat.com.mx | Código de barras (SKU de la tienda) | 18,201 |
| ariat.com | Número de estilo (1,733 de 4,987 estilos siguen publicados) | 6,121 |
| stetson.mx | WB SKU | 3,395 |
| westernbrothers.mx | Código de barras | 3,172 |
| stetson.com | WB SKU | 1,498 |
| montanawestworld.com | WB SKU | 519 |
| reflo.com | Código de barras de cada variante | 338 |
| willowlanehats.com | WB SKU | 318 |

Solo se escribe un dato si cumple todas estas condiciones:

- El campo está vacío.
- El valor existe en las listas de Criterios (color base por sinónimos, categoría por palabra clave, género de la lista básica).
- La fuente da un solo valor. Si dos fuentes dan valores distintos, se descarta (1,134 casos).

Además:

- **País:** solo cuando la ficha lo declara («Made in USA», «Hecho en México»), nunca a partir de «Imported».
- **Fit:** solo cuando la ficha nombra el corte («Relaxed Fit», «Corte Recto»).
- **Lo que nunca se toma de internet:** SKU, código de barras, temporada, ciclo de vida y precios.

La URL queda en «Fuentes de consulta» de la fila: `Investigación en línea 06/10/2026: <url>`.

| Campo completado en línea | Filas |
|----|----|
| Enlace de imagen | 4,657 |
| WB Silueta | 1,883 |
| WB Fit | 420 |
| WB Género | 267 |
| WB Color | 133 |
| WB País de origen | 59 |
| WB Descripcion | 45 |
| WB Categoría | 41 |
| WB Talla y Talla de EE. UU. | 35 |

**Sin fuente en línea disponible:**

| Marca | Motivo |
|----|----|
| Happy Socks | El sitio está en mantenimiento y la búsqueda por código de barras no identifica los productos. Sus 359 filas sin estilo, SKU ni descripción siguen pendientes |
| Wrangler (botas WACA, cinturones C4…) | wrangler.com bloquea las consultas |
| CAPSLAB, Roper, Denver, Tru Western, Ranch & Corral, Yellowstone | No publican un catálogo consultable |
| Ariat descontinuado | 3,254 estilos ya no están publicados en ariat.com |

## 6. Revisión del archivo Cíclico

| Hallazgo | Detalle |
|----|----|
| Rango declarado mayor que los datos | Productos declara 166,905 filas y tiene 65,790 |
| Fórmulas cuadráticas | Estatus y Detalle comparan cada fila contra toda la columna |
| Columnas de texto pesadas | Notas (13.8 MB de texto) y Fuentes de consulta (11.6 MB) |
| Mismo producto en varias filas | 403 grupos: SKU repetido entre Hoja2/Hoja3 y Catálogo existente, UPC sin cero inicial, padres repetidos |
| Filas sin WB Marca | 1,034; marca deducida en 723 |
| Códigos Stetson de 17 dígitos | 752 son clave interna, no UPC |
| Costos que parecen estar en dólares | 7,053 (11 a 20 contra venta de ~1,449) |
| Valores fuera de Criterios | `CORE`, `Pieza`, `MX`, `USA`, `(blank)`, `STETSON`, licencias con dos escrituras, coma decimal |

## 7. Diferencias entre documentos

Se siguieron Criterios y Anatomía, que son la autoridad de captura:

| Tema | Criterios / Anatomía | Flujo NetSuite |
|----|----|----|
| Talla de calzado | US = MX − 18 (hombre) o − 17 (mujer) | MX = US + 20 |
| Ropa | XXL, XXXL | 2XL, 3XL |
| Ciclo de vida | Core | CORE |
| Campo que no aplica | Vacío | — |

Las listas desplegables de la plantilla (Criterios 12) incluyen «No Aplica». Se dejaron como están para no cambiar la estructura, pero los datos usan vacío, como pide la Anatomía.

## 8. Pendientes

1. Happy Socks: estilo, SKU, descripción y clasificación de 359 variantes, que en NetSuite solo tienen código de barras.
2. REFLO: 367 variantes en la misma situación. La tienda solo cubrió las que siguen a la venta.
3. Confirmar la moneda de los costos con aviso de dólares.
4. Asignar marca a las 113 variantes de `Sin_Marca`.
5. Revisar en cada archivo las notas «Completado por regla» y «Completado por investigación en línea»: son propuestas con evidencia y requieren confirmación.
6. Decidir si los códigos Stetson de 17 dígitos se reemplazan por UPC del proveedor.
7. Confirmar las existencias negativas, sobre todo STETSON AMERICAS (−803 unidades de Stetson).
8. Confirmar la pareja de tiendas NetSuite–Shopify Ariat antes de usar la comparación por tienda.
