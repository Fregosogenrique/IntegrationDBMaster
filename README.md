# Normalizacion
Normalizacion de datos y homologacion

## Contenido

| Archivo | Descripción |
|----|----|
| `Anatomia_productos_atributos_G1522.md` / `.docx` | Estándar G1522: estructura padre y variante, y reglas de captura (Criterios) |
| `Estructura_datos_validaciones_G1522.md` / `.docx` | Diccionario de los 25 atributos, mapeo a plataformas y validaciones |
| `Ariat.xlsx` | Catálogo maestro Ariat (origen) |
| `Products.csv` | Exportación de la tienda Shopify Ariat (origen) |
| `homologar_ariat_g1522.py` | Script que empata, normaliza y valida las dos bases |
| `Base_Unificada_Ariat_G1522.xlsx` | Base única resultante (hojas Productos, Revisión y Resumen) |
| `Informe_homologacion_Ariat_G1522.md` | Reglas aplicadas, resultados y pendientes |
| `Ciclico_1522_investigado.xlsx` | Cíclico integrado: catálogo NetSuite con Shopify Stetson, Shopify WB, Odoo, stock y escaneos (origen) |
| `homologar_ciclico_g1522.py` | Homologa el Cíclico con Criterios y los validadores, integra productos iguales y genera un Cíclico por marca |
| `Bases_Sheets_G1522/<Marca>/Ciclico_1522_<Marca>.xlsx` | Un Cíclico por marca para Google Sheets, en su carpeta, con el mismo formato que `Bases_Sheets_G1522/Stetson/Ciclico_1522_Stetson.xlsx`: las 12 hojas, columnas, fórmulas de Sheets, listas, formatos y tablas que usan los scripts, más las hojas «Inventario» y «KPIs Inventario» con el inventario actual. Montana West y Wrangler en un solo archivo |
| `Catalogo_Estandar_Inventario_NetSuite_2026-10-06.xlsx` | Catálogo e inventario de NetSuite al 06/10/2026 (origen del inventario actual) |
| `inventario_g1522.py` | Homologa el inventario de NetSuite, Shopify Ariat, plataformas y escaneos en cada Cíclico por marca |
| `investigar_web_g1522.py` | Consulta las tiendas y sitios oficiales de cada marca y traduce lo publicado a los valores de Criterios |
| `Investigacion_web_G1522.csv` | Datos encontrados en línea, con llave, campo, valor, URL y evidencia; el homologador solo los usa en campos vacíos |
| `Informe_homologacion_Ciclico_G1522.md` | Revisión del Cíclico, reglas aplicadas, resultados y pendientes |

## Regenerar la base unificada

```bash
pip install pandas openpyxl xlsxwriter
python3 homologar_ariat_g1522.py
```

## Regenerar los Cíclicos por marca

```bash
pip install pandas openpyxl xlsxwriter python-calamine
python3 investigar_web_g1522.py      # opcional: actualiza Investigacion_web_G1522.csv
python3 homologar_ciclico_g1522.py   # o solo algunas marcas: python3 homologar_ciclico_g1522.py Stetson Roper
```

Usa `Ciclico_1522_investigado.xlsx`, `Catalogo_Estandar_Inventario_NetSuite_2026-10-06.xlsx` y `Products.csv` (inventario), `Base_Unificada_Ariat_G1522.xlsx` (evidencia de la tienda Ariat) y `Bases_Sheets_G1522/Stetson/Ciclico_1522_Stetson.xlsx` como plantilla de formato. Las correcciones hechas a mano en los atributos de cualquier `Bases_Sheets_G1522/<Marca>/Ciclico_1522_<Marca>.xlsx` y sus escaneos se conservan al regenerar. Los archivos se trabajan en Google Sheets: las fórmulas de Escaneo Diario, Productos_Resumen, Stock por Ubicación y las Bodegas son de Sheets.
