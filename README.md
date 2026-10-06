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
| `homologar_ciclico_g1522.py` | Homologa el Cíclico con Criterios y los validadores, integra productos iguales y separa por marca |
| `Bases_Sheets_G1522/` | Un archivo por marca y contenido (Productos, Revisión, Stock por ubicación), una hoja cada uno, listo para Google Sheets. Montana West y Wrangler juntos; Ariat por División |
| `Informe_homologacion_Ciclico_G1522.md` | Revisión del Cíclico, reglas aplicadas, resultados y pendientes |

## Regenerar la base unificada

```bash
pip install pandas openpyxl xlsxwriter
python3 homologar_ariat_g1522.py
```

## Regenerar las bases por marca para Google Sheets

```bash
pip install pandas openpyxl xlsxwriter python-calamine
python3 homologar_ciclico_g1522.py
```

Usa `Ciclico_1522_investigado.xlsx` y, para Ariat, `Base_Unificada_Ariat_G1522.xlsx`. Reemplaza el contenido de `Bases_Sheets_G1522/`.

