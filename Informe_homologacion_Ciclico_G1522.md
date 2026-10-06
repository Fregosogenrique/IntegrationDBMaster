# Informe de revisión y homologación del Cíclico G1522

*Revisión de `Ciclico_1522_investigado.xlsx` y separación en bases por marca para Google Sheets*

Resultado: carpeta `Bases_Sheets_G1522/`, generada con `python3 homologar_ciclico_g1522.py` (≈2 minutos).

## 1. Revisión del archivo Cíclico

### Por qué el archivo satura el navegador

| Hallazgo | Detalle |
|----|----|
| Rango declarado mucho mayor que los datos | La hoja Productos declara `A1:AR166905`, pero solo 65,790 filas tienen datos. Hay unas 101 mil filas vacías con formato que Sheets carga igual |
| Fórmulas en cada fila | Estatus de Validación, Detalle de Discrepancias y Panel de Duplicados se calculan por fórmula. La cadena de cálculo ocupa 7.3 MB. Algunas apuntan a libros externos (`[2]Criterios`, `[2]Productos_Resumen`) |
| Texto de trazabilidad pesado | Notas de enriquecimiento (13.8 MB de texto) y Fuentes de consulta (11.6 MB) pesan más que los 26 atributos juntos |
| Columnas duplicadas | Precio compra vigente y Precio venta vigente repiten Precio de compra y de venta (solo 46 filas difieren de cada una) |
| Todo en un libro | 12 hojas en un solo archivo: 396 MB sin comprimir |

La base Ariat anterior tenía el mismo problema: 59,346 filas × 60 columnas (3.5 millones de celdas) en una hoja, más la hoja Revisión.

### Calidad de los datos

| Hallazgo | Volumen | Tratamiento |
|----|----|----|
| Filas sin WB Marca | 1,034 | Marca deducida en 723 filas; 265 sin evidencia quedan en `Sin_Marca` |
| Mismo producto en dos o más filas | 403 grupos (799 filas) | Integrados en un registro (sección 3) |
| Padres repetidos del mismo estilo | 190 grupos | Integrados |
| Código de barras sin cero inicial (`87327002917`) | 25 pares Tru Western (Carga Hoja2 contra NetSuite) | Se restituye el cero y se integran |
| Mismo SKU con otro código de barras | 75 grupos Wrangler y Montana West (Carga Hoja2/Hoja3 contra Catálogo existente) | Integrados; el segundo código queda como alterno |
| Códigos Stetson de 17 dígitos (`12020000101017025`) | 752 | Son la clave interna Stetson (SKU sin guiones), no un UPC. Quedan con incidencia |
| Costo con coma decimal (`344,48`) | 140 | Corregido a punto |
| Costo que parece estar en dólares (11 a 20 contra venta de ~1,449) | 7,053 (6,558 de Ariat) | Aviso en cada fila: confirmar moneda (decisión N5 del flujo NetSuite) |
| Valores fuera de Criterios: `CORE`, `Pieza`, `Mexico`/`MX`/`MEX`, `USA`/`US`, `(blank)`, `STETSON`, `Tom And Jerry`, `Rick and Morty`, composición sin acentos | 1,439 | Homologados |
| Silueta fuera de su categoría (`Correa de 38 mm`, `Manga larga; frente con broches`, `Bifold`) | 45 | Campo vacío, como pide Criterios |
| Códigos de Shopify Stetson repetidos en artículos distintos (hoja Revisión Duplicados) | 11 | Pasan a Revisión de Stetson como «Conflicto plataforma»: se corrigen en la tienda |
| Artículos «Hoja a Revisar — inactivo» de la base Ariat anterior | 605 | Ya no están en el Cíclico y no se incluyen. Siguen en `Base_Unificada_Ariat_G1522.xlsx` |

## 2. Bases por marca

Regla de marca: **Marca principal**; si es Multimarca o está vacía, **WB Licencia**; si la licencia no es una marca, **WB Marca**; si no hay marca, el nombre de la marca en la descripción o el prefijo del código del proveedor (`CL/` CAPSLAB, `AR` Ariat, `WLHB` Willow Lane, etc.). En el Cíclico, Licencia y WB Marca coinciden en todas las filas Multimarca.

Montana West y Wrangler van en una sola base. Ariat pasa de 20,000 filas y se divide por División.

Cada archivo tiene **una sola hoja**. Por marca hay un archivo de Productos, uno de Revisión y uno de Stock por ubicación (Stetson también tiene uno de Escaneos):

| Carpeta | Productos | Válido | Con avisos | Con incidencias | Integrados |
|----|----|----|----|----|----|
| `Ariat/` Ropa | 31,959 | 25,540 | 6,268 | 151 | 51 |
| `Ariat/` Calzado | 10,545 | 6,220 | 4,288 | 37 | 11 |
| `Ariat/` Denim | 8,359 | 7,093 | 1,063 | 203 | 32 |
| `Ariat/` Accesorios | 5,726 | 1,675 | 4,013 | 38 | 208 |
| `Ariat/` Sin división | 1,841 | 0 | 1,319 | 522 | 0 |
| `Stetson/` | 2,966 | 1,485 | 241 | 1,240 | 0 |
| `Montana_West_Wrangler/` | 1,150 | 193 | 612 | 345 | 76 |
| `CAPSLAB/` | 703 | 0 | 368 | 335 | 0 |
| `REFLO/` | 652 | 0 | 285 | 367 | 0 |
| `Happy_Socks/` | 570 | 0 | 211 | 359 | 0 |
| `Roper/` | 288 | 0 | 4 | 284 | 0 |
| `Sin_Marca/` | 265 | 0 | 0 | 265 | 0 |
| `Denver/` | 264 | 135 | 3 | 126 | 0 |
| `Willow_Lane/` | 80 | 80 | 0 | 0 | 0 |
| `Tru_Western/` | 78 | 3 | 24 | 51 | 25 |
| `Ranch_Corral/` | 44 | 0 | 22 | 22 | 0 |
| `Generico/` | 22 | 0 | 1 | 21 | 0 |
| `Yellowstone/` | 4 | 0 | 0 | 4 | 0 |
| **Total** | **65,516** | **42,424** | **18,722** | **4,370** | **403** |

`Indice_bases_G1522.xlsx` lista los 44 archivos con filas, celdas, tamaño y conteos. `Listas_Criterios_G1522.xlsx` reúne las listas de Criterios (secciones 3, 8, 9 y 12).

### Optimización para Google Sheets

| Medida | Efecto |
|----|----|
| Un archivo por marca y por contenido, una hoja por archivo | Sheets abre solo lo que se va a trabajar |
| Solo las celdas con datos, sin filas vacías con formato | El rango declarado es el real |
| Sin fórmulas: estatus y validadores ya calculados | Nada se recalcula al abrir, filtrar u ordenar |
| Fuera las columnas de texto de trazabilidad (Notas, Fuentes de consulta, Panel de Duplicados) y los precios vigentes duplicados | El texto se consulta en el Cíclico por Identificador interno |
| Identificadores guardados como texto | Se conservan los ceros iniciales (133 códigos) |
| Desplegables de Criterios › 12 como una regla por columna | Marca principal, WB Marca, División, Género, Temporada, Ciclo de vida, Unidad, Color y Fit. Avisan, no bloquean |

El archivo más grande, `Productos_Ariat_Ropa.xlsx`, tiene 1.47 millones de celdas y pesa 4.3 MB. La base Ariat anterior tenía 3.5 millones de celdas en una hoja y pesaba 11 MB. Si aún resulta pesado, la regla `MAX_FILAS_LIBRO` del script permite partirlo más.

## 3. Productos iguales integrados en uno

Se funden en un registro los que son el mismo producto:

1. El mismo código de barras, aunque uno haya perdido el cero inicial.
2. El mismo WB SKU con marca, estilo, talla y color compatibles (iguales o uno vacío).
3. Una variante sin código igual en marca, estilo, talla y color a una sola variante con código.
4. Padres repetidos del mismo estilo y marca.

Si el SKU o el código coinciden pero el estilo, la talla o el color son distintos, no se funden: es una colisión de captura y va a Revisión (árbol de decisión de `Propuesta_Limpieza_Catalogo_Shopify_G1522.md`, §7).

Se conserva el registro con código válido y mejor origen: Catálogo existente, después NetSuite con existencia, NetSuite sin existencia, Hoja a Revisar, plataformas y al final las cargas Hoja2/Hoja3. Los campos vacíos se completan con los otros registros. Si los valores difieren, se conserva el principal y la diferencia queda en Revisión como «Conflicto entre duplicados». Las existencias se suman y las ubicaciones se unen.

Cada registro integrado lo indica en dos columnas:

- **Registros integrados:** motivo e IDs de las filas absorbidas.
- **Códigos de barras alternos:** el otro código, cuando el mismo producto traía dos (69 casos). Revisión pide confirmar cuál trae la etiqueta física.

Stock por ubicación y Escaneos se ligan al registro integrado por cualquiera de sus códigos.

## 4. Criterios aplicados

Además de las reglas de `homologar_ariat_g1522.py`, que se reutilizan tal cual, se aplicaron:

| Sección de Criterios | Aplicación | Registros |
|----|----|----|
| 1 · Paso 1 | Categoría por palabra clave y División por categoría | 415 y 37 completadas |
| 1 · Paso 2 | Género por descripción; accesorio sin género → Unisex | 704 |
| 1 · Paso 5 y 8 | Talla de EE. UU. de la misma fila del catálogo, filtrada por la familia de la categoría (sección 3) y el género | 134 |
| 1 · Paso 8 / 7 | Fit en Ropa y Denim cuando la descripción nombra un solo fit (Slim, Relajado, Recto, Clásico, Moderno, Bootcut) | 640 |
| 1 · Paso 9 / 7 | Silueta en Sombreros, Botas, Zapatos y Jeans cuando la descripción nombra una sola (Copa Cattleman, Punta Cuadrada, Trouser, Recto…) | 597 |
| 4 · Listas básicas | `CORE` → Core, `Pieza` → PZS | 56 |
| 8 · Catálogo de tallas | Aviso si la pareja WB Talla / Talla de EE. UU. no está en el catálogo | 559 |
| 9 · Ubicaciones | Columna Bodega (25 / 43) en Stock por ubicación y Escaneos | — |
| 12 · Listas automáticas | Desplegables en Productos | 9 columnas |
| Padre | El padre toma de sus variantes División, Categoría, Género, Temporada y Ciclo de vida cuando todas coinciden | incluido arriba |

En Ariat, los valores que la base anterior tomó de su tienda Shopify (Fit por corte, país, composición, imagen, temporada) se completan antes que las reglas por descripción, porque son mejor evidencia. Las decisiones de esa base sobre la tienda se conservan en `Revision_Ariat.xlsx`: 785 conflictos de precio, 6 conflictos de SKU o código y 526 variantes solo en Shopify. También se conservan los IDs de Shopify (Handle, ID producto, ID variante, Estatus) para cargas con `UPDATE`.

Lo deducido por regla queda en Revisión con su evidencia para confirmarlo. No se inventan temporadas, ciclos de vida, colores ni composiciones.

## 5. Validadores aplicados

Las fórmulas de los cuatro validadores se calculan en Python y se guardan como texto, con el mismo semáforo (`✅ PASA` / `❌ motivos`), solo en variantes:

| Columna | Reglas | Pasa |
|----|----|----|
| Validador NetSuite / Odoo | V1 longitud 12–14 (y código faltante), V2 UPC repetido, V4 SKU repetido, V6 falta estilo, N2 talla cero o vacía (admite 0 en Vestidos, Faldas, Jeans, Pantalones y Shorts, como pide la documentación) | 50,544 de 54,946 |
| Validador Shopify | V1, V2, V4, V6 más la regla de precio de la tienda: Stetson, precio × 1.16 múltiplo de 50; las demás marcas (WB), entero de precio × 1.16 terminado en 9 | 9,371 de 54,946 |

El Validador Shopify falla sobre todo por precio: en 44 mil variantes el precio de venta del catálogo da un múltiplo de 100 con IVA (1,724.14 × 1.16 = 2,000), no uno terminado en 9. Es lo mismo que la base Ariat ya documentaba: la tienda redondea a 9 y el ERP no. La regla «SKU = código de barras» de Shopify WB no se evalúa contra WB SKU, porque el flujo WB arma ese SKU a partir del código al preparar el archivo Matrixify.

## 6. Diferencias entre documentos

Se siguió Criterios y `Anatomia_productos_atributos_G1522.md`, que son la autoridad de captura:

| Tema | Criterios / Anatomía | `Flujo_Alta_Productos_NetSuite_G1522.md` |
|----|----|----|
| Talla de calzado | US = MX − 18 (hombre) o − 17 (mujer) | MX = US + 20 |
| Ropa | XXL, XXXL | 2XL, 3XL |
| Ciclo de vida | Core | CORE |

Conviene alinear el flujo NetSuite antes del primer lote.

## 7. Pendientes

1. Revisar cada `Revision_<marca>.xlsx`, empezando por «Requiere revisión» y «Conflicto entre duplicados».
2. Confirmar la moneda de los 7,053 costos con aviso de USD.
3. Asignar marca a las 265 filas de `Sin_Marca`.
4. Capturar estilo y SKU faltantes en Roper, REFLO y Happy Socks: casi todas sus incidencias son por eso.
5. Decidir si los códigos Stetson de 17 dígitos se reemplazan por UPC del proveedor.
6. Confirmar los códigos alternos de los 69 productos con dos códigos.
7. Confirmar el uso de Silueta en Tenis y Pantuflas (152 avisos).
