# Informe de homologación Ariat G1522

*Fusión de `Ariat.xlsx` y `Products.csv` en una base única bajo el estándar G1522*

Resultado: `Base_Unificada_Ariat_G1522.xlsx`, generado con `python3 homologar_ariat_g1522.py`.

## Fuentes

| Archivo | Contenido | Registros |
|----|----|----|
| `Ariat.xlsx` | Catálogo maestro G1522 (26 columnas A–Z y controles AA–AR) | 58,820 filas |
| `Products.csv` | Exportación de la tienda Shopify Ariat (Matrixify) | 3,983 productos, 19,350 variantes |

El maestro es la autoridad de captura. Shopify solo completa campos vacíos y sirve como cruce externo. Ningún valor del maestro se sobrescribe con datos de Shopify.

## Empate

- **Llave:** Código de barras, que identifica la variante. Cuando la variante de Shopify no trae código, se usa su SKU si coincide con un código de barras del maestro, porque en esta tienda el SKU es el código.
- **Empatadas:** 18,822 variantes.
- **Solo en Shopify:** 526 variantes (513 sin código de barras y 13 con un código que no existe en el maestro). Se agregaron a la base con `Origen de la fusión = Solo Shopify` y quedan en Revisión. Cuando hay un código parecido en el maestro, Revisión lo indica.
- **Solo en el maestro:** 39,998 filas, entre ellas los 9,636 padres o agrupadores.

## Estructura de la base unificada (hoja Productos)

| Bloque | Columnas |
|----|----|
| Nivel | `Nivel G1522`: Padre / agrupador o Variante |
| Atributos | Las 26 columnas A–Z del estándar, en el mismo orden y con los identificadores como texto (se conservan los ceros iniciales) |
| Validación | `Estatus G1522` (Válido, Válido con avisos, Con incidencias) e `Incidencias G1522` |
| Trazabilidad | `Origen de la fusión` y columnas `Shopify …` (IDs, handle, estatus, opciones, SKU, código, precios, inventario, tipo de empate) |
| Control | Columnas AA–AR originales del maestro, sin cambios y fuera del núcleo de 25 atributos |

La hoja **Revisión** registra cada cambio, conflicto o duda con: campo, valor origen, valor final, tipo, acción, evidencia y una columna vacía para el responsable de validación. La hoja **Resumen** concentra los conteos.

## Reglas aplicadas (Criterios)

| Regla | Aplicación | Registros |
|----|----|----|
| Campos vacíos | «No Aplica» en Fit y Silueta → celda vacía | 611 Fit, 1,152 Silueta |
| Fit solo en Ropa y Denim | Fit en calzado o accesorios → vacío | 2 |
| Silueta solo en Sombreros, Calzado y Jeans | Ningún caso fuera de categoría tras limpiar «No Aplica» | 0 |
| División según Categoría | División corregida con la tabla de categorías | 14 corregidas |
| Paso 1: palabra clave → Categoría | Solo con una coincidencia; los kits («Camisa y chaleco») van a Revisión | 331 asignadas, 152 a revisión |
| Paso 2: Género | Dama/Mujer, Caballero/Hombre, Niño, Niña en la descripción; accesorio sin género → Unisex | 662 |
| Paso 6: Color base | Solo si la descripción nombra un único color base o sinónimo | 50 |
| Paso 7: Unidad | PRS para Botas, Zapatos, Tenis y Pantuflas; PZS para lo demás | 331 |
| Talla única | Accesorios sin talla → Talla única / One Size | 12 |
| Clave SAT | Se restituye el cero inicial (8 dígitos) | 12 |
| Precio cero | Se trata como desconocido: vacío y a Revisión | 75 compra, 176 venta |

También se homologan CH/MED/GDE/UNI, 2XL/3XL, OS y las equivalencias entre paréntesis. En esta base no hubo casos.

## Datos completados desde Shopify

| Campo | Fuente en Shopify | Registros |
|----|----|----|
| WB País de origen | Variant Country of Origin (MX → México) | 111 |
| WB Fit | custom.corte con equivalencia directa (Bota → Bootcut, Slim, Clásico, Recto, Moderno) | 217 |
| WB Composición | custom.materiales, solo si son pares porcentaje-material que suman 100 % | 94 |
| Enlace de imagen | Imagen principal del producto | 22 |
| WB Descripción larga | Body HTML convertido a texto | 7 |
| WB Temporada | custom.season (Spring 2026 → SS26) | 3 |
| Precio de venta | Precio regular de la variante | 1 |

Los valores de Shopify sin equivalencia en Criterios no se cargan y van a Revisión: temporadas 2023–2025, cortes Retro o Acampanado y materiales sin porcentaje.

## Resultado de la validación

| Estatus | Filas |
|----|----|
| Válido | 46,390 |
| Válido con avisos | 11,675 |
| Con incidencias | 1,281 |

Incidencias bloqueantes:

| Incidencia | Filas | Origen principal |
|----|----|----|
| Código de barras faltante | 1,230 | 513 variantes solo Shopify, 604 inactivos, 89 artículos «Hoja a Revisar», 24 altas WB/Odoo |
| WB SKU faltante | 1,234 | Mismas filas, más 4 con código de barras pero sin SKU |
| Padre sin WB N.º de estilo | 22 | Padres o agrupadores |
| Falta estilo en una variante con código | 17 | — |
| Dígito de control inválido | 11 | Por ejemplo 019932027784 y 725272730712 |
| Código no numérico o de longitud inválida | 7 | C32763612, 100001, 70134059652, … |
| WB SKU duplicado | 3 | SKU 10037365 en 3 variantes archivadas de Shopify |

Avisos más frecuentes: Color no capturado (8,305), Temporada (4,113), Ciclo de vida (3,430) y Talla (2,545).

## Conflictos entre maestro y Shopify

- **Precio de venta (785 variantes):** la tienda redondea a terminación 9 (1,478 → 1,479) o tiene un precio distinto. Se conserva el maestro y la diferencia queda documentada.
- **SKU y código cruzados en Shopify (4):** por ejemplo, la variante con código 197318010637 tiene el SKU 197318010620. Hay que corregirlo en la tienda.
- **Código repetido en dos variantes de Shopify (2).**

## Pendientes

1. Revisar la hoja Revisión, filtrando primero «Requiere revisión» y «Conflicto».
2. Decidir si las 513 variantes de Shopify sin código de barras (318 activas, 183 en Draft y 12 archivadas) se capturan o se depuran.
3. Confirmar el uso de Silueta en Tenis y Pantuflas (152 filas con aviso), como pide el documento de anatomía.
4. Antes de cargar, confirmar moneda, impuestos y redondeo de precios por tienda.
