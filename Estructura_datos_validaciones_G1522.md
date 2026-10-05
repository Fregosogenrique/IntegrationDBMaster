# Documentación de la estructura de datos

*Diccionario de 25 atributos mapeo funcional y reglas de validación*

Grupo G1522 \| Versión 1.0 \| 5 de octubre de 2026

Este documento relaciona las columnas del catálogo G1522 con sus funciones en NetSuite, Odoo y Shopify, y describe las fórmulas de los validadores entregados. Criterios establece los valores de captura. Cuando un atributo no corresponda, el campo se deja en blanco. Se distinguen los controles existentes de los controles necesarios para una carga completa.

## Alcance de los 25 campos

Productos contiene 26 columnas base, A a Z. Se documentan 25 atributos de negocio excluyendo Identificador interno, columna B, que se conserva como referencia técnica adicional. Esta delimitación debe confirmarse con el dueño del catálogo si existe otra enumeración aprobada de 25 campos. No hay evidencia para declarar obligatoria la captura de todos los atributos en todas las categorías.

Los validadores contienen cinco entradas: WB N.º de estilo, WB SKU, Código de barras, Precio de venta y WB Talla. Las restantes siete columnas contienen controles o espacios reservados. No validan por sí solos el diccionario completo de 25 atributos.

## Nivel padre y variante

El modelo lógico mantiene un padre por modelo comercial y variantes por configuración vendible. SKU y código de barras se verifican en el nivel variante. El estilo agrupa modelos y no se rechaza por repetirse entre sus variantes. El Identificador interno no debe trasladarse como llave equivalente entre sistemas sin un cruce de correspondencias.

## Diccionario y reglas de captura

| **Núm y columna** | **Campo** | **Formato y regla** |
|----|----|----|
| 1 / A | Código de barras | Texto de 12 a 14 caracteres; conservar ceros iniciales. Identifica la variante comercial. Requerido para las filas a validar; comprobar dígitos y unicidad además de longitud. |
| 2 / C | Marca principal | Texto de lista. Admite Multimarca y las marcas registradas en Criterios. No confundir la agrupación principal con la marca real del producto. |
| 3 / D | WB N.º de estilo | Texto alfanumérico del modelo comercial, con guiones y formato del proveedor. Puede repetirse entre variantes del mismo modelo; no es llave única de variante. |
| 4 / E | WB SKU | Texto del código comercial de la variante; conservar espacios, guiones y ceros significativos. Único por variante. En Shopify WB el validador exige que sea igual al código de barras. |
| 5 / F | WB Talla | Texto exacto del catálogo de tallas de la familia correspondiente. Sin talla física: Talla única. No reemplazar por blanco una talla única válida. |
| 6 / G | WB Talla de EE. UU. | Texto de la misma fila de equivalencia que WB Talla, incluida la anchura del proveedor. Si la regla es Igual, copiar WB Talla. No convertir sin confirmar familia y etiqueta. |
| 7 / H | WB Marca | Texto exacto de la lista de marcas de Criterios. Representa la marca del producto. Una marca desconocida se registra para revisión. |
| 8 / I | WB Descripcion | Texto descriptivo corto del producto. La fuente aporta ejemplos, pero no establece una longitud máxima ni sintaxis obligatoria. |
| 9 / J | WB División | Lista cerrada: Accesorios, Ropa, Denim, Calzado. Debe coincidir con la división de WB Categoría. |
| 10 / K | WB Categoría | Texto exacto de la tabla de categorías; se obtiene por palabra clave o selección validada. Usar la primera palabra clave coincidente; no inventar categorías. |
| 11 / L | WB Género | Lista cerrada: Hombre, Mujer, Niño, Niña, Unisex. Dama se homologa a Mujer; Caballero a Hombre; accesorios sin género a Unisex. |
| 12 / M | WB Licencia | Texto de la licencia respaldada por el producto o proveedor. Criterios no contiene lista cerrada ni regla detallada. Cuando no corresponda, dejar el campo en blanco. |
| 13 / N | WB Temporada | Lista cerrada: SS26, FW26, SS27, FW27, SS28, FW28. No derivar la temporada de la fecha de captura; usar la información validada del producto. |
| 14 / O | WB Ciclo de vida | Lista cerrada: Seasonal, Core. Cuando no corresponda, dejar el campo en blanco. No deducir Core a partir de stock. |
| 15 / P | WB Color | Texto del color base de Criterios; normalizar nombres comerciales mediante sinónimos. Usar el dominante. Varios corresponde a multicolor sin dominante o al supuesto descrito en Criterios. |
| 16 / Q | WB Fit | Lista homologada de corte para Ropa y Denim. En calzado, sombreros y accesorios, dejar el campo en blanco. Si falta evidencia en una prenda, registrar revisión. |
| 17 / R | WB Silueta | Lista homologada según sombrero, calzado o jeans. En otras categorías, dejar el campo en blanco. La horma puede requerir nivel variante si cambia entre piezas. |
| 18 / S | WB Composición | Texto de materiales y porcentajes según etiqueta o ficha técnica. Sin lista o formato obligatorio en Criterios; no inventar materiales ni porcentajes. |
| 19 / T | WB Descripción larga | Texto detallado sustentado en la ficha del producto. Sirve como evidencia para Fit y Silueta. La fuente no establece límite de caracteres ni formato HTML. |
| 20 / U | WB País de origen | Texto del origen declarado por proveedor o etiqueta. Sin lista cerrada en Criterios. No deducir el origen de la marca. |
| 21 / V | Unidad | Lista cerrada: PRS para Botas, Zapatos, Tenis y Pantuflas; PZS para lo demás. La unidad describe cómo se controla o vende el artículo; no es una cantidad. |
| 22 / W | SAT Clave de producto | Identificador de texto de la clave asignada al producto. La fuente incluye ejemplos, pero no aporta catálogo SAT ni procedimiento fiscal de asignación. |
| 23 / X | Enlace de imagen | Texto con la dirección de la imagen asociada al producto o variante. La fuente no impone dominio ni extensión; confirmar que la imagen corresponda al producto. |
| 24 / Y | Precio de compra | Valor numérico de costo; conservar precisión de origen. La hoja no declara moneda ni política general de impuestos; confirmar antes de importar. |
| 25 / Z | Precio de venta | Valor numérico de venta; conservar precisión de origen. Los validadores Shopify aplican precio × 1.16. Confirmar la base del precio antes de usarlos. |

## Mapeo funcional entre plataformas

Los archivos no aportan exportaciones con encabezados nativos de los tres sistemas, pantallas de configuración, nombres de metacampos, identificadores de campos personalizados ni rutas de interfaz. Por ello, la matriz siguiente indica destinos funcionales propuestos para confirmar; no constituye un mapeo técnico verificado de producción. No se asignan identificadores inventados.

| **Campo** | **NetSuite** | **Odoo** | **Shopify** |
|----|----|----|----|
| Código de barras | Código de barras del artículo variante | Código de barras de variante | Código de barras de variante |
| Marca principal | Agrupación de marca del modelo | Agrupación de marca de plantilla | Agrupación de marca de producto |
| WB N.º de estilo | Estilo del modelo o artículo padre | Estilo de plantilla | Estilo de producto |
| WB SKU | Código comercial del artículo variante | Referencia de variante | SKU de variante |
| WB Talla | Talla del artículo variante | Atributo talla de variante | Opción talla de variante |
| WB Talla de EE. UU. | Talla US del artículo variante | Talla US de variante | Talla US de variante |
| WB Marca | Marca del modelo | Marca de plantilla | Marca de producto |
| WB Descripcion | Descripción corta del modelo | Nombre o descripción de plantilla | Título o descripción corta de producto |
| WB División | Clasificación división del artículo | Clasificación división de plantilla | Clasificación división de producto |
| WB Categoría | Clasificación categoría del artículo | Categoría de plantilla | Clasificación categoría de producto |
| WB Género | Género del modelo | Género de plantilla | Género de producto |
| WB Licencia | Licencia del modelo | Licencia de plantilla | Licencia de producto |
| WB Temporada | Temporada del modelo | Temporada de plantilla | Temporada de producto |
| WB Ciclo de vida | Ciclo de vida del modelo | Ciclo de vida de plantilla | Ciclo de vida de producto |
| WB Color | Color del artículo variante | Atributo color de variante | Opción color de variante |
| WB Fit | Fit del modelo | Fit de plantilla | Fit de producto |
| WB Silueta | Silueta del modelo o variante | Silueta de plantilla o variante | Silueta de producto o variante |
| WB Composición | Composición del modelo | Composición de plantilla | Composición de producto |
| WB Descripción larga | Descripción extensa del artículo | Descripción de plantilla | Descripción de producto |
| WB País de origen | Origen del artículo | Origen de plantilla | Origen de producto |
| Unidad | Unidad comercial del artículo | Unidad comercial de producto | Unidad comercial de producto o variante |
| SAT Clave de producto | Clave de producto del artículo | Clave de producto de plantilla | Clave de producto de referencia |
| Enlace de imagen | Imagen del artículo | Imagen de plantilla o variante | Imagen de producto o variante |
| Precio de compra | Costo del artículo variante | Costo de producto o variante | Costo de variante |
| Precio de venta | Precio del artículo variante | Precio de venta de producto o variante | Precio de variante |

### Información necesaria para confirmar los destinos

Para cada plataforma se debe registrar: nombre visible, pantalla o sección, identificador técnico, nivel padre o variante, tipo de dato, lista permitida, condición de obligatoriedad y columna de importación. Verificar si el destino es nativo o personalizado. No debe asumirse que todos los campos tienen un destino nativo o que el mismo nombre visible implica la misma función.

En Shopify WB y Stetson confirmar por separado los destinos, la configuración de talla y color y las reglas de precios. En Odoo y NetSuite confirmar el registro que representa al padre y la relación con las variantes. La prueba debe incluir una exportación y una recarga controlada con comparación de valores.

## Estructura de los archivos validadores

| **Columna** | **Contenido** | **Función** |
|----|----|----|
| A | WB N.º de estilo | Entrada del modelo |
| B | WB SKU | Entrada de variante |
| C | Código de barras | Entrada y activador del resultado |
| D | Precio de venta | Entrada para regla Shopify |
| E | WB Talla | Entrada para regla NetSuite |
| F | V1 Formato UPC | Longitud de Código de barras |
| G | V2 UPC Repetido | Duplicado interno de Código de barras |
| H | V4 SKU Repetido | Duplicado interno de SKU |
| I | V6 Faltan Datos | Estilo vacío con Código de barras presente |
| J y K | Reglas específicas | Dependen de plataforma; algunos espacios están vacíos |
| L | MOTIVO Semáforo | Concatena incidencias o indica PASA |

La hoja Catálogo estándar tiene encabezado en fila 1 y fórmulas observadas entre filas 2 y 200. Export_Tienda solo contiene el encabezado Código de Barras Actual (Pegar aquí para cruce). En las fórmulas revisadas no hay referencias a esa hoja; el cruce externo no está implementado por estos archivos.

## Validaciones existentes en los cuatro archivos

| **Control** | **Lógica observada** | **Límite del control** |
|----|----|----|
| V1 | Si C tiene valor, LEN(C) debe estar entre 12 y 14. | No revisa que todos los caracteres sean dígitos ni el dígito de control. |
| V2 | Si C tiene valor, COUNTIF(C:C,C) mayor que 1 señala duplicado. | Detecta coincidencias dentro del archivo, no contra otro sistema. |
| V4 | Si B tiene valor, COUNTIF(B:B,B) mayor que 1 señala duplicado. | No rechaza por sí mismo SKU vacío. |
| V6 | Si C tiene valor y A está vacío, señala Falta Estilo. | No exige todos los campos del catálogo. |
| Resultado | Si C está vacío, L queda vacío. Si las incidencias F a K están vacías, indica PASA. | Resultado vacío no equivale a aprobación. PASA solo cubre las comprobaciones presentes. |

## Reglas específicas por plataforma

### NetSuite G1522

La columna J señala N2 Talla cero o vacía cuando C tiene valor y E es el texto 0 o está vacía. La columna K no aporta una regla adicional en las filas revisadas. El control de talla cero contradice Criterios para Talla Ropa Dama numérica, donde 0 es válido. Debe resolverse por familia de talla antes de bloquear una variante legítima; los libros no se modificaron.

### Odoo G1522

Las columnas J y K están vacías en las filas revisadas. Aplica los controles comunes, sin reglas adicionales de talla o precio en este archivo.

### Shopify Western Brothers

La columna J exige B = C cuando existe Código de barras. La columna K calcula INT(D × 1.16), lo convierte a texto y exige que el último carácter sea 9. Esta fórmula verifica el último dígito de la parte entera; no comprueba decimales ni realiza un redondeo comercial. Si D está vacío, no genera incidencia de precio. Ejemplo explicativo: un precio base de 775 produce 899 con el factor del archivo y satisface el control.

### Shopify Stetson

La columna J exige MOD(D × 1.16, 50) = 0 cuando D tiene valor. La columna K está vacía en las filas revisadas. La regla equivale a exigir que el precio calculado con el factor del archivo sea múltiplo de 50. No existe tolerancia de redondeo en la fórmula; los decimales de origen pueden afectar la comparación. Si D está vacío, el control no reporta falta de precio.

El factor 1.16 se documenta como parte de las fórmulas suministradas. No prueba una política fiscal universal ni confirma que todo Precio de venta del archivo origen sea una base sin impuestos. Antes de ejecutar estos controles, confirmar moneda, tratamiento de impuestos y precisión.

## Controles en HojaProductos Prelimpieza

En Productos, AA contiene Estatus de Validación y AB Detalle de Discrepancias. Las fórmulas revisadas detectan UPC vacío o con la palabra FALTA, Código de barras duplicado y SKU duplicado. También revisan División, Categoría, Género, Temporada y Ciclo de vida y la coherencia entre Categoría y División.

Los faltantes de clasificación se etiquetan como avisos, y el estatus puede seguir siendo Válido cuando solo hay avisos. Las fórmulas contienen referencias externas como \[2\]Criterios y \[2\]Productos_Resumen. No se ha comprobado su resolución o recálculo. Esto impide tratar el estatus almacenado como evidencia suficiente de calidad o como bloqueo de carga.

Los campos AA a AM son de validación, revisión, inventario, procedencia o precios vigentes; quedan fuera del núcleo documental de 25 atributos. Deben conservarse como apoyo de control cuando se utilice el archivo maestro, sin enviarlos automáticamente como atributos del producto a otras plataformas.

## Controles complementarios para una carga

Los siguientes controles son requisitos operativos propuestos para completar el proceso; no se presentan como funciones ya implementadas en los validadores. Un archivo Excel con incidencias no impide técnicamente una importación al sistema. El bloqueo efectivo requiere una política de revisión o una integración que haga cumplir estos controles.

| **Control propuesto** | **Criterio de revisión** |
|----|----|
| Integridad de llaves | Fila de producto con SKU, Código de barras y Estilo según operación. Código de barras solo con dígitos, longitud admitida y ceros preservados. |
| Duplicados internos | SKU o Código de barras duplicados deben revisarse. Estilo repetido entre variantes es esperado. |
| Cruce externo | Comparar contra exportación vigente de cada destino. Código existente puede ser actualización del mismo registro o conflicto de identidad; resolver antes de cargar. |
| Clasificación | Valores exactos de Criterios y División coherente con Categoría. Un faltante por desconocimiento requiere revisión. |
| Tallas | Pareja MX y US válida para su familia, género y proveedor. Conservar sufijos de ancho. Admitir talla 0 cuando la familia la permite. |
| Atributos condicionales | Fit y Silueta se exigen solo cuando corresponde y existe evidencia. Los atributos improcedentes permanecen vacíos. |
| Precio | Aplicar la regla de la tienda correcta con moneda, base e impuestos confirmados. Resolver precisión antes de comparar. |
| Correspondencia de variante | Evitar que SKU y Código de barras apunten a variantes distintas en origen y destino. |
| Lectura posterior | Reexportar tras la carga y comparar llaves, tallas, clasificación, precios y valores vacíos con el archivo aprobado. |

## Secuencia de validación y carga

### Preparar

Conservar el archivo origen y exportar el catálogo vigente del destino con fecha de corte. Definir si se crearán o actualizarán registros.

### Normalizar

Aplicar Criterios, convertir atributos improcedentes a campos vacíos y documentar dudas. Mantener los identificadores como texto.

### Validar

Ejecutar controles internos, controles por tienda y cruce externo. Revisar también filas sin Código de barras, que no generan resultado en los validadores.

### Resolver

Registrar campo, valor origen, incidencia, corrección, evidencia y responsable de validación. No resolver contradicciones con valores inventados.

### Confirmar mapeo

Verificar los destinos técnicos y la forma en que una celda vacía se interpreta en creación o actualización. No asumir que un vacío elimina un valor existente.

### Probar y cargar

Realizar primero una prueba controlada por familia y tienda. Importar solo registros aprobados y conservar el resultado de la carga.

### Conciliar

Reexportar y comparar. Cerrar las incidencias solo después de confirmar que los valores quedaron en la variante correcta.

## Pendientes para completar el mapeo técnico

Confirmar la enumeración definitiva de 25 campos; comprobar en cada cuenta las rutas y los identificadores personalizados; resolver la regla de talla cero de NetSuite; confirmar aplicaciones de Silueta; implementar o ejecutar el cruce externo; resolver las referencias externas del maestro; y verificar el comportamiento de campos vacíos y precios en una importación controlada. XXL queda confirmado como valor estándar y sustituye 2XL en la captura.

## Fuentes y trazabilidad

HojaProductos_Prelimpieza.xlsx: Productos A1:Z1, ejemplos A2:Z3, fórmulas AA2:AB4 y precios vigentes AL2:AM4; Criterios secciones 1 a 8 y columnas AA y AB para listas editables. Los 14 textos pegados proporcionados contienen la misma versión de la guía y se contrastaron con el libro.

Validador_NetSuite_G1522.xlsx: Catálogo estándar, encabezados A1:L1, fórmulas F2:L4 y extensión de fórmulas hasta fila 200; Export_Tienda A1. Las reglas descritas se derivan de las fórmulas, sin afirmar ejecución contra sistemas productivos.

Validador_Odoo_G1522.xlsx: Catálogo estándar, encabezados A1:L1, fórmulas F2:L4 y extensión de fórmulas hasta fila 200; Export_Tienda A1. Las reglas descritas se derivan de las fórmulas, sin afirmar ejecución contra sistemas productivos.

Validador_Shopify_WB.xlsx: Catálogo estándar, encabezados A1:L1, fórmulas F2:L4 y extensión de fórmulas hasta fila 200; Export_Tienda A1. Las reglas descritas se derivan de las fórmulas, sin afirmar ejecución contra sistemas productivos.

Validador_Shopify_Stetson.xlsx: Catálogo estándar, encabezados A1:L1, fórmulas F2:L4 y extensión de fórmulas hasta fila 200; Export_Tienda A1. Las reglas descritas se derivan de las fórmulas, sin afirmar ejecución contra sistemas productivos.

## Informe de rutas de pantalla e identificadores técnicos

La consulta pública confirma campos y rutas estándar; no revela la configuración privada de G1522. Referencias consultadas el 5 de octubre de 2026. NetSuite usa como referencia el formulario estándar Inventory Item y Records Browser 2025.2. Odoo usa el código oficial 19.0 y la guía de variantes master, con referencias de importación 18.0. Shopify GraphQL Admin latest consultado corresponde a 2026-10. Confirmar las versiones efectivamente instaladas antes de implementar.

En las matrices, Nativo significa identificador documentado públicamente y candidato funcional, no correspondencia confirmada del campo WB. Propuesto significa diseño recomendado para G1522 si no existe ya un campo equivalente. No crear duplicados de campos existentes. Los identificadores personalizados propuestos no se han localizado ni creado en ninguna cuenta.

| **Plataforma** | **Registro padre** | **Registro variante y vínculo** |
|----|----|----|
| NetSuite | Artículo padre de matriz cuando la función está habilitada | Artículo hijo; parent referencia al padre. El tipo de artículo real depende de la cuenta. \[N1 N4\] |
| Odoo | product.template | product.product; product_tmpl_id referencia a plantilla. \[O2 O3\] |
| Shopify | Product | ProductVariant; product referencia al producto, inventoryItem enlaza inventario. \[S1 S2 S3\] |

### Rutas de NetSuite

| **Código** | **Ruta de pantalla y uso** |
|----|----|
| NS1 | Lists \> Accounting \> Items \> abrir artículo \> Primary Information. itemid, upccode, displayname y parent. \[N1 N4\] |
| NS2 | Artículo \> Sales / Pricing. salesdescription y precios por nivel y moneda. \[N1 N6\] |
| NS3 | Artículo \> Purchasing / Inventory. Revisar Purchase Price y datos de fabricación; ubicación exacta según formulario. \[N2\] |
| NS4 | Customization \> Lists, Records, & Fields \> Item Fields \> abrir definición. Revisar ID, tipo, aplicación y Subtab. \[N3\] |
| NS5 | Customization \> Lists, Records, & Fields \> Lists. Revisar listas de opciones; para matrices, la definición del campo y su pestaña Matrix. \[N4\] |
| NS6 | Home \> Set Preferences \> General \> Defaults \> Show Internal IDs. Abrir ayuda del campo desde su etiqueta para identificarlo. \[N5\] |

Los identificadores NetSuite que se muestran en la matriz son de SuiteScript y están en minúsculas. SuiteTalk puede usar nombres con otra capitalización, por ejemplo itemId. Un ID de campo no es el número Internal ID del registro ni el ID de una opción de lista. \[N1 N5\]

### Rutas de Odoo

| **Código** | **Ruta de pantalla y uso** |
|----|----|
| OD1 | Sales / Ventas \> Products / Productos \> Products / Productos \> abrir producto. Plantilla del modelo comercial. \[O1\] |
| OD2 | Producto \> botón inteligente Variants / Variantes \> abrir combinación. Referencia interna y código de barras de variante. \[O1 O3\] |
| OD3 | Sales \> Configuration \> Settings \> Product Catalog \> Variants. Habilitación de variantes cuando corresponde. \[O1\] |
| OD4 | Plantilla \> Attributes and Variants / Atributos y variantes. Configuración de valores de talla y color; identificar los atributos en la base. \[O1 O2\] |
| OD5 | Abrir el producto y Studio \> seleccionar campo \> propiedades y Technical Name. Consultar nombre real y modelo. Ruta sujeta a disponibilidad de Studio. \[O4\] |
| OD6 | Lista de registros \> seleccionar \> Action / Acción \> Export / Exportar. Obtener una exportación compatible con importación y su External ID. Menú exacto según versión. \[O5\] |

Los campos personalizados usan prefijo x\_; los creados con Studio conservan x_studio\_. Los nombres de este informe son propuestas y pueden diferir de los instalados. La inspección debe registrar modelo, nombre técnico, tipo y si el campo es calculado, relacionado o editable. \[O4\]

### Rutas de Shopify

| **Código** | **Ruta de pantalla y uso** |
|----|----|
| SH1 | Admin \> Products / Productos \> abrir producto. Título, descripción, organización y medios del padre. \[S1\] |
| SH2 | Products \> producto \> Variants / Variantes \> abrir variante. Opciones, precio, inventario, costo y datos de envío según permisos. \[S4 S3\] |
| SH3 | Settings / Configuración \> Metafields and metaobjects / Metacampos y metaobjetos \> Products o Variants \> definición. Registrar namespace, key, tipo y validaciones. \[S5\] |
| SH4 | Products \> producto o variante \> Metafields. Captura de atributos adicionales. Add definition permite crear la definición si está autorizado. \[S5\] |
| SH5 | Products \> producto \> Variants \> opciones de talla o color. Verificar si son opciones propias o están conectadas a metacampos. \[S7\] |

En GraphQL Admin 2026-10, ProductVariant publica barcodes y los objetos ProductVariantBarcode contienen value y type. Por eso el mapeo actual de códigos es ProductVariant.barcodes.nodes\[\].value; la integración debe seleccionar explícitamente el código maestro G1522. No confundir esta ruta con el campo barcode de Storefront o de versiones anteriores. \[S2 S6\]

## Matriz técnica de los 25 atributos en NetSuite

| **Campo** | **ID o destino** | **Ruta y condición** |
|----|----|----|
| Código de barras | upccode | NS1. Nativo texto; conservar ceros. \[N1 N2\] |
| Marca principal | custitem_g1522_marca_principal | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB N.º de estilo | custitem_g1522_estilo | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB SKU | itemid | NS1. Nativo candidato. Confirmar si WB SKU está en un campo personalizado distinto. \[N1\] |
| WB Talla | custitem_g1522_talla_mx | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Talla de EE. UU. | custitem_g1522_talla_us | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Marca | custitem_g1522_marca | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Descripcion | displayname | NS1. Nativo candidato para nombre visible. \[N1\] |
| WB División | custitem_g1522_division | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Categoría | custitem_g1522_categoria | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Género | custitem_g1522_genero | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Licencia | custitem_g1522_licencia | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Temporada | custitem_g1522_temporada | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Ciclo de vida | custitem_g1522_ciclo_vida | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Color | custitem_g1522_color | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Fit | custitem_g1522_fit | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Silueta | custitem_g1522_silueta | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Composición | custitem_g1522_composicion | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| WB Descripción larga | salesdescription | NS2. Nativo candidato para descripción de venta. \[N1\] |
| WB País de origen | countryofmanufacture | NS3. Nativo candidato; seleccionar referencia de país. \[N2\] |
| Unidad | unitstype + saleunit | NS1. Nativos de tipo y unidad de venta; mapear PZS y PRS a IDs de unidades. \[N1\] |
| SAT Clave de producto | custitem_g1522_sat_clave_producto | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| Enlace de imagen | custitem_g1522_imagen_url | NS4. Propuesto. Tipo y lista según diccionario. Confirmar ID instalado; talla y color pueden ser opciones Matrix. \[N3 N4\] |
| Precio de compra | cost | NS3. Nativo Purchase Price, no confundir con averagecost. \[N2\] |
| Precio de venta | Sublista price en REST; matriz de precios en SuiteScript | NS2. Elegir moneda, nivel y cantidad; no es un campo plano universal. \[N6\] |

No asignar automáticamente WB División a department ni WB Categoría a class: son clasificaciones contables u organizativas cuya equivalencia debe confirmarse. Los campos WB personalizados deben preservarse cuando ya existan. El estilo se propone como campo del padre; no se sustituye por el SKU de cada hijo.

## Matriz técnica de los 25 atributos en Odoo

| **Campo** | **Modelo y nombre técnico** | **Ruta y condición** |
|----|----|----|
| Código de barras | product.product.barcode | OD2. Nativo Char. \[O3\] |
| Marca principal | product.template.x_studio_g1522_marca_principal | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB N.º de estilo | product.template.x_studio_g1522_estilo | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB SKU | product.product.default_code | OD2. Nativo Internal Reference. \[O3\] |
| WB Talla | product.template.attribute_line_ids; product.product.product_template_attribute_value_ids | OD4 OD2. Nativos relacionales. Identificar el atributo de talla y su valor; no son un campo simple talla. \[O2 O3\] |
| WB Talla de EE. UU. | product.product.x_studio_g1522_talla_us | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Marca | product.template.x_studio_g1522_marca | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Descripcion | product.template.name | OD1. Nativo candidato; nombre del producto. \[O2\] |
| WB División | product.template.x_studio_g1522_division | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Categoría | product.template.categ_id | OD1. Nativo candidato Many2one a product.category; mapear por ID. \[O2\] |
| WB Género | product.template.x_studio_g1522_genero | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Licencia | product.template.x_studio_g1522_licencia | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Temporada | product.template.x_studio_g1522_temporada | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Ciclo de vida | product.template.x_studio_g1522_ciclo_vida | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Color | product.template.attribute_line_ids; product.product.product_template_attribute_value_ids | OD4 OD2. Nativos relacionales. Identificar atributo Color y valor. \[O2 O3\] |
| WB Fit | product.template.x_studio_g1522_fit | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Silueta | product.template.x_studio_g1522_silueta | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Composición | product.template.x_studio_g1522_composicion | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| WB Descripción larga | product.template.description_sale | OD1. Nativo candidato de descripción para ventas; web puede usar otro campo de módulo. \[O2\] |
| WB País de origen | product.template.x_studio_g1522_pais_origen | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| Unidad | product.template.uom_id | OD1. Nativo Many2one a uom.uom. Confirmar equivalencias PZS y PRS. \[O2\] |
| SAT Clave de producto | product.template.x_studio_g1522_sat_clave_producto | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| Enlace de imagen | product.template.x_studio_g1522_imagen_url | OD5. Propuesto; revisar módulos y campos ya instalados. Tipo conforme al diccionario. \[O4\] |
| Precio de compra | product.product.standard_price | OD2. Nativo Cost; no equivale siempre al precio de proveedor product.supplierinfo. \[O3\] |
| Precio de venta | product.template.list_price; product.product.lst_price; price_extra | OD1 OD2. Precio base y precio calculado de variante; revisar listas de precios para diferencias independientes. \[O2 O3\] |

No usar default_code de la plantilla para almacenar el estilo: cuando hay variantes la referencia comercial se maneja por product.product. El campo largo se propone como description_sale por función; si la descripción es para ecommerce, se debe inspeccionar el módulo web antes de elegir el destino. image_1920 representa datos de imagen, no un enlace URL; conservar Enlace de imagen en un campo de texto o resolver la descarga en la integración. \[O2 O3\]

## Matriz técnica de los 25 atributos en Shopify

| **Campo** | **Objeto y campo técnico** | **Ruta y condición** |
|----|----|----|
| Código de barras | ProductVariant.barcodes.nodes\[\].value | SH2. Nativo 2026-10; type identifica el estándar. Confirmar selección del código maestro. \[S2 S6\] |
| Marca principal | Product.metafield(namespace: g1522, key: marca_principal) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB N.º de estilo | Product.metafield(namespace: g1522, key: estilo) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB SKU | ProductVariant.sku; InventoryItem.sku | SH2. Nativos; misma identidad de variante en producto e inventario. \[S2 S3\] |
| WB Talla | Product.options; ProductVariant.selectedOptions | SH5. Nativos; nombre de opción Talla propuesto, confirmar el instalado. \[S1 S2 S7\] |
| WB Talla de EE. UU. | ProductVariant.metafield(namespace: g1522, key: talla_us) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB Marca | Product.vendor | SH1. Nativo candidato solo si vendor se usa como marca. \[S1\] |
| WB Descripcion | Product.title | SH1. Nativo candidato para título. \[S1\] |
| WB División | Product.metafield(namespace: g1522, key: division) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB Categoría | Product.productType; Product.category | SH1. productType candidato de categoría propia; category es taxonomía Shopify y necesita cruce, no copiar texto WB sin más. \[S1\] |
| WB Género | Product.metafield(namespace: g1522, key: genero) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB Licencia | Product.metafield(namespace: g1522, key: licencia) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB Temporada | Product.metafield(namespace: g1522, key: temporada) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB Ciclo de vida | Product.metafield(namespace: g1522, key: ciclo_vida) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB Color | Product.options; ProductVariant.selectedOptions | SH5. Nativos; nombre de opción Color propuesto. \[S1 S2 S7\] |
| WB Fit | Product.metafield(namespace: g1522, key: fit) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB Silueta | Product.metafield(namespace: g1522, key: silueta) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB Composición | Product.metafield(namespace: g1522, key: composicion) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| WB Descripción larga | Product.descriptionHtml | SH1. Nativo candidato. description es lectura de texto sin etiquetas; controlar la conversión a HTML. \[S1\] |
| WB País de origen | InventoryItem.countryCodeOfOrigin | SH2. Nativo candidato de origen para envío; requiere código de país, no nombre libre. \[S3\] |
| Unidad | ProductVariant.metafield(namespace: g1522, key: unidad) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| SAT Clave de producto | Product.metafield(namespace: g1522, key: sat_clave_producto) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| Enlace de imagen | Product.metafield(namespace: g1522, key: imagen_url) | SH3 SH4. Propuesto. El namespace y key reales deben obtenerse de la definición. \[S5\] |
| Precio de compra | InventoryItem.unitCost.amount | SH2. Nativo de lectura de costo; moneda de tienda y permisos. Confirmar input de escritura para la versión usada. \[S3\] |
| Precio de venta | ProductVariant.price | SH2. Nativo en moneda de tienda; política de impuestos de la tienda por confirmar. \[S2\] |

Enlace de imagen se conserva como metacampo URL propuesto; Product.media y los medios de variante son recursos de imagen, no el mismo dato textual. Unidad PZS o PRS requiere metacampo si se desea conservar el estándar; unitPriceMeasurement expresa otra función y no es sustituto directo. SAT Clave de producto no debe reemplazarse por harmonizedSystemCode, que corresponde a clasificación aduanera. \[S1 S2 S3\]

## Especificación propuesta de campos adicionales

La convención g1522 es un diseño sugerido para destinos faltantes. Reutilizar los nombres reales cuando ya exista una implementación. No crear estos campos ni cambiar las cuentas únicamente por el hecho de aparecer en el informe.

| **Tipo de atributo** | **NetSuite** | **Odoo** | **Shopify** |
|----|----|----|----|
| Lista cerrada | List / Record con lista controlada | Selection o Many2one a catálogo | single_line_text_field con validación de valores cuando esté disponible |
| Identificador y texto corto | Free Form Text | Char | single_line_text_field |
| Descripción extensa | Long Text según capacidad | Text o Html según uso | multi_line_text_field o descripción HTML nativa |
| Enlace de imagen | Hyperlink o texto URL | Char con presentación URL | url; file_reference solo si se administra archivo |
| Precio adicional | Currency con contexto | Monetary con moneda o Float según modelo | money cuando se almacene como metacampo |

## Registro necesario para confirmar cada campo instalado

Registrar por campo y plataforma: tienda o base, versión, rol, formulario, etiqueta visible, código de ruta, ID técnico real, modelo u objeto, nivel padre o variante, tipo, destino de lista y IDs de valores, condición de obligatoriedad, permisos, encabezado de exportación, formato de importación, tratamiento del vacío y evidencia de prueba. Para campos personalizados el ID se obtiene de la cuenta, no de una búsqueda pública.

### Casos mínimos de comprobación

| **Caso** | **Resultado esperado** |
|----|----|
| Modelo con dos tallas | Un padre y dos variantes; estilo común y llaves distintas. |
| Talla de ropa XXL | Conservar XXL en catálogo y opciones; convertir 2XL a XXL durante normalización. |
| Accesorio sin talla | Talla única y One Size; Fit vacío y Silueta vacía si no corresponde. |
| Talla numérica 0 | Aceptar cuando pertenece a familia válida; revisar conflicto del validador NetSuite. |
| Código con cero inicial | Conservar texto y valor íntegro al exportar e importar. |
| Código existente en destino | Actualizar el mismo registro solo si se confirma identidad; detener conflicto entre variantes. |
| Vacío en actualización | Confirmar si conserva o elimina el valor existente; documentar por mecanismo de carga. |
| Precios por tienda | Aplicar regla WB o Stetson con base e impuestos confirmados; comparar valor final. |
| Talla MX repetida con distintos anchos | Mantener variantes y talla US completa; evitar colisión por reducir la combinación. |

### Estado de completitud del informe

Quedan cubiertos el diccionario, las rutas públicas, los IDs estándar y el diseño propuesto de destinos faltantes. No se han inspeccionado las cuentas privadas ni ejecutado cargas. La correspondencia de los campos WB personalizados, las listas y sus IDs, la versión instalada y los resultados productivos permanecen por confirmar con evidencia de cada cuenta.

## Referencias oficiales del informe técnico

\[N1\] Oracle formulario Inventory Item e identificadores. https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_0614012133.html

\[N2\] Oracle SuiteScript Records Browser Inventory Item 2025 2. https://www.netsuite.com/help/helpcenter/en_US/srbrowser/Browser2025_2/script/record/inventoryitem.html

\[N3\] Oracle configuración de campos de artículo. https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2827818.html

\[N4\] Oracle matrices de artículos. https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N2228669.html

\[N5\] Oracle visualización de identificadores. https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N3420345.html

\[N6\] Oracle sublista de precios. https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_159531460854.html

\[O1\] Odoo variantes y navegación. https://www.odoo.com/documentation/master/applications/sales/sales/products_prices/products/variants.html

\[O2\] Odoo código oficial de product.template rama 19 0. https://github.com/odoo/odoo/blob/19.0/addons/product/models/product_template.py

\[O3\] Odoo código oficial de product.product rama 19 0. https://github.com/odoo/odoo/blob/19.0/addons/product/models/product_product.py

\[O4\] Odoo Studio campos y nombres técnicos. https://www.odoo.com/documentation/19.0/applications/studio/fields.html

\[O5\] Odoo importación y exportación. https://www.odoo.com/documentation/18.0/applications/essentials/export_import_data.html

\[S1\] Shopify Product GraphQL Admin. https://shopify.dev/docs/api/admin-graphql/latest/objects/Product

\[S2\] Shopify ProductVariant GraphQL Admin. https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant

\[S3\] Shopify InventoryItem GraphQL Admin. https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem

\[S4\] Shopify edición de variantes. https://help.shopify.com/en/manual/products/variants/edit-variants

\[S5\] Shopify definiciones de metacampos. https://help.shopify.com/en/manual/custom-data/metafields/metafield-definitions/creating-custom-metafield-definitions

\[S6\] Shopify ProductVariantBarcode GraphQL Admin. https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariantBarcode

\[S7\] Shopify opciones conectadas a metacampos. https://help.shopify.com/en/manual/custom-data/metafields/add-variants-with-metafields
