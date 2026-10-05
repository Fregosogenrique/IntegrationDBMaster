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

## Regenerar la base unificada

```bash
pip install pandas openpyxl xlsxwriter
python3 homologar_ariat_g1522.py
```
