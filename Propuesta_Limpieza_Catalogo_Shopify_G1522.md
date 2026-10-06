# Propuesta de limpieza del catálogo Shopify

Cómo poner los catálogos de Stetson México y Western Brothers dentro del Estándar G1522 y, sobre todo, cómo mantenerlos ahí.

- Empresa: Grupo Quince 22
- Tiendas: `stetsonmexico` (Stetson México) y WB Ecommerce (Western Brothers)
- Fecha: 22 de septiembre de 2026
- Documentos hermanos: `Flujo_Alta_Productos_Shopify_Stetson.md` y `Flujo_Alta_Productos_Shopify_WB.md` (el alta nueva); `Propuesta_Limpieza_Catalogo_Odoo_G1522.md` (la misma limpieza del lado de Odoo)
- Diagnóstico de Stetson medido sobre lo publicado en `stetson.mx` y el admin el 22 de septiembre de 2026. Diagnóstico de WB tomado de la auditoría del 16 al 18 de septiembre (`Control_Datos_Shopify_WB.md`).

---

## 1. Resumen para dirección

**Qué se pide.** Autorizar una limpieza por olas en las dos tiendas: **unas 2 semanas de trabajo efectivo en Stetson** y **unos 3 días en Western Brothers**, más una rutina semanal de 15 minutos que evite volver al punto de partida.

**El problema en una línea.** Las dos tiendas están en puntos muy distintos:

- **Stetson** no tiene el estándar montado: no existen los metacampos, el SKU sigue 38 formatos distintos, las tallas se capturan de siete maneras y hay productos duplicados. Es una limpieza de fondo.
- **Western Brothers** ya tiene el estándar y ya pasó una auditoría (se borraron 12 duplicados y se rehízo el lote Ariat). Le queda el acabado: etiquetas viejas, listas de metacampos por conciliar, tallas pendientes en NetSuite y una medición que confirme que no quedan UPC repetidos.

**Por qué no es cosmético.** En Shopify nada impide que un SKU o un código de barras se repita: Shopify no lo valida. Un UPC en dos productos significa inventario partido entre dos fichas, transferencias recibidas en el producto equivocado y un punto de venta que escanea una pieza y cobra otra. Además, lo que no tiene metacampos del estándar no se puede filtrar ni cruzar con Odoo o NetSuite.

**Qué se gana.**

| Hoy | Después |
|---|---|
| Stetson: el mismo sombrero puede estar dos veces (Skyline 6X) y nada lo detecta | Una pieza, un producto; medición semanal de duplicados |
| Stetson: el estándar no tiene dónde vivir (sin metacampos) | Los 8 metacampos, iguales en las dos tiendas |
| Stetson: tallas como `CH`, `MED`, `s`, y opciones llamadas `Talla MX` en sombreros | Una opción `Talla` con los valores del estándar |
| Etiquetas mezcladas con frases de SEO | Patrón único `No.Estilo, Categoría, Color, Género, Temporada, Marca` en las dos tiendas |
| Cada alta arrastra la duda de "¿esto ya existía?" | El cruce contra la tienda es confiable porque la tienda está limpia |

**Qué pasa si no se hace.** Los flujos de alta dejan limpio todo lo que entre de ahora en adelante. Pero el cruce del alta es tan bueno como el catálogo contra el que cruza: si en la tienda hay un UPC en dos productos, el alta no sabe a cuál agregar la talla nueva. La limpieza es lo que hace que el flujo de alta funcione bien.

**Lo que se pide autorizar** está en la sección 11.

---

## 2. Diagnóstico

### 2.1 Stetson México: el estándar no está montado

Lo publicado en la tienda en línea son **153 productos y 884 variantes**. El admin tiene más: la app Stockyphi marca **440 productos**, así que hay del orden de 290 productos que no están publicados en la tienda en línea (borradores, solo punto de venta o archivados). La primera tarea de la limpieza es medirlos (Ola 0).

**Problema 1. No hay dónde poner el estándar.**

| Hallazgo | Volumen |
|---|---|
| Metacampos `custom.*` del estándar | 0 de 8 existen |
| Vendor con el nombre de la tienda en vez de la marca (`Stetson México`) | 151 de 153 |
| Type en texto libre | 15 valores y 2 vacíos |
| Metacampo `Tipo de producto` (no es del estándar) | 159 productos lo usan |

**Problema 2. Identidad duplicada o incompleta.**

| Hallazgo | Volumen |
|---|---|
| Estilo duplicado: Skyline 6X (`skyline-6x-7240-stetson-r` y `sombrero-skyline-6x-cowboy-stetson-r`) | 2 productos, 18 SKU repetidos |
| Variantes sin SKU | 21, todas en el Skyline duplicado |
| Handles `-copy` / `-copia` (creados con "Duplicar") | 4 |
| Formatos de SKU distintos | 38. El código Stetson (`SFPALC-48400766`) cubre 296 de 884 variantes |
| Variantes sin código de barras | **Por medir.** La ficha revisada (Texana Palacio II 6X) no tiene ninguno en sus 4 tallas |

**Problema 3. Las tallas no tienen estándar.**

| Hallazgo | Volumen |
|---|---|
| Productos con dos o más opciones | 50 (43 sombreros, 4 camisas, 3 cinturones) |
| De esos, con opción `Color` de **un solo valor** (la opción no sirve para nada) | 34 |
| De esos, con varios colores reales | 16 |
| Opción de talla con nombre distinto de `Talla` (`Talla MX`) | 5 |
| Sombreros con tallas fuera de la fracción US (`S`, `M`, `L`, `XL`, `CH`, `MED`, `GDE`) | 5 productos |
| Productos con tallas en minúscula (`s`, `m`, `xl`) | 14 |
| `Unitalla` como valor de opción en vez de `Default Title` | 2 |

**Problema 4. Presentación sin patrón.**

| Hallazgo | Volumen |
|---|---|
| Productos con frases de SEO como etiqueta (`stetson hecho en usa.`) | 59 |
| Productos sin etiquetas | 3 |
| Títulos con `| Stetson®` u otros adornos | 13 |
| Títulos sin la palabra Stetson | 48 |
| Handles con el sufijo `-r` | 83 |
| Productos sin imagen | 0 |
| Descripción vacía o muy corta | 2 |

Del lado bueno: **todos los productos publicados tienen imagen**, casi todos tienen descripción y todos los precios siguen la misma lógica (múltiplos de 50). Lo comercial está atendido; lo que falta es identidad y clasificación. Es el mismo diagnóstico que en Odoo.

### 2.2 Western Brothers: acabado

| Hallazgo | Volumen | Estado |
|---|---|---|
| Grupos de UPC en más de un handle | 14 grupos (28 productos) | Resueltos el 16–18 sep. **Falta volver a medir** |
| Colisiones de captura (Camisa REAL Billie, Bota Sport Western) | 2 | Resueltas |
| Lote Ariat del 15-sep (69 drafts con SKU invertido) | 69 | Borrados; 10 recargados bien |
| Etiquetas con patrón viejo (`A1109003, cat_bandanas`) | Parte del catálogo viejo | Por medir y homologar |
| Lista del metacampo `custom.categoria` vs WB Categoria del ERP | — | Se agregó `Chamarras`; falta la conciliación completa |
| Estilos con talla vacía o en cero en NetSuite | 5 (10063824, A442002902, AR2829400, AR2829650, AR2830200) | Pendiente en el ERP |
| Estilo 10063824: color "Café" (ERP) vs "Distressed Brown" (Shopify) | 1 | Pendiente |
| Productos en el catálogo | 587 (exportación `ProductsWB` del 22-sep) | — |

WB no necesita una limpieza de fondo. Necesita una **medición completa** que confirme que la auditoría dejó el catálogo limpio, y cerrar los pendientes.

---

## 3. Principios de la limpieza

Siete reglas que aplican a las dos tiendas. Si una acción viola una de estas, no se hace.

1. **Primero el destino, luego el dato.** No se llena un metacampo que no existe ni se renombra una talla sin la lista final. En Stetson la Ola 1 (estructura) bloquea a todas las demás.
2. **Primero ver qué depende de lo que se toca.** Antes de cambiar Type, Vendor, etiquetas o handles, se revisa qué colecciones automáticas, filtros y apps dependen de ellos. En Shopify, un cambio de etiqueta puede sacar productos de una colección sin que nadie lo note.
3. **Un método único:** exportar con `ID` y `Variant ID` → corregir en Excel → reimportar con `UPDATE`. Nunca `MERGE` para corregir (si no encuentra el producto, crea uno) y nunca `REPLACE`.
4. **Respaldo antes de cada carga.** La exportación previa, guardada con fecha y nombre de la ola, es el punto de retorno. Sin respaldo no se carga.
5. **Nada con historial se borra: se archiva.** Un producto con ventas o existencias pasa a `Archived` con el SKU y el código de barras prefijados `Z-`, igual que en Odoo. Así libera el código para el producto que se queda y conserva su historial. Solo se borran borradores sin ventas ni existencias (como los 69 drafts del lote Ariat).
6. **Por olas, no por campos.** Se cierra una ola, se mide, y solo entonces se abre la siguiente.
7. **Se empieza por lo que se vende.** Dentro de cada ola: primero lo publicado y con existencias, luego lo publicado sin existencias, al final los borradores.

---

## 4. El método único

Vale para cualquier corrección de más de 10 productos.

1. **Filtrar** el subconjunto de la ola en la exportación de la tienda.
2. **Exportar** con Matrixify, siempre con `ID`, `Handle`, `Variant ID` y los campos a corregir. Guardar la plantilla de exportación para reusarla.
3. **Guardar el export como respaldo** antes de editar.
4. **Corregir** en Excel, contra el estándar (Odoo / NetSuite / lista del proveedor). Nunca a criterio propio.
5. **Quitar del archivo** las columnas que no se corrigen, en particular las de inventario (`Inventory Available: …`): un cero borra existencias y una celda vacía le quita la sucursal a la variante.
6. **Reimportar** con `Command = UPDATE`. `ID` y `Variant ID` no se editan: son lo que hace que Matrixify actualice ese producto y no otro.
7. **Dry run** primero, luego una muestra de 5, luego el resto.
8. **Medir** con el tablero de la sección 8 y cerrar la ola en la bitácora.

Cuatro operaciones delicadas, con su regla:

| Operación | Riesgo | Regla |
|---|---|---|
| Renombrar una opción (`Talla MX` → `Talla`) o cambiar un valor (`CH` → `S`) | Bajo: las variantes se conservan | Por `ID` + `Variant ID`, con `UPDATE` |
| Quitar una opción que sobra (la `Color` de un solo valor) | **Alto:** si hay que recrear variantes, se pierden `Variant ID`, historial por variante y existencias | Producto por producto en el admin, con respaldo. Si Shopify no deja quitarla sin recrear variantes, **se deja como está** y se anota |
| Cambiar un handle | Medio: rompe enlaces y anuncios | Matrixify crea la redirección del handle viejo al nuevo por omisión. Confirmar que la opción esté activa |
| Cambiar Type, Vendor o etiquetas | Medio: saca productos de colecciones | Solo después de la revisión de colecciones de la Ola 0 |

---

## 5. Stetson México: siete olas

Esfuerzos en días de trabajo efectivo de una persona, sin contar esperas del proveedor o de autorizaciones.

### Ola 0 — Medición y dependencias

| | |
|---|---|
| **Alcance** | Todo el catálogo del admin (no solo lo publicado) y todo lo que lee el catálogo |
| **Cómo** | 1) Exportación completa con Matrixify: productos, variantes, códigos de barras, estado, canales, inventario por sucursal, metacampos. 2) Exportación de colecciones con sus condiciones. 3) Revisión del filtro de la tienda (Smart Products Filter). 4) Revisión de la app Stockyphi: qué sincroniza y en qué sentido |
| **Esfuerzo** | 1 día |
| **Riesgo** | Ninguno: solo lectura |
| **Criterio de cierre** | Tablero de la sección 8 con su primera medición; lista de colecciones y filtros con el campo del que dependen (Type, Tag, Vendor); alcance de Stockyphi documentado |
| **Por qué va primero** | Hoy no se sabe cuántas variantes no tienen código de barras ni qué hay en los ~290 productos no publicados. Tampoco se sabe si cambiar el Vendor vacía una colección. Sin esto, cualquier ola es a ciegas |

### Ola 1 — Estructura destino

| | |
|---|---|
| **Alcance** | 8 metacampos del estándar (con las mismas claves y listas que WB); tabla Categoría del estándar → Categoría Shopify; lista final de valores de talla por familia |
| **Cómo** | Configuración → Metacampos y metaobjetos → Productos. Las listas se copian de WB y de la hoja Criterios, con acentos |
| **Esfuerzo** | 0.5 día |
| **Riesgo** | Bajo |
| **Criterio de cierre** | Los 8 metacampos existen con sus listas; la tabla de categorías tiene las 39 del estándar |
| **Bloquea a** | Olas 3, 4 y 6 |

### Ola 2 — Identidad

| | |
|---|---|
| **Alcance** | Skyline 6X duplicado (18 SKU repetidos, 21 variantes sin SKU); 4 handles `-copy/-copia`; cualquier SKU o código de barras en más de un producto que salga de la Ola 0 |
| **Cómo** | Árbol de decisión de la sección 6, caso por caso. Es la única ola que no se resuelve en bloque |
| **Esfuerzo** | 1 día (más lo que aparezca en la Ola 0) |
| **Riesgo** | Medio: se decide sobre productos con ventas y existencias. Se archiva, no se borra |
| **Criterio de cierre** | Cero SKU y cero códigos de barras en más de un producto activo; cero handles con sufijo de duplicado; cero variantes activas sin SKU |

### Ola 3 — Código de barras y No. de Estilo

| | |
|---|---|
| **Alcance** | Variantes sin código de barras (volumen de la Ola 0), y el No. de Estilo en `custom.no_estilo` de todos los productos |
| **Cómo** | Cruce por **SKU Stetson** contra la lista del proveedor y el catálogo de Odoo para traer el UPC. El No. de Estilo sale del mismo cruce; en sombreros se puede proponer como SKU sin los dos últimos dígitos (`SFPALC-484007`), pero se confirma contra el proveedor antes de cargarlo. Carga por `Variant ID` |
| **Esfuerzo** | 2 días, más la espera del proveedor |
| **Riesgo** | Bajo |
| **Criterio de cierre** | Cero variantes publicadas sin código de barras; `custom.no_estilo` lleno en todo lo publicado |
| **Por qué va aquí** | El código de barras es la llave con Odoo, NetSuite y las transferencias. Sin él, el cruce de las olas siguientes y del flujo de alta no tiene de dónde agarrarse |

### Ola 4 — Tallas y opciones

| | |
|---|---|
| **Alcance** | 5 opciones `Talla MX` → `Talla`; 14 productos con tallas en minúscula; 5 sombreros con tallas alfa; 2 `Unitalla` → `Default Title`; 34 productos con una opción `Color` de un solo valor |
| **Cómo** | Renombrar opción y valores por `ID` + `Variant ID` con `UPDATE` (seguro). La opción `Color` que sobra se quita en el admin, producto por producto, solo si Shopify lo permite sin recrear variantes (sección 4). Los sombreros con `S`/`M`/`L` se convierten a fracción solo si el proveedor da la equivalencia; si no, se quedan y se anotan |
| **Esfuerzo** | 2 días |
| **Riesgo** | Medio en la parte de quitar opciones; bajo en lo demás |
| **Criterio de cierre** | Toda opción de talla se llama `Talla`; ningún valor en minúscula ni `CH/MED/GDE`; ningún `Unitalla` como valor |
| **Beneficio visible** | El selector de talla en la tienda y en el punto de venta se ve igual en todos los productos |

### Ola 5 — Clasificación

| | |
|---|---|
| **Alcance** | Los 8 metacampos del estándar (División, Género, Categoría, Temporada, Lifecycle, Composición, Licencia); Vendor = `Stetson` (151); categoría de la taxonomía Shopify |
| **Cómo** | Desde Odoo por código de barras cuando el producto ya está cargado bajo el estándar; si no, propuesta automática por Type y título con el mapa de la hoja Criterios, revisión de una muestra del 10% y carga. Vendor en bloque **después** de confirmar en la Ola 0 que ninguna colección filtra por Vendor |
| **Esfuerzo** | 2 días |
| **Riesgo** | Bajo |
| **Criterio de cierre** | Metacampos llenos al 100% en lo publicado; Vendor = marca; categoría Shopify asignada |

### Ola 6 — Etiquetas, Type, títulos y handles

| | |
|---|---|
| **Alcance** | Etiquetas del estándar en todo; retiro de frases SEO (59 productos); Type según la decisión S3; 13 títulos con `| Stetson®`; títulos sin la marca (48); handles fuera de convención |
| **Cómo** | 1) Agregar las etiquetas del estándar con `Tags Command = MERGE`. 2) Si alguna colección dependía de una etiqueta vieja, pasar la condición de la colección a la etiqueta o al metacampo nuevo. 3) Retirar las frases SEO con `Tags Command = DELETE`. 4) Type, solo si se aprueba S3 y las colecciones ya no dependen del Type viejo. 5) Títulos con `UPDATE`. 6) **Handles solo si hay motivo** (sufijo de duplicado, handle genérico): cambiar un handle que funciona no da valor y arriesga enlaces |
| **Esfuerzo** | 2 días |
| **Riesgo** | Medio: toca lo que usan las colecciones. Por eso va al final |
| **Criterio de cierre** | Todo producto publicado lleva las 6 etiquetas del estándar; cero etiquetas de más de dos palabras; ningún título con adornos |
| **Por qué va al final** | Las etiquetas se construyen con No. de Estilo, Categoría, Color, Género y Temporada. Hacerlas antes es escribirlas dos veces |

### Ola 7 — Borradores y no publicados

| | |
|---|---|
| **Alcance** | Los ~290 productos del admin que no están en la tienda en línea (volumen exacto de la Ola 0) |
| **Cómo** | Clasificar en tres grupos: 1) se van a vender → pasan por las olas 2 a 6 y se publican; 2) solo punto de venta → misma limpieza, sin publicar en línea; 3) basura (borradores de prueba, duplicados sin ventas ni existencias) → se borran |
| **Esfuerzo** | 1 a 2 días |
| **Riesgo** | Bajo si se respeta la regla: nada con ventas o existencias se borra |
| **Criterio de cierre** | Cada producto del admin está en uno de los tres grupos, y el grupo 3 está en cero |

---

## 6. Western Brothers: tres olas

WB ya tiene el estándar montado; su limpieza es de verificación y acabado.

### Ola W1 — Medición completa

| | |
|---|---|
| **Alcance** | Todo el catálogo (587 productos) |
| **Cómo** | Sobre la exportación diaria `ProductsWB` (con el conector "Matrixify WB", Claude puede correrla y medir): UPC en más de un handle; `Variant SKU` distinto de `Variant Barcode`; SKU que sea un No. de Estilo; metacampos vacíos; tallas fuera del estándar; precios que no terminan en 9; handles `marca-<estilo>`; etiquetas con patrón viejo |
| **Esfuerzo** | 0.5 día |
| **Criterio de cierre** | Tablero de la sección 8 medido. Si aparece algo en identidad (UPC repetido, SKU invertido), se resuelve con el árbol de la sección 7 antes de la Ola W2 |

### Ola W2 — Listas y pendientes del ERP

| | |
|---|---|
| **Alcance** | Conciliación completa de la lista de `custom.categoria` contra WB Categoria (y de División, Género, Temporada, Lifecycle); los 5 estilos con talla vacía en NetSuite; color del estilo 10063824 |
| **Cómo** | Comparar valor por valor, con acentos. Las tallas se corrigen en NetSuite contra el Internal ID y después se dan de alta con el flujo |
| **Esfuerzo** | 1 día, más la espera de NetSuite |
| **Criterio de cierre** | Las listas de Shopify son idénticas a las del ERP; los 5 estilos dados de alta o con fecha comprometida |

### Ola W3 — Etiquetas del catálogo viejo

| | |
|---|---|
| **Alcance** | Productos con el patrón viejo (`A1109003, cat_bandanas`) |
| **Cómo** | Igual que la Ola 6 de Stetson: primero revisar colecciones, luego agregar el patrón nuevo con `MERGE`, pasar las condiciones de colección que dependan de etiquetas viejas y al final retirarlas con `DELETE` |
| **Esfuerzo** | 1 día |
| **Criterio de cierre** | Todo producto lleva el patrón `No.Estilo, Categoria, Color, Genero, Temporada, Marca`; cero etiquetas `cat_*` |

---

## 7. Árbol de decisión para duplicados

El mismo para las dos tiendas. Se resuelve grupo por grupo:

1. **¿Dos productos comparten un código de barras?**
   → Duplicado real si son el mismo estilo. Si son estilos distintos, es **colisión de captura**: se corrige el código de barras equivocado (casos Camisa REAL Billie y Bota Sport Western en WB).

2. **¿Comparten SKU pero tienen códigos de barras distintos?**
   → No es duplicado: un SKU mal capturado. Se corrige el SKU.

3. **En un duplicado real, ¿cuál se conserva?** En este orden:
   1. El que tiene la estructura correcta (opción `Talla`, SKU y código de barras en todas las variantes, handle con convención).
   2. El que tiene existencias.
   3. El que tiene ventas.
   4. El más antiguo.

   En Skyline 6X: `sombrero-skyline-6x-cowboy-stetson-r` tiene 21 variantes sin SKU y una opción `Perfil` de más, así que en principio se conserva `skyline-6x-7240-stetson-r`. Se confirma con las existencias y las ventas de la Ola 0.

4. **Si al que se conserva le faltan tallas que el otro sí tiene**, se agregan como variantes nuevas con `MERGE`, con su SKU y código de barras, **después** de liberar esos códigos (paso 6).

5. **Antes de retirar el otro, se mueven sus existencias** al que se conserva, con un ajuste o transferencia documentado por sucursal. Archivar o borrar un producto con existencias esconde el inventario, no lo mueve.

6. **El que se retira:**
   - Con ventas o historial: `Status = Archived`, y SKU y código de barras prefijados `Z-` (libera los códigos para el que se queda y deja el registro identificable).
   - Sin ventas ni existencias, y es un borrador: se borra.

7. **Redirección** del handle retirado al que se conserva (Contenido → Menús → Redirecciones de URL, o con Matrixify).

8. **Registro** en la bitácora de la ola: los dos `ID`, cuál se conservó, por qué, y el movimiento de inventario.

---

## 8. Tablero de salud del catálogo

Las mismas métricas para las dos tiendas, medidas sobre una exportación de Matrixify. Se miden al cerrar cada ola y luego cada semana.

| # | Métrica | Cómo se mide | Stetson hoy | WB hoy | Meta |
|---|---|---|---|---|---|
| M1 | Códigos de barras en más de un producto | Agrupar por `Variant Barcode`, contar handles distintos > 1 | Por medir | 0 tras la auditoría (por confirmar) | 0 |
| M2 | SKU en más de un producto | Igual, por `Variant SKU` | 18 (Skyline) | Por confirmar | 0 |
| M3 | Variantes publicadas sin código de barras | `Variant Barcode` vacío + producto `Active` | Por medir | Por medir | 0 |
| M4 | Variantes sin SKU | `Variant SKU` vacío | 21 | Por medir | 0 |
| M5 | WB: SKU distinto del código de barras | `Variant SKU` ≠ `Variant Barcode` | No aplica | Por medir | 0 |
| M6 | Productos sin `custom.no_estilo` | Metacampo vacío | 153 (no existe) | Por medir | 0 |
| M7 | Opciones de talla fuera del estándar | `Option Name` ≠ `Talla` / `Title`, o valor fuera de la lista de la familia | ~55 productos | Por medir | 0 |
| M8 | Productos sin el patrón de etiquetas | Faltan una o más de las 6 etiquetas del estándar | ~153 | Por medir | 0 |
| M9 | Handles con sufijo de duplicado | Handle termina en `-copy`, `-copia`, `-1`, `-2` | 4 | Por medir | 0 |
| M10 | Precio fuera de regla | Stetson: no múltiplo de 50; WB: no termina en 9 | 0 | Por medir | 0 |

M1, M2 y M5 son las de identidad: si alguna sale mayor a cero, se atiende **esa semana**, antes de la siguiente alta.

Una sola cifra para dirección, por tienda: **% de productos publicados que cumplen el estándar completo** (sin duplicados, con código de barras, con los 8 metacampos, talla estándar y patrón de etiquetas). Hoy en Stetson es 0%, porque los metacampos no existen. La meta al cerrar la Ola 6 es 100% sobre lo publicado.

---

## 9. Rutina de mantenimiento

### 9.1 Los cuatro candados

| # | Candado | Qué hace | Cómo |
|---|---|---|---|
| L1 | **Una sola puerta de entrada** | Ningún producto se crea fuera del flujo de alta. Nadie usa "Duplicar", ni el importador tradicional, ni crea productos desde otra app | Acuerdo operativo + revisión semanal de M9 y de productos creados en la semana sin registro en bitácora |
| L2 | **Validador obligatorio** | Ningún lote se carga sin pasar las 16 validaciones del flujo, incluida la comparación contra la tienda | El semáforo se anexa a la bitácora del lote. Sin ese registro, el lote no está cerrado |
| L3 | **Listas cerradas con dueño** | Los valores de `custom.categoria` y demás listas solo los agrega el responsable de datos | Permisos del admin: solo el responsable edita definiciones de metacampos. El valor fuera de lista rebota en la carga, que es lo que se busca |
| L4 | **Medición semanal de identidad** | M1, M2 y M5 cada semana | Exportación programada en Matrixify (ya existe en WB: `ProductsWB` diaria; crear la equivalente en Stetson) y un cruce de 15 minutos, o que Claude la corra con el conector |

Hay una diferencia con Odoo: allá el candado más barato era hacer obligatorio el No. de Estilo en la ficha. Shopify no permite hacer obligatorio un metacampo al crear un producto. Por eso aquí el peso lo cargan L1 y L4: no se puede impedir el error, así que hay que encontrarlo rápido.

### 9.2 Calendario de control

| Cuándo | Qué | Quién |
|---|---|---|
| Al cerrar cada lote de alta | Checklist posterior del flujo y bitácora | Quien carga |
| Semanal, 15 minutos | M1, M2, M5, M9 en las dos tiendas | Responsable de datos |
| Mensual, 1 hora | Tablero completo (M1 a M10), comparado con el mes anterior | Responsable de datos |
| Al arranque de cada temporada | Temporada y Lifecycle de los estilos nuevos; revisión de listas contra el estándar | Responsable de datos |
| Semestral | Listas de Shopify (las dos tiendas) contra la hoja Criterios, Odoo y NetSuite, en los dos sentidos | Responsable de datos |

### 9.3 La regla que sostiene todo

**Un hecho, un solo lugar.** El dato de catálogo vive en el estándar (NetSuite / Odoo). Shopify lo publica, no lo inventa. Si un dato está mal en la tienda, se corrige en el origen y se vuelve a cargar; si se corrige solo en Shopify, en la siguiente carga vuelve el error.

---

## 10. Riesgos del proyecto

| Riesgo | Probabilidad | Cómo se controla |
|---|---|---|
| Sacar productos de colecciones al cambiar etiquetas, Type o Vendor | **Alta** si no se revisa | Ola 0 (dependencias) antes que nada; etiquetas nuevas con `MERGE` antes de borrar las viejas |
| Perder variantes, historial y existencias al quitar una opción | Media | Solo producto por producto, con respaldo; si exige recrear variantes, no se hace |
| Esconder inventario al archivar un duplicado | Media | Paso 5 del árbol: mover existencias antes de archivar |
| Borrar existencias o quitar sucursales en una actualización | Media | Columnas de inventario fuera de todo archivo de limpieza |
| Crear productos nuevos por error al corregir | Baja si se sigue el método | `UPDATE`, nunca `MERGE`, con `ID` y `Variant ID` sin editar |
| Una app (Stockyphi) sobrescribe lo corregido | Por confirmar | Ola 0: documentar qué sincroniza; si escribe catálogo, pausarla durante las cargas o corregir en su origen |
| Romper enlaces al cambiar handles | Baja | Redirección automática de Matrixify; handles solo se cambian con motivo |
| Que la operación vuelva a ensuciar | **Alta si no hay candados** | Los cuatro candados de 9.1, en particular L1 y L4 |
| Esperas del proveedor para los códigos de barras | Media | La Ola 3 identifica temprano lo que depende del proveedor y avanza en paralelo |

---

## 11. Lo que se pide autorizar

### 11.1 Decisiones

| # | Decisión | Recomendación | Bloquea |
|---|---|---|---|
| L-D1 | Duplicados con historial se **archivan** con prefijo `Z-` (no se borran), en las dos tiendas, igual que en Odoo | Aprobar. Unifica el criterio de los tres sistemas | Ola 2 / W1 |
| L-D2 | Quitar la opción `Color` de un solo valor en los 34 productos de Stetson | Aprobar solo donde Shopify lo permita sin recrear variantes | Ola 4 |
| L-D3 | Retirar las frases de SEO de las etiquetas (59 productos en Stetson) | Aprobar, después de revisar colecciones | Ola 6 |
| L-D4 | Vendor `Stetson México` → `Stetson` | Aprobar, después de revisar colecciones | Ola 5 |
| L-D5 | Crear en Stetson la exportación diaria equivalente a `ProductsWB` | Aprobar. Es la base de L4 | Rutina |
| L-D6 | Conectar Matrixify de Stetson a Claude, como ya está el de WB | Recomendado. Permite medir, cruzar y preparar archivos sin descargas manuales | Acelera todas las olas |

Además siguen abiertas las decisiones de los flujos de alta que afectan la limpieza: S1 (qué va en el SKU de Stetson), S2 (metacampos), S3 (Type) y S4 (regla de precio).

### 11.2 Calendario propuesto

| Semana | Stetson México | Western Brothers | Entregable de cierre |
|---|---|---|---|
| 1 | Ola 0 (medición y dependencias), Ola 1 (estructura), Ola 2 (identidad) | Ola W1 (medición completa) | Tablero de las dos tiendas medido; M1 y M2 en cero en las dos |
| 2 | Ola 3 (código de barras y No. de Estilo), Ola 4 (tallas y opciones) | Ola W2 (listas y ERP), Ola W3 (etiquetas) | Stetson: M3, M4, M6, M7 en cero. WB: tablero completo en cero |
| 3 | Ola 5 (clasificación), Ola 6 (etiquetas, Type, títulos), Ola 7 (no publicados) | Rutina semanal | Stetson: M8 en cero; % de cumplimiento del estándar al 100% sobre lo publicado |
| Continuo | Rutina de mantenimiento en las dos tiendas | | Tablero mensual |

Nota sobre el orden: **en Stetson la Ola 3 va antes que la 5 a propósito.** La clasificación se trae de Odoo cruzando por código de barras; si el código de barras no está, no hay por dónde cruzar. Es la misma lógica que en la limpieza de Odoo, donde el código de barras va antes que el No. de Estilo.

---

## Anexo — Relación con la limpieza de Odoo

Las dos limpiezas se ayudan entre sí y conviene coordinarlas:

| En Odoo | Ayuda a Shopify en |
|---|---|
| Ola 2 (códigos de barras faltantes) | Stetson Ola 3: el UPC que se recupere en Odoo es el que se carga en Shopify |
| Ola 3 (No. de Estilo y Marca) | Stetson Ola 3 y Ola 5: el No. de Estilo y la clasificación se traen de Odoo por código de barras |
| Ola 4 (clasificación) | Stetson Ola 5: División, Género y Categoría ya normalizadas |
| Hoja Criterios y listas cerradas | Listas de los metacampos en las dos tiendas |

Si las dos corren al mismo tiempo, el orden práctico es: códigos de barras en Odoo → códigos de barras en Stetson → clasificación en Odoo → clasificación en Stetson.
