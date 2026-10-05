"""Homologación de la base de productos Ariat bajo el estándar G1522.

Empata el catálogo maestro (Ariat.xlsx) con la exportación de la tienda
Shopify de Ariat (Products.csv) y produce una base única que respeta las
reglas de Anatomia_productos_atributos_G1522.md y
Estructura_datos_validaciones_G1522.md.

Secuencia (sección «Secuencia de validación y carga»):
  1. Preparar   - leer ambos orígenes sin alterarlos, identificadores como texto.
  2. Empatar    - llave Código de barras (variante); respaldo: SKU de Shopify
                  cuando contiene el código de barras.
  3. Normalizar - aplicar Criterios: textos sustitutos a vacío, homologación
                  de tallas, colores, división por categoría, unidad, etc.
  4. Completar  - llenar solo campos vacíos del maestro con evidencia de
                  Shopify; el maestro es la autoridad y nunca se sobrescribe.
  5. Validar    - controles internos (llaves, listas cerradas, coherencias).
  6. Resolver   - todo cambio, conflicto o duda queda en la hoja «Revisión».

Uso:  python3 homologar_ariat_g1522.py
Salida: Base_Unificada_Ariat_G1522.xlsx (hojas Productos, Revisión, Resumen).
"""

import html
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
MAESTRO = BASE / "Ariat.xlsx"
SHOPIFY = BASE / "Products.csv"
SALIDA = BASE / "Base_Unificada_Ariat_G1522.xlsx"

# --------------------------------------------------------------------------
# Criterios (Anatomia_productos_atributos_G1522.md)
# --------------------------------------------------------------------------

ATRIBUTOS = [
    "Código de barras", "Identificador interno", "Marca principal", "WB N.º de estilo",
    "WB SKU", "WB Talla", "WB Talla de EE. UU.", "WB Marca", "WB Descripcion",
    "WB División", "WB Categoría", "WB Género", "WB Licencia", "WB Temporada",
    "WB Ciclo de vida", "WB Color", "WB Fit", "WB Silueta", "WB Composición",
    "WB Descripción larga", "WB País de origen", "Unidad", "SAT Clave de producto",
    "Enlace de imagen", "Precio de compra", "Precio de venta",
]

DIVISIONES = {"Accesorios", "Ropa", "Denim", "Calzado"}
GENEROS = {"Hombre", "Mujer", "Niño", "Niña", "Unisex"}
TEMPORADAS = {"SS26", "FW26", "SS27", "FW27", "SS28", "FW28"}
CICLOS = {"Seasonal", "Core"}
UNIDADES = {"PZS", "PRS"}
MARCAS = {
    "Roper", "Denver", "Ariat", "Wrangler", "Stetson", "Montana West", "Tru Western",
    "Ranch & Corral", "Jony Lama", "Justin boots", "Yellowstone", "Generico", "CAPSLAB",
    "Happy Socks", "REFLO", "Willow Lane",
}
MARCAS_PRINCIPALES = MARCAS | {"Multimarca"}

CATEGORIA_DIVISION = {
    "Bandanas": "Accesorios", "Bolsos": "Accesorios", "Botas": "Calzado",
    "Bufandas": "Accesorios", "Calcetines": "Ropa", "Camisas": "Ropa",
    "Carteras": "Accesorios", "Chalecos": "Ropa", "Chamarras": "Ropa",
    "Cinturones": "Accesorios", "Cobijas": "Accesorios", "Cuchillos": "Accesorios",
    "Cuidado de Botas": "Accesorios", "Cuidado de Sombreros": "Accesorios",
    "Equipaje": "Accesorios", "Estuches": "Accesorios", "Faldas": "Ropa",
    "Fragancias": "Accesorios", "Gorras": "Accesorios", "Hebillas": "Accesorios",
    "Jeans": "Denim", "Joyeria": "Accesorios", "Jumpsuits": "Ropa", "Libros": "Accesorios",
    "Llaveros": "Accesorios", "Mascotas": "Accesorios", "Mochilas": "Accesorios",
    "Pantalones": "Ropa", "Pantuflas": "Calzado", "Pijamas": "Ropa", "Playeras": "Ropa",
    "Plumas para sombrero": "Accesorios", "Shorts": "Ropa", "Sombreros": "Accesorios",
    "Sudaderas": "Ropa", "Sueteres": "Ropa", "Tenis": "Calzado", "Vestidos": "Ropa",
    "Zapatos": "Calzado",
}
CALZADO_PRS = {"Botas", "Zapatos", "Tenis", "Pantuflas"}
FAMILIA_TALLA_UNICA = {
    c for c in CATEGORIA_DIVISION
    if c in {"Bandanas", "Bolsos", "Bufandas", "Carteras", "Cobijas", "Cuchillos",
             "Equipaje", "Estuches", "Gorras", "Hebillas", "Joyeria", "Libros",
             "Llaveros", "Mochilas", "Plumas para sombrero"}
}

# Tabla «2. Palabra clave → Categoría»: se aplica la primera coincidencia en este orden.
PALABRAS_CLAVE = [
    ("Cuidado de Botas", "Cuidado de Botas"), ("Cuidado de Sombreros", "Cuidado de Sombreros"),
    ("Plumas para sombrero", "Plumas para sombrero"), ("Gorra", "Gorras"),
    ("Sombrero", "Sombreros"), ("Texana", "Sombreros"), ("Bandana", "Bandanas"),
    ("Bolso", "Bolsos"), ("Bufanda", "Bufandas"), ("Cartera", "Carteras"),
    ("Clip para billetes", "Carteras"), ("Cinturón", "Cinturones"), ("Cobija", "Cobijas"),
    ("Cuchillo", "Cuchillos"), ("Equipaje", "Equipaje"), ("Estuche", "Estuches"),
    ("Fragancia", "Fragancias"), ("Hebilla", "Hebillas"), ("Joyería", "Joyeria"),
    ("Llavero", "Llaveros"), ("Libro", "Libros"), ("Mochila", "Mochilas"),
    ("Mascota", "Mascotas"), ("Jean", "Jeans"), ("Bota", "Botas"), ("Zapato", "Zapatos"),
    ("Tenis", "Tenis"), ("Pantufla", "Pantuflas"), ("Calcet", "Calcetines"),
    ("Camisa", "Camisas"), ("Sobrecamisa", "Camisas"), ("Chaleco", "Chalecos"),
    ("Chamarra", "Chamarras"), ("Falda", "Faldas"), ("Jumpsuit", "Jumpsuits"),
    ("Pantalón", "Pantalones"), ("Pijama", "Pijamas"), ("Playera", "Playeras"),
    ("Short", "Shorts"), ("Sudadera", "Sudaderas"), ("Suéter", "Sueteres"),
    ("Sueter", "Sueteres"), ("Vestido", "Vestidos"),
]

COLORES = {
    "Rojo": ["Red", "Vino", "Escarlata", "Granate", "Burgundy"],
    "Azul": ["Navy", "Azul marino", "Turquesa", "Indigo", "Blue"],
    "Amarillo": ["Mostaza", "Yellow"],
    "Verde": ["Olivo", "Olive", "Green"],
    "Naranja": ["Orange"],
    "Morado": ["Púrpura", "Purple", "Lila"],
    "Rosa": ["Pink"],
    "Negro": ["Black", "Negra"],
    "Blanco": ["White", "Hueso"],
    "Gris": ["Grey", "Gray", "Carbón", "Charcoal"],
    "Beige": ["Crema", "Arena", "Khaki", "Caqui", "Sand"],
    "Cafe": ["Café", "Brown", "Cognac", "Coñac", "Chocolate", "Tabaco", "Taupe",
             "Arcilla", "Terracota", "Camel", "Miel", "Marrón"],
}
# «Mezclilla», «Denim» y «Tan» se excluyen de la inferencia por descripción:
# en los nombres describen la tela o son palabras comunes del español.
COLORES_VALIDOS = set(COLORES) | {"Varios"}

FIT_VALIDOS = {"Regular", "Relajado", "Slim", "Clásico", "Moderno", "Recto", "Bootcut"}
SILUETA_SOMBRERO = {"Copa Cattleman", "Copa Rancher", "Copa Pinch Front", "Copa Gus",
                    "Copa Teardrop", "Copa Open Road", "Copa Brick"}
SILUETA_CALZADO = {"Punta Redonda Ancha", "Punta Cuadrada Ancha", "Punta Redonda",
                   "Punta Cuadrada", "Punta Ovalada", "Punta Snip", "Horma Alexia",
                   "Horma Agatha"}
SILUETA_JEANS = {"Recto", "Bootcut", "Skinny", "Tapered", "Trouser"}

# Paso 4: homologación de tallas.
TALLA_MX = {"CH": "S", "MED": "M", "GDE": "L", "UNI": "Talla única", "2XL": "XXL",
            "3XL": "XXXL"}
TALLA_US = {"OS": "One Size", "UNI": "One Size", "2XL": "XXL", "3XL": "XXXL"}
TALLAS_ALFA = ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"]

TEXTOS_SUSTITUTOS = {"No Aplica", "No aplica", "N/A", "NA", "n/a", "-", "--", ".",
                     "NULL", "null", "None", "Sin dato", "FALTA"}

# Shopify custom.corte → Fit homologado (solo equivalencias directas).
CORTE_A_FIT = {"Recto": "Recto", "Slim": "Slim", "Clásico": "Clásico", "Clasico": "Clásico",
               "Moderno": "Moderno", "Bota": "Bootcut", "Corte Bota": "Bootcut"}
TEMPORADA_SHOPIFY = {"Spring 2026": "SS26", "Fall 2026": "FW26", "Spring 2027": "SS27",
                     "Fall 2027": "FW27", "Spring 2028": "SS28", "Fall 2028": "FW28"}
PAISES = {"MX": "México", "US": "Estados Unidos", "CN": "China", "VN": "Vietnam",
          "IN": "India", "BD": "Bangladés", "KH": "Camboya", "PK": "Pakistán"}
MATERIALES = {
    "algodon": "Algodón", "cotton": "Algodón", "poliester": "Poliéster",
    "polyester": "Poliéster", "spandex": "Elastano", "elastano": "Elastano",
    "pu spandex": "Elastano", "pu": "Poliuretano", "poliuretano elastano": "Elastano",
    "elastano de poliuretano": "Elastano", "nailon": "Nylon", "nylon": "Nylon",
    "rayon": "Rayón", "viscosa": "Viscosa", "lana": "Lana", "piel": "Piel",
    "modal": "Modal", "lyocell": "Lyocell", "tencel": "Tencel", "acrilico": "Acrílico",
}


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------

def sin_acentos(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn").lower()


def patron_palabra(palabra, fin=r"\b"):
    return re.compile(r"\b" + re.escape(sin_acentos(palabra)) + fin)


# Palabra clave completa o en plural; «Calcet» se usa como raíz (Calcetín, Calcetas).
PATRONES_CATEGORIA = [(patron_palabra(k, "" if k == "Calcet" else r"(?:s|es)?\b"), c)
                      for k, c in PALABRAS_CLAVE]
# Frases que contienen una palabra clave sin referirse a la categoría.
FRASES_NEUTRAS = re.compile(r"\bcorte (?:de )?bota\b")
PATRONES_COLOR = [(patron_palabra(s), base) for base, sin in COLORES.items()
                  for s in [base] + sin]
PATRONES_GENERO = [(patron_palabra(k), g) for k, g in [
    ("Dama", "Mujer"), ("Mujer", "Mujer"), ("Caballero", "Hombre"), ("Hombre", "Hombre"),
    ("Niño", "Niño"), ("Niña", "Niña")]]


def categorias_por_palabra(texto):
    """Categorías cuyas palabras clave aparecen, en el orden de la tabla."""
    t = FRASES_NEUTRAS.sub(" ", sin_acentos(texto))
    encontradas = []
    for patron, categoria in PATRONES_CATEGORIA:
        if patron.search(t) and categoria not in encontradas:
            encontradas.append(categoria)
    return encontradas


def colores_en(texto):
    t = sin_acentos(texto)
    return {base for patron, base in PATRONES_COLOR if patron.search(t)}


def generos_en(texto):
    t = sin_acentos(texto)
    return {g for patron, g in PATRONES_GENERO if patron.search(t)}


def digito_control_gtin(codigo):
    """True si el último dígito es el dígito de control GTIN (UPC/EAN)."""
    cuerpo, control = codigo[:-1], int(codigo[-1])
    suma = sum(int(d) * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(cuerpo)))
    return (10 - suma % 10) % 10 == control


def html_a_texto(valor):
    texto = re.sub(r"<br\s*/?>|</p>|</li>|</div>", "\n", valor, flags=re.I)
    texto = html.unescape(re.sub(r"<[^>]+>", " ", texto))
    lineas = (" ".join(l.split()) for l in texto.splitlines())
    return "\n".join(l for l in lineas if l)


def rich_text_a_texto(valor):
    partes = []

    def recorrer(nodo):
        if isinstance(nodo, dict):
            if nodo.get("type") == "text":
                partes.append(nodo.get("value", ""))
            for hijo in nodo.get("children", []):
                recorrer(hijo)
            if nodo.get("type") in ("list-item", "paragraph"):
                partes.append(" ")

    try:
        recorrer(json.loads(valor))
    except (ValueError, TypeError):
        return ""
    return " ".join("".join(partes).split())


PAR_MATERIAL = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*([a-z ]+?)(?=\s*(?:[,/;.]|\by\b|\d|$))")


def normalizar_composicion(texto):
    """Convierte «97% poliéster, 3% spandex» al formato del maestro.

    Solo acepta textos formados exclusivamente por pares porcentaje-material
    reconocidos que sumen 100 %; cualquier otro caso devuelve "" para revisión.
    """
    t = sin_acentos(texto).replace("producto importado", " ")
    pares = PAR_MATERIAL.findall(t)
    resto = re.sub(r"\by\b|[\s,/;.]", "", PAR_MATERIAL.sub("", t))
    if not pares or resto:
        return ""
    componentes = {}
    for porcentaje, material in pares:
        nombre = MATERIALES.get(material.strip())
        if not nombre:
            return ""
        componentes[nombre] = componentes.get(nombre, 0) + float(porcentaje)
    if abs(sum(componentes.values()) - 100) > 0.01:
        return ""
    orden = sorted(componentes.items(), key=lambda kv: (kv[1], kv[0]))
    return ", ".join(f"{p:g}% {m}" for m, p in orden)


def numero(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


class Revision:
    """Bitácora de la hoja Revisión: campo, valor origen, corrección y evidencia."""

    COLUMNAS = ["Código de barras", "WB SKU", "Identificador interno", "Campo",
                "Valor origen", "Valor final", "Tipo", "Incidencia / acción",
                "Evidencia", "Responsable de validación"]

    def __init__(self):
        self.filas = []

    def add(self, fila, campo, origen, final, tipo, accion, evidencia=""):
        self.filas.append([fila["Código de barras"], fila["WB SKU"],
                           fila["Identificador interno"], campo, origen, final, tipo,
                           accion, evidencia, ""])

    def tabla(self):
        return pd.DataFrame(self.filas, columns=self.COLUMNAS)


# --------------------------------------------------------------------------
# 1. Preparar
# --------------------------------------------------------------------------

def leer_maestro():
    df = pd.read_excel(MAESTRO, dtype=str).fillna("")
    for c in ATRIBUTOS:
        df[c] = df[c].str.strip()
    df["Origen de la fusión"] = "Solo maestro"
    return df


def leer_shopify():
    """Una fila por variante con los datos del producto padre propagados."""
    sp = pd.read_csv(SHOPIFY, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    mf = "Metafield: custom.{} [{}]".format
    columnas_padre = {
        "Title": "Title", "Body HTML": "Body HTML", "Vendor": "Vendor", "Type": "Type",
        "Tags": "Tags", "Status": "Status", "Handle": "Handle",
        mf("season", "single_line_text_field"): "season",
        mf("corte", "single_line_text_field"): "corte",
        mf("materiales", "rich_text_field"): "materiales",
        mf("sku", "single_line_text_field"): "estilo",
    }
    padres = sp.drop_duplicates("ID").set_index("ID")[list(columnas_padre)]
    padres = padres.rename(columns=columnas_padre)
    imagenes = sp[sp["Image Src"] != ""].drop_duplicates("ID").set_index("ID")["Image Src"]
    var = sp[sp["Variant ID"] != ""][[
        "ID", "Variant ID", "Variant SKU", "Variant Barcodes", "Option1 Name",
        "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
        "Variant Price", "Variant Compare At Price", "Variant Cost",
        "Variant Country of Origin", "Variant Inventory Qty"]].copy()
    var = var.join(padres, on="ID")
    var["Image Src"] = var["ID"].map(imagenes).fillna("")
    var["Opciones"] = var.apply(opciones_texto, axis=1)
    return var.reset_index(drop=True)


def opciones_texto(r):
    partes = []
    for i in (1, 2, 3):
        nombre, valor = r[f"Option{i} Name"], r[f"Option{i} Value"]
        if valor and valor not in ("#VALUE!", "Default Title"):
            partes.append(f"{nombre}: {valor}")
    return " / ".join(partes)


# --------------------------------------------------------------------------
# 2. Empatar
# --------------------------------------------------------------------------

def empatar(maestro, shopify, rev):
    codigos = set(maestro.loc[maestro["Código de barras"] != "", "Código de barras"])
    llave = shopify["Variant Barcodes"].where(shopify["Variant Barcodes"].isin(codigos), "")
    por_sku = (llave == "") & shopify["Variant SKU"].isin(codigos)
    llave[por_sku] = shopify.loc[por_sku, "Variant SKU"]
    shopify["Llave"] = llave
    shopify["Empate"] = ""
    shopify.loc[llave != "", "Empate"] = "Código de barras"
    shopify.loc[por_sku, "Empate"] = "SKU Shopify = código de barras"

    # Variante de Shopify duplicada sobre el mismo código: se usa la primera.
    duplicadas = shopify[(llave != "") & llave.duplicated(keep="first")]
    for _, s in duplicadas.iterrows():
        rev.add({"Código de barras": s["Llave"], "WB SKU": s["Variant SKU"],
                 "Identificador interno": ""}, "Código de barras", s["Llave"], s["Llave"],
                "Conflicto Shopify", "Código de barras repetido en dos variantes de Shopify; "
                "se empató solo la primera", f"Shopify variante {s['Variant ID']}")
    unicas = shopify[(llave != "") & ~llave.duplicated(keep="first")].set_index("Llave")

    sh = {
        "Shopify ID producto": "ID", "Shopify ID variante": "Variant ID",
        "Shopify Handle": "Handle", "Shopify Estatus": "Status",
        "Shopify Título": "Title", "Shopify Opciones": "Opciones",
        "Shopify SKU": "Variant SKU", "Shopify Código de barras": "Variant Barcodes",
        "Shopify Precio": "Variant Price",
        "Shopify Precio comparación": "Variant Compare At Price",
        "Shopify Inventario": "Variant Inventory Qty", "Shopify Empate": "Empate",
    }
    for destino, origen in sh.items():
        maestro[destino] = maestro["Código de barras"].map(unicas[origen]).fillna("")
    empatadas = maestro["Shopify ID variante"] != ""
    maestro.loc[empatadas, "Origen de la fusión"] = "Maestro + Shopify"

    # SKU y código de barras de Shopify que apuntan a variantes distintas.
    for i, r in maestro[empatadas].iterrows():
        s_sku, s_cb = r["Shopify SKU"], r["Shopify Código de barras"]
        if s_sku and s_cb and s_sku != s_cb and s_sku in codigos:
            rev.add(r, "WB SKU", s_sku, r["WB SKU"], "Conflicto Shopify",
                    "En Shopify el SKU y el código de barras corresponden a variantes "
                    "distintas del maestro; corregir la variante en Shopify",
                    f"Shopify SKU {s_sku} / código {s_cb}")
    return maestro, unicas, shopify[shopify["Llave"] == ""]


# --------------------------------------------------------------------------
# 3. Normalizar (Criterios)
# --------------------------------------------------------------------------

def cambiar(df, i, campo, nuevo, rev, tipo, accion, evidencia=""):
    anterior = df.at[i, campo]
    if anterior == nuevo:
        return
    df.at[i, campo] = nuevo
    rev.add(df.loc[i], campo, anterior, nuevo, tipo, accion, evidencia)


def normalizar(df, rev):
    for i in df.index:
        r = df.loc[i]
        nivel_padre = "padre" in r["Origen del registro"]

        # Regla de campos vacíos: ningún texto sustituto.
        for c in ATRIBUTOS:
            if r[c] in TEXTOS_SUSTITUTOS:
                cambiar(df, i, c, "", rev, "Corrección aplicada",
                        "Texto sustituto eliminado: el campo se deja realmente vacío")

        for c in ("Precio de compra", "Precio de venta"):
            if r[c] != "" and numero(r[c]) == 0:
                cambiar(df, i, c, "", rev, "Requiere revisión",
                        "Precio cero tratado como dato desconocido; capturar el precio real")

        # Claves SAT de 8 dígitos que perdieron el cero inicial.
        sat = df.at[i, "SAT Clave de producto"]
        if re.fullmatch(r"\d{7}", sat):
            cambiar(df, i, "SAT Clave de producto", sat.zfill(8), rev, "Corrección aplicada",
                    "Se restituye el cero inicial de la clave SAT (8 dígitos)")

        # Paso 4 y 5: homologación de tallas.
        for campo, tabla in (("WB Talla", TALLA_MX), ("WB Talla de EE. UU.", TALLA_US)):
            valor = df.at[i, campo]
            if "(" in valor:
                limpio = re.sub(r"\s*\(.*?\)", "", valor).strip()
                cambiar(df, i, campo, limpio, rev, "Corrección aplicada",
                        "Se eliminan equivalencias entre paréntesis")
                valor = limpio
            if valor.upper() in tabla:
                cambiar(df, i, campo, tabla[valor.upper()], rev, "Corrección aplicada",
                        f"Talla homologada según Criterios ({valor} → {tabla[valor.upper()]})")

        # Género: Dama / Caballero.
        genero = df.at[i, "WB Género"]
        if genero in ("Dama", "Caballero"):
            cambiar(df, i, "WB Género", {"Dama": "Mujer", "Caballero": "Hombre"}[genero], rev,
                    "Corrección aplicada", "Género homologado según Criterios")

        # Color: nombres comerciales a color base.
        color = df.at[i, "WB Color"]
        if color and color not in COLORES_VALIDOS:
            bases = colores_en(color)
            if len(bases) == 1:
                cambiar(df, i, "WB Color", bases.pop(), rev, "Corrección aplicada",
                        "Nombre comercial traducido al color base con Sinónimos")

        descripcion = df.at[i, "WB Descripcion"]

        # Paso 1: Categoría y División por palabra clave cuando falta.
        if not df.at[i, "WB Categoría"]:
            categorias = categorias_por_palabra(descripcion)
            if len(categorias) == 1:
                cambiar(df, i, "WB Categoría", categorias[0], rev, "Completado por regla",
                        "Categoría asignada por palabra clave", f"WB Descripcion: {descripcion}")
            elif categorias:
                rev.add(df.loc[i], "WB Categoría", "", "", "Requiere revisión",
                        "La descripción menciona varias categorías (kit o conjunto); "
                        "asignar manualmente", f"WB Descripcion: {descripcion} · "
                        f"coincidencias: {', '.join(categorias)}")
        categoria = df.at[i, "WB Categoría"]
        if categoria in CATEGORIA_DIVISION:
            division = CATEGORIA_DIVISION[categoria]
            if df.at[i, "WB División"] != division:
                previo = df.at[i, "WB División"]
                cambiar(df, i, "WB División", division, rev,
                        "Corrección aplicada" if previo else "Completado por regla",
                        "División tomada de la tabla de categorías",
                        f"WB Categoría: {categoria}")
            # Paso 7: Unidad por categoría.
            unidad = "PRS" if categoria in CALZADO_PRS else "PZS"
            if df.at[i, "Unidad"] != unidad:
                previo = df.at[i, "Unidad"]
                cambiar(df, i, "Unidad", unidad, rev,
                        "Corrección aplicada" if previo else "Completado por regla",
                        "Unidad según categoría (PRS calzado, PZS lo demás)",
                        f"WB Categoría: {categoria}")

        # Paso 2: Género explícito en la descripción.
        if not df.at[i, "WB Género"]:
            generos = generos_en(descripcion)
            if len(generos) == 1:
                cambiar(df, i, "WB Género", generos.pop(), rev, "Completado por regla",
                        "Género tomado de la descripción", f"WB Descripcion: {descripcion}")
            elif not generos and df.at[i, "WB División"] == "Accesorios":
                cambiar(df, i, "WB Género", "Unisex", rev, "Completado por regla",
                        "Accesorio sin género → Unisex", f"WB Descripcion: {descripcion}")

        # Paso 6: Color base presente en la descripción.
        if not df.at[i, "WB Color"] and not nivel_padre:
            bases = colores_en(descripcion)
            if len(bases) == 1:
                cambiar(df, i, "WB Color", bases.pop(), rev, "Completado por regla",
                        "Color base identificado en la descripción; confirmar que es el "
                        "dominante", f"WB Descripcion: {descripcion}")

        # Paso 8 y 9: Fit y Silueta solo donde aplican.
        division = df.at[i, "WB División"]
        if df.at[i, "WB Fit"] and division in ("Calzado", "Accesorios"):
            cambiar(df, i, "WB Fit", "", rev, "Corrección aplicada",
                    "Fit no aplica en calzado, sombreros y accesorios: campo vacío")
        silueta = df.at[i, "WB Silueta"]
        if silueta and categoria in CATEGORIA_DIVISION and categoria not in (
                "Sombreros", "Botas", "Zapatos", "Jeans", "Tenis", "Pantuflas"):
            cambiar(df, i, "WB Silueta", "", rev, "Corrección aplicada",
                    "Silueta no aplica en esta categoría: campo vacío",
                    f"WB Categoría: {categoria}")

        # Productos sin talla física.
        if (categoria in FAMILIA_TALLA_UNICA and not nivel_padre
                and not df.at[i, "WB Talla"] and not df.at[i, "WB Talla de EE. UU."]):
            cambiar(df, i, "WB Talla", "Talla única", rev, "Completado por regla",
                    "Familia Talla única", f"WB Categoría: {categoria}")
            cambiar(df, i, "WB Talla de EE. UU.", "One Size", rev, "Completado por regla",
                    "Familia Talla única", f"WB Categoría: {categoria}")


# --------------------------------------------------------------------------
# 4. Completar con Shopify (solo campos vacíos del maestro)
# --------------------------------------------------------------------------

def completar_con_shopify(df, unicas, rev):
    tipo = "Completado desde Shopify"
    for i in df.index[df["Origen de la fusión"] == "Maestro + Shopify"]:
        r = df.loc[i]
        s = unicas.loc[r["Código de barras"]]
        evidencia = f"Shopify {s['Handle']} / variante {s['Variant ID']}"

        if not r["Enlace de imagen"] and s["Image Src"]:
            cambiar(df, i, "Enlace de imagen", s["Image Src"], rev, tipo,
                    "Imagen principal del producto en Shopify", evidencia)

        if not r["WB Descripción larga"] and s["Body HTML"]:
            texto = html_a_texto(s["Body HTML"])
            if texto:
                cambiar(df, i, "WB Descripción larga", texto, rev, tipo,
                        "Descripción de la ficha de Shopify (HTML convertido a texto)",
                        evidencia)

        if not r["WB País de origen"] and s["Variant Country of Origin"]:
            codigo = s["Variant Country of Origin"]
            if codigo in PAISES:
                cambiar(df, i, "WB País de origen", PAISES[codigo], rev, tipo,
                        "País de origen declarado en la variante de Shopify",
                        f"{evidencia} ({codigo})")

        if not r["WB Composición"] and s["materiales"]:
            texto = rich_text_a_texto(s["materiales"])
            compuesto = normalizar_composicion(texto)
            if compuesto:
                cambiar(df, i, "WB Composición", compuesto, rev, tipo,
                        "Composición de la ficha de Shopify normalizada", f"{evidencia}: {texto}")
            elif texto:
                rev.add(r, "WB Composición", "", "", "Requiere revisión",
                        "Shopify trae materiales sin porcentajes completos; capturar desde "
                        "etiqueta o ficha técnica", f"{evidencia}: {texto}")

        if not r["WB Temporada"] and s["season"]:
            if s["season"] in TEMPORADA_SHOPIFY:
                cambiar(df, i, "WB Temporada", TEMPORADA_SHOPIFY[s["season"]], rev, tipo,
                        "Temporada declarada en Shopify", f"{evidencia}: {s['season']}")
            else:
                rev.add(r, "WB Temporada", "", "", "Requiere revisión",
                        "La temporada de Shopify no existe en la lista de Criterios",
                        f"{evidencia}: {s['season']}")

        if not r["WB Fit"] and s["corte"] and r["WB División"] in ("Ropa", "Denim"):
            fit = CORTE_A_FIT.get(s["corte"].strip())
            if fit:
                cambiar(df, i, "WB Fit", fit, rev, tipo, "Corte de Shopify homologado a Fit",
                        f"{evidencia}: {s['corte']}")
            else:
                rev.add(r, "WB Fit", "", "", "Requiere revisión",
                        "El corte de Shopify no tiene equivalencia en la lista de Fit",
                        f"{evidencia}: {s['corte']}")

        # Precio: el maestro manda; se documentan diferencias con la tienda.
        venta = numero(r["Precio de venta"])
        precio, comparacion = numero(s["Variant Price"]), numero(s["Variant Compare At Price"])
        regular = comparacion if comparacion and comparacion > (precio or 0) else precio
        if venta is None and regular:
            cambiar(df, i, "Precio de venta", s["Variant Compare At Price"]
                    if regular == comparacion else s["Variant Price"], rev, tipo,
                    "Precio regular de la variante en Shopify", evidencia)
        elif venta is not None and regular is not None and abs(venta - regular) >= 0.01:
            rev.add(r, "Precio de venta", r["Precio de venta"], r["Precio de venta"],
                    "Conflicto maestro-Shopify",
                    "El precio regular en Shopify difiere del maestro; se conserva el maestro",
                    f"{evidencia}: precio {s['Variant Price']}, comparación "
                    f"{s['Variant Compare At Price'] or '—'}")


# --------------------------------------------------------------------------
# Variantes que solo existen en Shopify
# --------------------------------------------------------------------------

def filas_solo_shopify(sin_empate, codigos_maestro, rev):
    filas = []
    for _, s in sin_empate.iterrows():
        f = {c: "" for c in ATRIBUTOS}
        codigo = s["Variant Barcodes"] or (s["Variant SKU"] if s["Variant SKU"].isdigit()
                                          and 12 <= len(s["Variant SKU"]) <= 14 else "")
        f.update({
            "Código de barras": codigo, "WB SKU": s["Variant SKU"],
            "Marca principal": "Ariat", "WB Marca": "Ariat",
            "WB N.º de estilo": s["estilo"], "WB Descripcion": s["Title"],
            "WB Descripción larga": html_a_texto(s["Body HTML"]) if s["Body HTML"] else "",
            "Enlace de imagen": s["Image Src"],
            "WB País de origen": PAISES.get(s["Variant Country of Origin"], ""),
        })
        precio, comparacion = numero(s["Variant Price"]), numero(s["Variant Compare At Price"])
        if comparacion and comparacion > (precio or 0):
            f["Precio de venta"] = s["Variant Compare At Price"]
        elif precio:
            f["Precio de venta"] = s["Variant Price"]
        if numero(s["Variant Cost"]):
            f["Precio de compra"] = s["Variant Cost"]
        if s["season"] in TEMPORADA_SHOPIFY:
            f["WB Temporada"] = TEMPORADA_SHOPIFY[s["season"]]
        compuesto = normalizar_composicion(rich_text_a_texto(s["materiales"]))
        f["WB Composición"] = compuesto

        # Talla desde las opciones solo cuando la regla es «Igual» (ropa alfa).
        valor = s["Option1 Value"].strip().upper()
        valor = TALLA_MX.get(valor, valor)
        una_opcion = s["Option1 Name"] in ("Talla", "Size", "Tamaño") and not (
            s["Option2 Value"] not in ("", "#VALUE!") or s["Option3 Value"])
        if una_opcion and valor in TALLAS_ALFA:
            f["WB Talla"] = f["WB Talla de EE. UU."] = valor

        f.update({
            "Origen del registro": "Nuevo – Shopify Ariat (sin empate en maestro)",
            "Origen de la fusión": "Solo Shopify",
            "Shopify ID producto": s["ID"], "Shopify ID variante": s["Variant ID"],
            "Shopify Handle": s["Handle"], "Shopify Estatus": s["Status"],
            "Shopify Título": s["Title"], "Shopify Opciones": s["Opciones"],
            "Shopify SKU": s["Variant SKU"], "Shopify Código de barras": s["Variant Barcodes"],
            "Shopify Precio": s["Variant Price"],
            "Shopify Precio comparación": s["Variant Compare At Price"],
            "Shopify Inventario": s["Variant Inventory Qty"], "Shopify Empate": "Sin empate",
        })
        filas.append(f)

        motivo = ("Variante de Shopify sin código de barras" if not codigo else
                  "Código de barras de Shopify inexistente en el maestro")
        cercanos = [c for c in codigos_maestro
                    if c.startswith(codigo) or codigo.startswith(c) or c == codigo.zfill(12)
                    ] if len(codigo) >= 10 else []
        evidencia = f"Shopify {s['Handle']} / variante {s['Variant ID']} / {s['Opciones']}"
        if cercanos:
            evidencia += " · posibles coincidencias en maestro: " + ", ".join(cercanos[:5])
        rev.add(f, "Código de barras", s["Variant Barcodes"], codigo, "Requiere revisión",
                motivo + "; confirmar identidad antes de cargar", evidencia)
    return pd.DataFrame(filas)


# --------------------------------------------------------------------------
# 5. Validar
# --------------------------------------------------------------------------

def validar(df):
    codigos = df["Código de barras"]
    skus = df["WB SKU"]
    dup_cb = codigos.duplicated(keep=False) & (codigos != "")
    dup_sku = skus.duplicated(keep=False) & (skus != "")
    estatus, detalle, niveles = [], [], []

    for i, r in df.iterrows():
        errores, avisos = [], []
        padre = "padre" in r["Origen del registro"]
        niveles.append("Padre / agrupador" if padre else "Variante")
        cb = r["Código de barras"]

        if padre and not r["WB N.º de estilo"]:
            errores.append("Padre sin WB N.º de estilo")
        if not padre:
            if not cb:
                errores.append("Código de barras faltante")
            elif not cb.isdigit():
                errores.append("Código de barras con caracteres no numéricos")
            elif not 12 <= len(cb) <= 14:
                errores.append("Código de barras fuera de 12 a 14 dígitos")
            elif not digito_control_gtin(cb):
                errores.append("Dígito de control del código de barras inválido")
            if dup_cb[i]:
                errores.append("Código de barras duplicado")
            if not r["WB SKU"]:
                errores.append("WB SKU faltante")
            if dup_sku[i]:
                errores.append("WB SKU duplicado")
            if cb and not r["WB N.º de estilo"]:
                errores.append("Falta estilo")
            if not r["WB Talla"]:
                avisos.append("WB Talla no capturada")
            if not r["WB Talla de EE. UU."]:
                avisos.append("WB Talla de EE. UU. no capturada")
            if not r["Precio de venta"]:
                avisos.append("Precio de venta no capturado")

        listas = [("Marca principal", MARCAS_PRINCIPALES), ("WB Marca", MARCAS),
                  ("WB División", DIVISIONES), ("WB Categoría", set(CATEGORIA_DIVISION)),
                  ("WB Género", GENEROS), ("WB Temporada", TEMPORADAS),
                  ("WB Ciclo de vida", CICLOS), ("WB Color", COLORES_VALIDOS),
                  ("WB Fit", FIT_VALIDOS), ("Unidad", UNIDADES)]
        for campo, validos in listas:
            if r[campo] and r[campo] not in validos:
                errores.append(f"{campo} fuera de Criterios ({r[campo]})")

        categoria, division = r["WB Categoría"], r["WB División"]
        if categoria in CATEGORIA_DIVISION and division and \
                CATEGORIA_DIVISION[categoria] != division:
            errores.append("División no coincide con Categoría")
        for campo in ("WB División", "WB Categoría", "WB Género", "WB Temporada",
                      "WB Ciclo de vida"):
            if not r[campo]:
                avisos.append(f"{campo} no capturado")
        if not padre and not r["WB Color"]:
            avisos.append("WB Color no capturado")

        silueta = r["WB Silueta"]
        if silueta:
            if categoria == "Sombreros":
                validas = SILUETA_SOMBRERO
            elif categoria in ("Botas", "Zapatos"):
                validas = SILUETA_CALZADO
            elif categoria == "Jeans":
                validas = SILUETA_JEANS
            elif categoria in ("Tenis", "Pantuflas"):
                validas = SILUETA_CALZADO
                avisos.append("Silueta en Tenis/Pantuflas pendiente de confirmar en Criterios")
            else:
                validas = set()
            if silueta not in validas:
                errores.append(f"WB Silueta fuera de Criterios para {categoria or 'sin categoría'}"
                               f" ({silueta})")

        sat = r["SAT Clave de producto"]
        if sat and not re.fullmatch(r"\d{8}", sat):
            errores.append("SAT Clave de producto no tiene 8 dígitos")
        for campo in ("Precio de compra", "Precio de venta"):
            if r[campo] and numero(r[campo]) is None:
                errores.append(f"{campo} no numérico")
        if r["Enlace de imagen"] and not r["Enlace de imagen"].startswith("http"):
            errores.append("Enlace de imagen no es una URL")

        if errores:
            estatus.append("Con incidencias")
        elif avisos:
            estatus.append("Válido con avisos")
        else:
            estatus.append("Válido")
        detalle.append("; ".join(errores + [f"[Aviso] {a}" for a in avisos]))

    df.insert(0, "Nivel G1522", niveles)
    df["Estatus G1522"] = estatus
    df["Incidencias G1522"] = detalle
    return df


# --------------------------------------------------------------------------
# Salida
# --------------------------------------------------------------------------

def resumen(base, rev, total_shopify, sin_empate):
    filas = [
        ("Filas en maestro (Ariat.xlsx)", int((base["Origen de la fusión"] != "Solo Shopify").sum())),
        ("Variantes en Shopify (Products.csv)", total_shopify),
        ("Variantes empatadas maestro + Shopify", int((base["Origen de la fusión"] == "Maestro + Shopify").sum())),
        ("Variantes solo en Shopify agregadas", int((base["Origen de la fusión"] == "Solo Shopify").sum())),
        ("  · sin código de barras", int((sin_empate["Variant Barcodes"] == "").sum())),
        ("Filas en base unificada", len(base)),
        ("", ""),
    ]
    for estado, n in base["Estatus G1522"].value_counts().items():
        filas.append((f"Estatus G1522: {estado}", int(n)))
    filas.append(("", ""))
    tabla = rev.groupby(["Tipo", "Campo"]).size().reset_index(name="Registros")
    filas += [(f"Revisión · {t} · {c}", int(n)) for t, c, n in tabla.itertuples(index=False)]
    return pd.DataFrame(filas, columns=["Concepto", "Valor"])


def escribir(base, rev, res):
    numericas = ["Precio de compra", "Precio de venta"]
    for c in numericas:
        base[c] = pd.to_numeric(base[c], errors="coerce")
    with pd.ExcelWriter(SALIDA, engine="xlsxwriter",
                        engine_kwargs={"options": {"strings_to_numbers": False,
                                                   "strings_to_urls": False}}) as xw:
        for nombre, tabla in (("Productos", base), ("Revisión", rev), ("Resumen", res)):
            tabla.to_excel(xw, sheet_name=nombre, index=False)
            hoja = xw.sheets[nombre]
            hoja.freeze_panes(1, 0)
            hoja.autofilter(0, 0, len(tabla), len(tabla.columns) - 1)
            hoja.set_column(0, len(tabla.columns) - 1, 18)


def main():
    rev = Revision()
    maestro = leer_maestro()
    shopify = leer_shopify()
    print(f"Maestro: {len(maestro)} filas · Shopify: {len(shopify)} variantes")

    base, unicas, sin_empate = empatar(maestro, shopify, rev)
    print(f"Empatadas: {(base['Origen de la fusión'] == 'Maestro + Shopify').sum()}"
          f" · Shopify sin empate: {len(sin_empate)}")

    codigos = set(base.loc[base["Código de barras"] != "", "Código de barras"])
    nuevas = filas_solo_shopify(sin_empate, codigos, rev)
    base = pd.concat([base, nuevas], ignore_index=True).fillna("")

    normalizar(base, rev)
    completar_con_shopify(base, unicas, rev)
    base = validar(base)

    columnas_shopify = [c for c in base.columns if c.startswith("Shopify ")]
    control = [c for c in maestro.columns if c not in ATRIBUTOS and c not in columnas_shopify
               and c != "Origen de la fusión"]
    orden = (["Nivel G1522"] + ATRIBUTOS + ["Estatus G1522", "Incidencias G1522",
             "Origen de la fusión"] + columnas_shopify + control)
    base = base[orden]

    revision = rev.tabla()
    res = resumen(base, revision, len(shopify), sin_empate)
    escribir(base, revision, res)
    print(res.to_string(index=False))
    print(f"Archivo generado: {SALIDA.name}")


if __name__ == "__main__":
    main()
