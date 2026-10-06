# Informe de homologación del Cíclico G1522 por marca

*Revisión de `Ciclico_1522_investigado.xlsx`, un Cíclico por marca con la estructura de `Ciclico_1522_Stetson.xlsx` e investigación en línea de los datos faltantes*

Resultado: un archivo `Ciclico_1522_<Marca>.xlsx` por marca en la raíz del repositorio. Se genera con `python3 homologar_ciclico_g1522.py` (≈8 minutos). La investigación se actualiza con `python3 investigar_web_g1522.py`.

## 1. Archivos por marca

Cada archivo repite la estructura de `Ciclico_1522_Stetson.xlsx`:

- **Hojas:** las mismas 12, sin hojas nuevas: Escaneo Diario, Historial de Escaneos, Escaneos, Configuración, Productos, Productos_Resumen, Criterios, Revisión Duplicados, Stock por Ubicación, Bodega 25, Bodega 43 y Resumen Integración.
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

## 2. Cómo se trató cada campo

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

## 3. Productos iguales integrados en uno

Se funden en un registro (213 integraciones):

1. El mismo código de barras, aunque uno haya perdido el cero inicial.
2. El mismo SKU con estilo, talla y color compatibles.
3. Una variante sin código igual en estilo, talla y color a una con código.

Si el SKU o el código coinciden pero el estilo, la talla o el color son distintos, no se funden: es una colisión de captura y queda anotada.

Se conserva el registro con código válido y mejor origen. Sus campos vacíos se completan con los otros, las existencias se suman y las ubicaciones se unen. En «🔍 Panel de Duplicados» del registro conservado se indica cuántos integró y los códigos alternos. Los registros originales quedan completos en la hoja Revisión Duplicados, con la fuente «registro conservado» o «registro integrado».

## 4. Investigación en línea

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

## 5. Revisión del archivo Cíclico

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

## 6. Diferencias entre documentos

Se siguieron Criterios y Anatomía, que son la autoridad de captura:

| Tema | Criterios / Anatomía | Flujo NetSuite |
|----|----|----|
| Talla de calzado | US = MX − 18 (hombre) o − 17 (mujer) | MX = US + 20 |
| Ropa | XXL, XXXL | 2XL, 3XL |
| Ciclo de vida | Core | CORE |
| Campo que no aplica | Vacío | — |

Las listas desplegables de la plantilla (Criterios 12) incluyen «No Aplica». Se dejaron como están para no cambiar la estructura, pero los datos usan vacío, como pide la Anatomía.

## 7. Pendientes

1. Happy Socks: estilo, SKU, descripción y clasificación de 359 variantes, que en NetSuite solo tienen código de barras.
2. REFLO: 367 variantes en la misma situación. La tienda solo cubrió las que siguen a la venta.
3. Confirmar la moneda de los costos con aviso de dólares.
4. Asignar marca a las 113 variantes de `Sin_Marca`.
5. Revisar en cada archivo las notas «Completado por regla» y «Completado por investigación en línea»: son propuestas con evidencia y requieren confirmación.
6. Decidir si los códigos Stetson de 17 dígitos se reemplazan por UPC del proveedor.
