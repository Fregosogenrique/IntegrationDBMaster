# Anatomía de productos y atributos estándar

*Estructura padre y variante y reglas de captura del catálogo G1522*

Grupo G1522 \| Versión 1.0 \| 5 de octubre de 2026

Este documento define cómo representar un modelo comercial y sus variantes, cómo identificar cada variante y cómo llenar los atributos del catálogo. La autoridad de captura es la hoja Criterios de HojaProductos_Prelimpieza.xlsx. Los valores que antes representaban un atributo que no corresponde se dejan en blanco. Un dato desconocido también se deja vacío, pero debe registrarse para revisión.

## Estructura del producto

El padre reúne los atributos compartidos del modelo comercial. La variante representa una configuración vendible, por ejemplo una talla y un color. Dos unidades físicas de una misma variante comparten SKU y código de barras; el catálogo no asigna un identificador nuevo por cada unidad en inventario. Esta separación traduce el nivel padre y el nivel hijo descritos en el reporte de avances.

| **Nivel** | **Identificación** | **Atributos principales** |
|----|----|----|
| Padre o modelo | Marca y WB N.º de estilo | Marca, descripción, división, categoría, género, temporada, ciclo de vida y características compartidas. |
| Variante vendible | WB SKU y Código de barras | Talla, talla de EE. UU., color, unidad y datos propios de la variante. |
| Unidad física | No se individualiza en estos archivos | Las existencias contabilizan piezas de una variante; no hay serie individual documentada. |

El nivel de cada atributo en este documento es una propuesta de organización del estándar. Los archivos no contienen un esquema técnico de relaciones padre e hijo. Si composición, silueta, imagen o precio cambia entre variantes, debe conservarse la diferencia en el nivel que corresponda, sin sobrescribirla por herencia.

### Ejemplo tomado de Productos

| **Estilo padre** | **Código de barras** | **SKU variante** | **Talla MX y EE UU** |
|----|----|----|----|
| 11-004-1312-4039 | 052356088867 | 11-004-1312-4039-29 32 | 29 x 32 / 29W / 32L |
| 11-004-1312-4039 | 052356088928 | 11-004-1312-4039-30 32 | 30 x 32 / 30W / 32L |

Fuente del ejemplo: Productos, filas 2 y 3. El estilo se repite porque agrupa el mismo modelo. Los identificadores y tallas cambian entre variantes. Se conserva el cero inicial del código de barras.

## Llaves de identificación

Código de barras y WB SKU identifican la variante dentro del catálogo. WB N.º de estilo identifica el modelo y puede repetirse en sus variantes. El identificador interno de Productos columna B es una referencia del sistema de origen; no debe sustituir las llaves comerciales ni asumirse portable entre plataformas.

La denominación UPC se usa en los validadores como nombre de control. Su fórmula admite longitudes de 12 a 14 caracteres y no comprueba que sean dígitos ni valida el dígito de control. Por tanto, una longitud aceptada por el archivo no prueba por sí sola la validez del código.

## Regla de campos vacíos

Cuando un atributo no corresponda, dejar la celda realmente vacía, sin escribir un texto sustituto, guion, cero o espacio. Cuando la información sea desconocida o contradictoria, dejar el campo vacío y registrar el motivo en Revisión. Un blanco por falta de información no confirma que el atributo sea improcedente. Los productos sin talla usan Talla única y One Size, porque estos sí son valores válidos.

## Ruta de llenado

### Paso 1 Categoría y División

Busca en el nombre del producto una palabra de la tabla «2. Palabra clave → Categoría». Esa fila te da la Categoría y la División. Si no hay palabra clave, usa la lista «3. Categorías»; si no existe, no la inventes: anótala en Revisión.

### Paso 2 Género

Dama / Mujer → Mujer · Caballero / Hombre → Hombre · Niño / Niña según corresponda · Sombreros y accesorios sin género → Unisex. Usa solo los valores de «4. Listas básicas».

### Paso 3 Familia de talla

Con Categoría + Género ubica la familia en «3. Categorías» (columna Familia de talla). La familia define qué valores de talla son válidos.

### Paso 4 WB Talla

Capturar exactamente la talla del catálogo por familia. Homologar CH a S, MED a M, GDE a L y UNI a Talla única. Para ropa, usar XXL y XXXL como están en el catálogo. WB Talla expresa la venta en México y WB Talla de EE. UU. la etiqueta americana. No agregar equivalencias entre paréntesis.

### Paso 5 WB Talla de EE. UU.

Toma el valor de la misma fila del catálogo (columna «Talla de EE. UU.»). Si la regla dice «Igual», copia la WB Talla.

### Paso 6 Color

Elige el color base de «6. Colores». Nombres comerciales se traducen con la columna Sinónimos de la misma sección (ej. Cognac → Cafe). Si el nombre trae dos colores, usa el dominante.

### Paso 7 Temporada, Ciclo de vida, Unidad

Temporada y Ciclo de vida de «4. Listas básicas». Unidad: PRS para calzado (Botas, Zapatos, Tenis, Pantuflas); PZS para todo lo demás.

### Paso 8 Fit

Determina el fit usando la descripción larga y la tabla «7. Fit y Silueta». Aplica solo para Ropa y Denim. Usa "dejar el campo en blanco" en calzado, sombreros y accesorios.

### Paso 9 Silueta

Determina la silueta usando la descripción y la tabla «7. Fit y Silueta». Aplica solo para Sombreros, Calzado y Jeans. Usa "dejar el campo en blanco" en el resto.

### Paso 10 Si algo no cuadra

No inventes valores: deja el campo vacío y registra el caso en la hoja Revisión para validarlo.

El valor estándar confirmado es XXL. Si una fuente trae 2XL, homologar a XXL. La indicación contraria de la ruta original queda sustituida por esta regla. La regla general para Niño y Niña debe leerse junto con las familias infantiles específicas, como cinturones y jeans, para conservar la información de etiqueta.

## Listas básicas y marcas

| **Campo** | **Valores válidos** |
|----|----|
| División | Accesorios, Ropa, Denim, Calzado |
| Género | Hombre, Mujer, Niño, Niña, Unisex |
| Temporada | SS26, FW26, SS27, FW27, SS28, FW28 |
| Ciclo de vida | Seasonal, Core |
| Unidad | PZS, PRS |
| WB Marca | Roper, Denver, Ariat, Wrangler, Stetson, Montana West, Tru Western, Ranch & Corral, Jony Lama, Justin boots, Yellowstone, Generico, CAPSLAB, Happy Socks, REFLO, Willow Lane |
| Marca principal | Multimarca y las marcas de la lista anterior |

Los valores anteriores excluyen los textos sustituidos por un campo vacío. Las nuevas marcas, categorías o temporadas requieren actualización controlada de Criterios antes de su uso. No se agregan libremente durante la captura.

## Categorías división y familia de talla

| **Categoría** | **División** | **Familia de talla** |
|----|----|----|
| Bandanas | Accesorios | Talla única |
| Bolsos | Accesorios | Talla única |
| Botas | Calzado | Talla Calzado MX |
| Bufandas | Accesorios | Talla única |
| Calcetines | Ropa | Talla Calcetín |
| Camisas | Ropa | Talla Ropa |
| Carteras | Accesorios | Talla única |
| Chalecos | Ropa | Talla Ropa |
| Chamarras | Ropa | Talla Ropa |
| Cinturones | Accesorios | Talla Cinturón |
| Cobijas | Accesorios | Talla única |
| Cuchillos | Accesorios | Talla única |
| Cuidado de Botas | Accesorios | Contenido / Talla única |
| Cuidado de Sombreros | Accesorios | Contenido / Talla Ropa / Talla única |
| Equipaje | Accesorios | Talla única |
| Estuches | Accesorios | Talla única |
| Faldas | Ropa | Talla Ropa |
| Fragancias | Accesorios | Contenido |
| Gorras | Accesorios | Talla única |
| Hebillas | Accesorios | Talla única |
| Jeans | Denim | Hombre: Cintura Jean + Largo Jean · Mujer: Talla Jean Dama (Regular / Largo) · Niño/Niña: Talla Niño |
| Joyeria | Accesorios | Talla única |
| Jumpsuits | Ropa | Talla Ropa |
| Libros | Accesorios | Talla única |
| Llaveros | Accesorios | Talla única |
| Mascotas | Accesorios | Talla Ropa |
| Mochilas | Accesorios | Talla única |
| Pantalones | Ropa | Hombre: Cintura Jean + Largo Jean · Mujer: Talla Jean Dama |
| Pantuflas | Calzado | Talla Calzado MX |
| Pijamas | Ropa | Talla Ropa |
| Playeras | Ropa | Talla Ropa |
| Plumas para sombrero | Accesorios | Talla única |
| Shorts | Ropa | Hombre: Talla Short Hombre · Mujer: Talla Jean Dama (Regular) |
| Sombreros | Accesorios | Talla Sombrero |
| Sudaderas | Ropa | Talla Ropa |
| Sueteres | Ropa | Talla Ropa |
| Tenis | Calzado | Talla Calzado MX |
| Vestidos | Ropa | Talla Ropa (alfa) o Talla Ropa Dama numérica |
| Zapatos | Calzado | Talla Calzado MX |

## Asignación por palabras clave

Aplicar la primera coincidencia de la tabla de origen, respetando su orden. Cuando ninguna palabra coincida, elegir una categoría existente con evidencia. La clasificación requiere revisión si el nombre no permite resolverla.

| **Palabra clave**    | **Categoría**        | **División** |
|----------------------|----------------------|--------------|
| Cuidado de Botas     | Cuidado de Botas     | Accesorios   |
| Cuidado de Sombreros | Cuidado de Sombreros | Accesorios   |
| Plumas para sombrero | Plumas para sombrero | Accesorios   |
| Gorra                | Gorras               | Accesorios   |
| Sombrero             | Sombreros            | Accesorios   |
| Texana               | Sombreros            | Accesorios   |
| Bandana              | Bandanas             | Accesorios   |
| Bolso                | Bolsos               | Accesorios   |
| Bufanda              | Bufandas             | Accesorios   |
| Cartera              | Carteras             | Accesorios   |
| Clip para billetes   | Carteras             | Accesorios   |
| Cinturón             | Cinturones           | Accesorios   |
| Cobija               | Cobijas              | Accesorios   |
| Cuchillo             | Cuchillos            | Accesorios   |
| Equipaje             | Equipaje             | Accesorios   |
| Estuche              | Estuches             | Accesorios   |
| Fragancia            | Fragancias           | Accesorios   |
| Hebilla              | Hebillas             | Accesorios   |
| Joyería              | Joyeria              | Accesorios   |
| Llavero              | Llaveros             | Accesorios   |
| Libro                | Libros               | Accesorios   |
| Mochila              | Mochilas             | Accesorios   |
| Mascota              | Mascotas             | Accesorios   |
| Jean                 | Jeans                | Denim        |
| Bota                 | Botas                | Calzado      |
| Zapato               | Zapatos              | Calzado      |
| Tenis                | Tenis                | Calzado      |
| Pantufla             | Pantuflas            | Calzado      |
| Calcet               | Calcetines           | Ropa         |
| Camisa               | Camisas              | Ropa         |
| Sobrecamisa          | Camisas              | Ropa         |
| Chaleco              | Chalecos             | Ropa         |
| Chamarra             | Chamarras            | Ropa         |
| Falda                | Faldas               | Ropa         |
| Jumpsuit             | Jumpsuits            | Ropa         |
| Pantalón             | Pantalones           | Ropa         |
| Pijama               | Pijamas              | Ropa         |
| Playera              | Playeras             | Ropa         |
| Short                | Shorts               | Ropa         |
| Sudadera             | Sudaderas            | Ropa         |
| Suéter               | Sueteres             | Ropa         |
| Sueter               | Sueteres             | Ropa         |
| Vestido              | Vestidos             | Ropa         |

## Colores y sinónimos

| **Color base** | **Nombres comerciales y sinónimos** |
|----|----|
| Rojo | Red, Vino, Escarlata, Granate, Burgundy |
| Azul | Navy, Azul marino, Turquesa, Indigo, Mezclilla, Denim, Blue |
| Amarillo | Mostaza, Yellow |
| Verde | Olivo, Olive, Green |
| Naranja | Orange |
| Morado | Púrpura, Purple, Lila |
| Rosa | Pink |
| Negro | Black, Negra |
| Blanco | White, Hueso |
| Gris | Grey, Gray, Carbón, Charcoal |
| Beige | Crema, Arena, Tan, Khaki, Caqui, Sand |
| Cafe | Café, Brown, Cognac, Coñac, Chocolate, Tabaco, Taupe, Arcilla, Terracota, Camel, Miel, Marrón |
| Varios | Estampados multicolor sin color dominante o que no aparezca en la lista |

## Fit y silueta

| **Atributo y aplicación** | **Valores homologados** |
|----|----|
| Fit en Ropa y Denim | Regular, Relajado, Slim, Clásico, Moderno, Recto, Bootcut |
| Silueta de Sombreros | Copa Cattleman, Copa Rancher, Copa Pinch Front, Copa Gus, Copa Teardrop, Copa Open Road, Copa Brick |
| Silueta de Botas y Zapatos | Punta Redonda Ancha, Punta Cuadrada Ancha, Punta Redonda, Punta Cuadrada, Punta Ovalada, Punta Snip, Horma Alexia, Horma Agatha |
| Silueta de Jeans | Recto, Bootcut, Skinny, Tapered, Trouser |
| Otras aplicaciones | Dejar el campo en blanco cuando no corresponda. |

La lista editable de Silueta incluye Cierre perimetral, pero la tabla de aplicación no especifica su categoría. La ruta incluye Calzado en general y la tabla detallada solo Botas y Zapatos. Confirmar el uso de Cierre perimetral y la aplicación a Tenis o Pantuflas antes de asignarlos. Fit debe sustentarse en descripción larga o ficha técnica.

## Familias de talla y equivalencias

Cada equivalencia se valida como pareja de WB Talla y Talla de EE. UU. dentro de su familia. Un mismo valor MX puede tener distintas etiquetas US por anchura o proveedor. El catálogo completo de parejas permanece en Criterios, sección 8; los ejemplos siguientes explican su uso y no amplían las listas.

| **Familia** | **Regla y ejemplos** |
|----|----|
| Talla única | Gorras, carteras, hebillas, estuches y accesorios sin talla. UNI y OS se capturan así. Ejemplos: Talla única → One Size |
| Talla Ropa | Igual Ejemplos: XXS → XXS; XS → XS; S → S |
| Talla Ropa Dama numérica | Igual (vestidos y prendas dama con talla numérica US) Ejemplos: 0 → 0; 2 → 2; 4 → 4 |
| Cintura Jean + Largo Jean | Formato «Cintura x Largo». En web: filtro principal Cintura, Largo secundario. Ejemplos: 33 x 28 → 33W / 28L; 34 x 28 → 34W / 28L; 36 x 28 → 36W / 28L |
| Talla Jean Dama (Regular) | MX impar = US + 3. Cintura corporal ≈ 64 cm. La «R» (Regular) no se escribe: 0R → US 0 / MX 3. Ejemplos: 3 → 0; 5 → 2; 7 → 4 |
| Talla Jean Dama (Largo) | Mismas tallas con entrepierna larga (≈34 in vs 32 in Regular). 4L → MX «7 Largo» / US «4 Long». Ejemplos: 3 Largo → 0 Long; 5 Largo → 2 Long; 7 Largo → 4 Long |
| Talla Sombrero | Igual (fracción US) · ≈ 54 cm Ejemplos: 6 3/4 → 6 3/4; 6 7/8 → 6 7/8; 7 → 7 |
| Talla Calzado MX – Hombre | US = MX − 18 (tabla estándar; validar con fábrica) Ejemplos: 25 → 7; 25.5 → 7.5; 26 → 8 |
| Talla Calzado MX – Mujer | US = MX − 17 (tabla estándar; validar con fábrica) Ejemplos: 22 → 5; 22.5 → 5.5; 23 → 6 |
| Talla Calzado MX – Hombre (con ancho) | MX = US + 18. El sufijo (D, EE, RM, FS…) es el ancho/horma del proveedor y se captura tal cual. Ejemplos: 22 → 4 EE; 23 → 5 EE; 24 → 6 D |
| Talla Calzado MX – Mujer (con ancho) | MX = US + 17. El sufijo (B, C, RS, SM…) es el ancho/horma del proveedor y se captura tal cual. Ejemplos: 22 → 5 B; 22.5 → 5.5 B; 22.5 → 5.5 FS |
| Talla Cinturón – Hombre | Igual Ejemplos: 28 → 28; 30 → 30; 32 → 32 |
| Talla Cinturón – Mujer | Igual Ejemplos: S → S; M → M; L → L |
| Talla Cinturón – Niño | Cinturones infantiles numéricos (cintura en pulgadas). Igual Ejemplos: 18 → 18; 20 → 20; 22 → 22 |
| Talla Niño (numérica) | Talla por EDAD como principal (años pares). Ejemplos: 2 → 2; 4 → 4; 6 → 6 |
| Talla Niño (alfa US Youth) | Etiqueta US Youth XS = 4-5 años. En WB Talla va la edad; en US la letra. Ejemplos: 4 → XS; 6 → S; 8 → M |
| Talla Niño (jeans cintura) | Solo si la etiqueta trae cintura en pulgadas; mostrar la edad como apoyo. Ejemplos: 22 → 22W; 23 → 23W; 24 → 24W |
| Talla Calcetín | Por rango de calzado: MX 21–23 (Calzado Dama US 4–6). Calcetín sin talla → Talla única / One Size. Ejemplos: S → S; M → M; L → L |
| Talla Short Hombre | Igual Ejemplos: 27 → 27W; 28 → 28W; 29 → 29W |
| Talla Pantalón Dama Plus (W) | MX numérica; EE. UU. = número + W (Women's plus) Ejemplos: 10 → 10W; 12 → 12W; 14 → 14W |
| Talla Pantalón Hombre Big (W) | Cintura grande; EE. UU. = cintura + W Ejemplos: 46 → 46W; 48 → 48W; 50 → 50W |
| Talla Cintura numérica (Faldas / Shorts dama) | Cintura en pulgadas; MX y EE. UU. iguales Ejemplos: 24 → 24; 25 → 25; 26 → 26 |
| Contenido | WB Talla en ml; US en fl oz como lo declara el envase (≈ ml ÷ 29.57) Ejemplos: 22 ml → 0.75 fl oz; 30 ml → 1.0 fl oz; 44 ml → 1.5 fl oz |

Calzado adulto: la tabla usa US = MX − 18 para Hombre y US = MX − 17 para Mujer, con confirmación de fábrica. Con ancho, conservar el sufijo completo en la talla US. No generar combinaciones que no estén en el catálogo. El contenido se captura en ml y fl oz conforme al envase. La talla numérica 0 es válida en Talla Ropa Dama numérica y como equivalencia US de Talla Jean Dama Regular.

## Diccionario de atributos

Para organizar los 25 atributos solicitados, se excluye el Identificador interno de las 26 columnas A a Z de Productos. Esta es una delimitación documental, porque los archivos no enumeran formalmente cuáles son los 25 campos del reporte. La presencia de un campo en el estándar no significa que siempre deba estar lleno: aplican las reglas por categoría y los vacíos permitidos.

### Código de barras

Productos A. Nivel: Variante. Texto de 12 a 14 caracteres; conservar ceros iniciales. Identifica la variante comercial. Requerido para las filas a validar; comprobar dígitos y unicidad además de longitud.

### Marca principal

Productos C. Nivel: Padre. Texto de lista. Admite Multimarca y las marcas registradas en Criterios. No confundir la agrupación principal con la marca real del producto.

### WB N.º de estilo

Productos D. Nivel: Padre. Texto alfanumérico del modelo comercial, con guiones y formato del proveedor. Puede repetirse entre variantes del mismo modelo; no es llave única de variante.

### WB SKU

Productos E. Nivel: Variante. Texto del código comercial de la variante; conservar espacios, guiones y ceros significativos. Único por variante. En Shopify WB el validador exige que sea igual al código de barras.

### WB Talla

Productos F. Nivel: Variante. Texto exacto del catálogo de tallas de la familia correspondiente. Sin talla física: Talla única. No reemplazar por blanco una talla única válida.

### WB Talla de EE. UU.

Productos G. Nivel: Variante. Texto de la misma fila de equivalencia que WB Talla, incluida la anchura del proveedor. Si la regla es Igual, copiar WB Talla. No convertir sin confirmar familia y etiqueta.

### WB Marca

Productos H. Nivel: Padre. Texto exacto de la lista de marcas de Criterios. Representa la marca del producto. Una marca desconocida se registra para revisión.

### WB Descripcion

Productos I. Nivel: Padre. Texto descriptivo corto del producto. La fuente aporta ejemplos, pero no establece una longitud máxima ni sintaxis obligatoria.

### WB División

Productos J. Nivel: Padre. Lista cerrada: Accesorios, Ropa, Denim, Calzado. Debe coincidir con la división de WB Categoría.

### WB Categoría

Productos K. Nivel: Padre. Texto exacto de la tabla de categorías; se obtiene por palabra clave o selección validada. Usar la primera palabra clave coincidente; no inventar categorías.

### WB Género

Productos L. Nivel: Padre. Lista cerrada: Hombre, Mujer, Niño, Niña, Unisex. Dama se homologa a Mujer; Caballero a Hombre; accesorios sin género a Unisex.

### WB Licencia

Productos M. Nivel: Padre. Texto de la licencia respaldada por el producto o proveedor. Criterios no contiene lista cerrada ni regla detallada. Cuando no corresponda, dejar el campo en blanco.

### WB Temporada

Productos N. Nivel: Padre. Lista cerrada: SS26, FW26, SS27, FW27, SS28, FW28. No derivar la temporada de la fecha de captura; usar la información validada del producto.

### WB Ciclo de vida

Productos O. Nivel: Padre. Lista cerrada: Seasonal, Core. Cuando no corresponda, dejar el campo en blanco. No deducir Core a partir de stock.

### WB Color

Productos P. Nivel: Variante. Texto del color base de Criterios; normalizar nombres comerciales mediante sinónimos. Usar el dominante. Varios corresponde a multicolor sin dominante o al supuesto descrito en Criterios.

### WB Fit

Productos Q. Nivel: Padre. Lista homologada de corte para Ropa y Denim. En calzado, sombreros y accesorios, dejar el campo en blanco. Si falta evidencia en una prenda, registrar revisión.

### WB Silueta

Productos R. Nivel: Padre o variante. Lista homologada según sombrero, calzado o jeans. En otras categorías, dejar el campo en blanco. La horma puede requerir nivel variante si cambia entre piezas.

### WB Composición

Productos S. Nivel: Padre. Texto de materiales y porcentajes según etiqueta o ficha técnica. Sin lista o formato obligatorio en Criterios; no inventar materiales ni porcentajes.

### WB Descripción larga

Productos T. Nivel: Padre. Texto detallado sustentado en la ficha del producto. Sirve como evidencia para Fit y Silueta. La fuente no establece límite de caracteres ni formato HTML.

### WB País de origen

Productos U. Nivel: Padre. Texto del origen declarado por proveedor o etiqueta. Sin lista cerrada en Criterios. No deducir el origen de la marca.

### Unidad

Productos V. Nivel: Variante. Lista cerrada: PRS para Botas, Zapatos, Tenis y Pantuflas; PZS para lo demás. La unidad describe cómo se controla o vende el artículo; no es una cantidad.

### SAT Clave de producto

Productos W. Nivel: Padre. Identificador de texto de la clave asignada al producto. La fuente incluye ejemplos, pero no aporta catálogo SAT ni procedimiento fiscal de asignación.

### Enlace de imagen

Productos X. Nivel: Padre o variante. Texto con la dirección de la imagen asociada al producto o variante. La fuente no impone dominio ni extensión; confirmar que la imagen corresponda al producto.

### Precio de compra

Productos Y. Nivel: Variante. Valor numérico de costo; conservar precisión de origen. La hoja no declara moneda ni política general de impuestos; confirmar antes de importar.

### Precio de venta

Productos Z. Nivel: Variante. Valor numérico de venta; conservar precisión de origen. Los validadores Shopify aplican precio × 1.16. Confirmar la base del precio antes de usarlos.

## Fuentes y alcance

Fuente principal: HojaProductos_Prelimpieza.xlsx, hojas Criterios y Productos. Criterios secciones 1 a 8 y listas editables de Fit y Silueta en columnas AA y AB. Ejemplo de variantes: Productos filas 2 y 3. Referencias de control: los cuatro archivos Validador de NetSuite, Odoo, Shopify WB y Shopify Stetson. Los 14 textos pegados proporcionados reproducen el mismo contenido de Criterios; se usó la hoja del libro como autoridad.

Los campos sin regla específica en Criterios se describen por su encabezado y por ejemplos del libro, indicando expresamente el alcance de la evidencia. No se afirma que las reglas estén configuradas o verificadas en los sistemas productivos.

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

### Identificadores esenciales para la anatomía

| **Concepto** | **NetSuite** | **Odoo** | **Shopify** |
|----|----|----|----|
| SKU | itemid si WB SKU corresponde al código nativo | product.product.default_code | ProductVariant.sku / InventoryItem.sku |
| Código de barras | upccode | product.product.barcode | ProductVariant.barcodes.nodes\[\].value |
| Relación padre | parent | product.product.product_tmpl_id | ProductVariant.product.id |
| Talla y color | Opciones de matriz personalizadas | attribute_line_ids y product_template_attribute_value_ids | Product.options y ProductVariant.selectedOptions |

Los detalles de destinos, propuestas de campos adicionales y confirmación por cada atributo se desarrollan en Documentación de la estructura de datos. Las rutas son referencias públicas; el uso real en G1522 requiere comprobación por cuenta.

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
