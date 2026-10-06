"""Homologación del Cíclico integrado bajo el estándar G1522, separado por marca.

Toma la hoja Productos de Ciclico_1522_investigado.xlsx (catálogo NetSuite
integrado con Shopify Stetson, Shopify Western Brothers y Odoo), le aplica las
mismas reglas que homologar_ariat_g1522.py más las de la hoja Criterios del
Cíclico, y genera archivos por marca de una sola hoja, optimizados para
trabajarse en Google Sheets mientras el inventario pasa al ERP.

Secuencia (Estructura_datos_validaciones_G1522.md, «Secuencia de validación y carga»):
  1. Preparar   - leer el Cíclico sin alterarlo; identificadores como texto.
                  Ariat suma la base ya homologada (Base_Unificada_Ariat_G1522.xlsx),
                  que es la única que conserva la evidencia de su tienda Shopify.
  2. Marca      - Marca principal; si es Multimarca, WB Licencia; si no, WB Marca;
                  sin marca: la del mismo estilo, el nombre en la descripción o el
                  prefijo del código.
  3. Normalizar - Criterios (homologar_ariat_g1522.normalizar) más los casos que
                  solo aparecen en el Cíclico: país, licencia, CORE, Pieza, ceros
                  iniciales del código, composición, coma decimal; y Criterios ›
                  3, 7, 8, 9 y 12 (talla de EE. UU., Fit, Silueta, bodega, desplegables).
  4. Integrar   - los registros que son el mismo producto se funden en uno:
                  mismo código (aun sin ceros iniciales), mismo SKU con estilo y
                  talla compatibles, o variante sin código igual a otra con código.
                  Los padres repetidos por estilo también se funden.
  5. Validar    - controles G1522 y los cuatro validadores (NetSuite, Odoo,
                  Shopify WB, Shopify Stetson) como columnas ya calculadas.
  6. Resolver   - todo cambio, fusión, conflicto o duda queda en «Revisión».

Uso:    python3 homologar_ciclico_g1522.py
Salida: carpeta Bases_Sheets_G1522/ con una carpeta por marca (Montana West y
        Wrangler juntos; Ariat con Productos dividido por División) y, en cada una,
        Productos, Revisión y Stock por ubicación en archivos de una sola hoja;
        más Indice_bases_G1522.xlsx y Listas_Criterios_G1522.xlsx.
"""

import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

import homologar_ariat_g1522 as g

BASE = Path(__file__).resolve().parent
CICLICO = BASE / "Ciclico_1522_investigado.xlsx"
ARIAT = BASE / "Base_Unificada_Ariat_G1522.xlsx"
SALIDA = BASE / "Bases_Sheets_G1522"

ATRIBUTOS = g.ATRIBUTOS
CAMPOS_FUSION = [c for c in ATRIBUTOS if c not in ("Código de barras", "Identificador interno")]

# Marcas que se trabajan en un mismo libro.
GRUPOS = {"Montana West": "Montana West + Wrangler", "Wrangler": "Montana West + Wrangler"}
# Una marca con más filas divide su archivo de Productos por División, para Sheets.
MAX_FILAS_LIBRO = 20000

g.TEXTOS_SUSTITUTOS |= {"(blank)", "(Blank)", "0.0"}

PAISES = {"mexico": "México", "mx": "México", "mex": "México",
          "usa": "Estados Unidos", "us": "Estados Unidos", "eua": "Estados Unidos",
          "eeuu": "Estados Unidos", "estados unidos": "Estados Unidos",
          "china": "China", "india": "India", "vietnam": "Vietnam"}
MATERIAL_ESCRITURA = {"algodon": "Algodón", "poliester": "Poliéster", "rayon": "Rayón",
                      "acrilico": "Acrílico", "nailon": "Nylon", "nylon": "Nylon",
                      "elastano": "Elastano", "poliamida": "Poliamida", "lana": "Lana",
                      "viscosa": "Viscosa", "lino": "Lino", "piel": "Piel"}

# Prioridad del registro que se conserva al fundir duplicados (árbol de decisión,
# Propuesta_Limpieza_Catalogo_Shopify_G1522.md §7): estructura y existencias primero.
PRIORIDAD_ORIGEN = [("Catálogo existente", 50), ("NetSuite con existencia", 46),
                    ("NetSuite —", 45), ("NetSuite sin existencia", 40),
                    ("Hoja a Revisar — artículo", 30), ("Shopify Stetson", 22),
                    ("Shopify Western", 22), ("Odoo", 20), ("Shopify Ariat", 15),
                    ("Carga Hoja", 10)]

NUMERICAS = ["Stock NetSuite", "Disponible NetSuite", "Stock Shopify Stetson",
             "Stock Shopify WB", "Stock Odoo", "Piezas escaneadas"]
TEXTOS_UNION = ["Ubicaciones con stock (NetSuite)", "Ubicaciones con existencia negativa"]
SHOPIFY_ARIAT = ["Shopify Handle", "Shopify ID producto", "Shopify ID variante", "Shopify Estatus"]
RENOMBRAR = {"Stock Sistema NetSuite": "Stock NetSuite",
             "Stock Shopify Stetson México": "Stock Shopify Stetson",
             "Stock Shopify Western Brothers": "Stock Shopify WB",
             "Stock Odoo Universal Unique Brands": "Stock Odoo"}


# --------------------------------------------------------------------------
# Bitácora
# --------------------------------------------------------------------------

class Revision(g.Revision):
    """La bitácora de Ariat con la fila de origen, para repartirla por libro."""

    COLUMNAS = g.Revision.COLUMNAS[:3] + ["WB Marca"] + g.Revision.COLUMNAS[3:]

    def add(self, fila, campo, origen, final, tipo, accion, evidencia=""):
        self.filas.append([fila.get("_uid", -1), fila.get("Código de barras", ""),
                           fila.get("WB SKU", ""), fila.get("Identificador interno", ""),
                           fila.get("WB Marca", ""), campo, origen, final, tipo, accion,
                           evidencia, ""])

    def tabla(self):
        return pd.DataFrame(self.filas, columns=["_uid"] + self.COLUMNAS)


def cambiar(df, i, campo, nuevo, rev, tipo, accion, evidencia=""):
    g.cambiar(df, i, campo, nuevo, rev, tipo, accion, evidencia)


# --------------------------------------------------------------------------
# 1. Preparar
# --------------------------------------------------------------------------

def leer_hoja(xl, hoja):
    df = pd.read_excel(xl, sheet_name=hoja, dtype=str).fillna("")
    df.columns = [str(c).strip() for c in df.columns]
    return df.apply(lambda s: s.str.strip())


def leer_ciclico():
    xl = pd.ExcelFile(CICLICO, engine="calamine")
    productos = leer_hoja(xl, "Productos")
    productos = productos[(productos[ATRIBUTOS] != "").any(axis=1)].reset_index(drop=True)
    productos = productos.rename(columns=RENOMBRAR)
    resumen = leer_hoja(xl, "Productos_Resumen")
    escaneadas = resumen[resumen["Piezas_Escaneadas"] != "0"].drop_duplicates("Id_Interno")
    productos["Piezas escaneadas"] = productos["Identificador interno"].map(
        escaneadas.set_index("Id_Interno")["Piezas_Escaneadas"]).fillna("")
    hojas = {h: leer_hoja(xl, h) for h in ("Stock por Ubicación", "Escaneos",
                                           "Revisión Duplicados")}
    criterios = pd.read_excel(xl, sheet_name="Criterios", dtype=str, header=None).fillna("")
    criterios = criterios.apply(lambda s: s.str.strip())
    return productos, hojas, leer_criterios(criterios)


def seccion(criterios, titulo, salto):
    """Filas de una tabla de Criterios (columnas A–D) hasta la siguiente sección."""
    inicio = criterios.index[criterios[0].str.startswith(titulo)][0] + salto
    filas = []
    for _, r in criterios.loc[inicio:].iterrows():
        if not r[0] or re.match(r"\d+\.\s", r[0]):
            break
        filas.append(r)
    return filas


def leer_criterios(criterios):
    """Lo que la hoja Criterios aporta al proceso.

    · 3 Categorías: familia de talla de cada categoría.
    · 8 Catálogo de tallas: parejas (familia, WB Talla, Talla de EE. UU.).
    · 9 Ubicaciones: bodega (25 / 43) de cada ubicación, columnas G y K.
    · 12 Listas automáticas: valores de los desplegables de Productos, columnas S a AD.
    """
    familias = {r[0]: r[2] for r in seccion(criterios, "3. CATEG", 3)}
    tallas = [(r[0], r[1], r[2]) for r in seccion(criterios, "8. CAT", 3)]
    encabezado = criterios.index[criterios[6] == "Ubicación"][0]
    bodegas = {r[6]: r[10] for _, r in criterios.loc[encabezado + 1:].iterrows()
               if r[6] and r[10]}
    listas = {}
    for j in range(18, 30):
        valores = [v for v in criterios.loc[encabezado:, j] if v]
        listas[valores[0]] = [v for v in valores[1:] if v not in g.TEXTOS_SUSTITUTOS]
    return {"familias": familias, "tallas": tallas, "bodegas": bodegas, "listas": listas,
            "parejas": {(mx, us) for _, mx, us in tallas}}


def leer_ariat():
    xl = pd.ExcelFile(ARIAT, engine="calamine")
    base = leer_hoja(xl, "Productos")
    revision = leer_hoja(xl, "Revisión")
    return base, revision


# --------------------------------------------------------------------------
# Ariat: evidencia de su tienda Shopify tomada de la base homologada
# --------------------------------------------------------------------------

def integrar_base_ariat(df, base, rev_ariat, rev):
    """Suma a Ariat lo que solo vive en Base_Unificada_Ariat_G1522.xlsx.

    Copia los IDs de Shopify, agrega las variantes que solo existen en Shopify y
    guarda para «completar_desde_ariat» los valores que se tomaron de la tienda.
    """
    for c in SHOPIFY_ARIAT:
        df[c] = ""
    empatada = base[base["Origen de la fusión"] != "Solo Shopify"]
    por_id = empatada[empatada["Identificador interno"] != ""].drop_duplicates(
        "Identificador interno").set_index("Identificador interno")
    hay = df["Identificador interno"].isin(por_id.index)
    for c in SHOPIFY_ARIAT:
        df.loc[hay, c] = df.loc[hay, "Identificador interno"].map(por_id[c])

    solo = base[base["Origen de la fusión"] == "Solo Shopify"].copy()
    solo["Origen del registro"] = "Nuevo – Shopify Ariat (sin empate en maestro)"
    solo = solo[[c for c in df.columns if c in solo.columns]]
    inicio = df["_uid"].max() + 1
    solo["_uid"] = range(inicio, inicio + len(solo))
    df = pd.concat([df, solo], ignore_index=True).fillna("")

    # Las decisiones sobre la tienda Shopify Ariat se conservan tal como se tomaron.
    tipos = {"Conflicto maestro-Shopify", "Conflicto Shopify"}
    campos_tienda = {"Código de barras", "WB Composición", "WB Fit"}
    conserva = rev_ariat[rev_ariat["Tipo"].isin(tipos) | (
        (rev_ariat["Tipo"] == "Requiere revisión") & rev_ariat["Campo"].isin(campos_tienda))]
    uid_cb = df[df["Código de barras"] != ""].drop_duplicates("Código de barras") \
        .set_index("Código de barras")["_uid"]
    uid_sku = df[df["WB SKU"] != ""].drop_duplicates("WB SKU").set_index("WB SKU")["_uid"]
    for fila in conserva.to_dict("records"):
        uid = uid_cb.get(fila["Código de barras"], uid_sku.get(fila["WB SKU"], -1))
        rev.add({"_uid": uid, "Código de barras": fila["Código de barras"],
                 "WB SKU": fila["WB SKU"], "Identificador interno": fila["Identificador interno"],
                 "WB Marca": "Ariat"}, fila["Campo"], fila["Valor origen"], fila["Valor final"],
                fila["Tipo"], fila["Incidencia / acción"], fila["Evidencia"])

    completados = rev_ariat[rev_ariat["Tipo"] == "Completado desde Shopify"]
    evidencia = {(r["Identificador interno"], r["Campo"]): r["Evidencia"]
                 for _, r in completados.iterrows() if r["Identificador interno"]}
    return df, (por_id, evidencia)


def completar_desde_ariat(df, ariat, rev):
    """Llena campos vacíos de Ariat con lo que la base Ariat tomó de Shopify."""
    valores, evidencia = ariat
    fila_de = {ident: i for i, ident in df["Identificador interno"].items() if ident}
    for (ident, campo), ev in evidencia.items():
        if ident not in valores.index or ident not in fila_de:
            continue
        nuevo, i = valores.at[ident, campo], fila_de[ident]
        if not df.at[i, campo] and nuevo:
            cambiar(df, i, campo, nuevo, rev, "Completado desde Shopify",
                    "Valor de la tienda Shopify Ariat (Base_Unificada_Ariat_G1522)", ev)


# --------------------------------------------------------------------------
# 2. Marca de las filas sin WB Marca
# --------------------------------------------------------------------------

def prefijo(texto):
    """Prefijo de código del proveedor: «CL/», «AR» en AR2842-220, «WACA» en WACA0213."""
    token = re.split(r"[\s:]+", texto.strip().upper())[0] if texto.strip() else ""
    m = re.match(r"[A-Z]{1,6}/|[A-Z]{2,5}(?=\d)", token)
    return m.group(0) if m else ""


def marca_canonica(texto):
    """La marca de la lista de Criterios escrita igual que «texto» (sin mayúsculas ni acentos)."""
    return {g.sin_acentos(m): m for m in g.MARCAS}.get(g.sin_acentos(texto.strip()), "")


def marca_archivo(r):
    """Marca que decide el libro: Marca principal; si es Multimarca o está vacía, la
    licencia; si la licencia no es una marca, WB Marca (ya completada por nombre o código)."""
    if r["Marca principal"] in g.MARCAS:
        return r["Marca principal"]
    return marca_canonica(r["WB Licencia"]) or r["WB Marca"]


def inferir_marcas(df, rev):
    con_marca = df[df["WB Marca"] != ""]
    por_estilo = con_marca[con_marca["WB N.º de estilo"] != ""].groupby(
        con_marca["WB N.º de estilo"].str.upper())["WB Marca"].agg(set)
    estadistica = defaultdict(Counter)
    for c in ("WB N.º de estilo", "WB SKU", "WB Descripcion"):
        for p, m in zip(con_marca[c].map(prefijo), con_marca["WB Marca"]):
            if p:
                estadistica[p][m] += 1
    por_prefijo = {}
    for p, cuenta in estadistica.items():
        marca, n = cuenta.most_common(1)[0]
        if n >= 5 and n / sum(cuenta.values()) >= 0.97:
            por_prefijo[p] = (marca, n)
    # Nombres de marca de una palabra también al inicio de un código pegado (ARIATMNS…).
    nombres = [(m, g.patron_palabra(m, "" if " " not in m and len(m) >= 5 else r"\b"))
               for m in sorted(g.MARCAS, key=len, reverse=True) if m != "Generico"]
    nombres.append(("CAPSLAB", g.patron_palabra("CAPS")))

    for i in df.index[df["WB Marca"] == ""]:
        r = df.loc[i]
        marca, evidencia = "", ""
        principal = r["Marca principal"]
        licencia = marca_canonica(r["WB Licencia"])
        estilo = r["WB N.º de estilo"].upper()
        if principal in g.MARCAS:
            marca, evidencia = principal, f"Marca principal: {principal}"
        elif licencia:
            marca, evidencia = licencia, f"WB Licencia: {r['WB Licencia']}"
        elif estilo and len(por_estilo.get(estilo, ())) == 1:
            marca = next(iter(por_estilo[estilo]))
            evidencia = f"Mismo WB N.º de estilo que otras filas de {marca}: {r['WB N.º de estilo']}"
        else:
            texto = g.sin_acentos(f"{r['WB Descripcion']} {r['WB Descripción larga']}")
            halladas = {m for m, patron in nombres if patron.search(texto)}
            if len(halladas) == 1:
                marca = halladas.pop()
                evidencia = f"La descripción nombra la marca: {r['WB Descripcion']}"
            else:
                prefijos = {prefijo(r[c]) for c in ("WB N.º de estilo", "WB SKU",
                                                    "WB Descripcion")} - {""}
                marcas = {por_prefijo[p][0] for p in prefijos if p in por_prefijo}
                if len(marcas) == 1:
                    marca = marcas.pop()
                    p = next(p for p in prefijos if p in por_prefijo)
                    evidencia = (f"Prefijo de código «{p}» usado en {por_prefijo[p][1]} filas "
                                 f"de {marca}: {r['WB Descripcion'] or r['WB SKU']}")
        if marca:
            cambiar(df, i, "WB Marca", marca, rev, "Completado por regla",
                    "Marca deducida; confirmar con el proveedor", evidencia)
        else:
            rev.add(r, "WB Marca", "", "", "Requiere revisión",
                    "Sin marca ni evidencia para deducirla; asignar manualmente",
                    f"{r['WB Descripcion']} · {r['Origen del registro']}")


# --------------------------------------------------------------------------
# 3. Normalizar: casos propios del Cíclico
# --------------------------------------------------------------------------

def codigo_de_sku(df, rev):
    """En NetSuite el Nombre/número del hijo es el UPC: un SKU con forma de GTIN válido
    en una variante sin código se usa como su código de barras."""
    for i in df.index[(df["Código de barras"] == "") & ~es_padre(df)]:
        sku = df.at[i, "WB SKU"]
        if sku.isdigit() and 12 <= len(sku) <= 14 and g.digito_control_gtin(sku):
            cambiar(df, i, "Código de barras", sku, rev, "Completado por regla",
                    "SKU con forma de código de barras válido (convención NetSuite: "
                    "Nombre/número del hijo = UPC)", f"WB SKU: {sku}")


def normalizar_extra(df, rev):
    licencias = df.loc[df["WB Licencia"] != "", "WB Licencia"]
    canon_marca = {g.sin_acentos(m): m for m in g.MARCAS}
    llave = lambda t: re.sub(r"\s+", " ", re.sub(r"\band\b", "&", g.sin_acentos(t))).strip()
    variantes = defaultdict(Counter)
    for valor, n in licencias.value_counts().items():
        variantes[llave(valor)][valor] = n
    canon_licencia = {}
    for k, cuenta in variantes.items():
        canon = canon_marca.get(k) or next((v for v, _ in cuenta.most_common() if "&" in v),
                                           cuenta.most_common(1)[0][0])
        for v in cuenta:
            canon_licencia[v] = canon

    for i in df.index:
        cb = df.at[i, "Código de barras"]
        if cb.isdigit() and len(cb) == 11 and g.digito_control_gtin(cb.zfill(12)):
            cambiar(df, i, "Código de barras", cb.zfill(12), rev, "Corrección aplicada",
                    "Se restituye el cero inicial del UPC (12 dígitos) perdido en Excel")

        for campo in ("Precio de compra", "Precio de venta"):
            precio = df.at[i, campo]
            if re.fullmatch(r"\d+,\d{1,2}", precio):
                cambiar(df, i, campo, precio.replace(",", "."), rev, "Corrección aplicada",
                        "Coma decimal convertida a punto")

        ciclo = df.at[i, "WB Ciclo de vida"]
        if ciclo and ciclo not in g.CICLOS and ciclo.capitalize() in g.CICLOS:
            cambiar(df, i, "WB Ciclo de vida", ciclo.capitalize(), rev, "Corrección aplicada",
                    "Ciclo de vida homologado a la lista de Criterios (Seasonal, Core)")

        if df.at[i, "Unidad"] == "Pieza":
            cambiar(df, i, "Unidad", "PZS", rev, "Corrección aplicada",
                    "Unidad homologada: Pieza → PZS")

        pais = df.at[i, "WB País de origen"]
        if pais and PAISES.get(g.sin_acentos(pais), pais) != pais:
            cambiar(df, i, "WB País de origen", PAISES[g.sin_acentos(pais)], rev,
                    "Corrección aplicada", "País de origen escrito con el nombre en español")

        licencia = df.at[i, "WB Licencia"]
        if licencia and canon_licencia.get(licencia, licencia) != licencia:
            cambiar(df, i, "WB Licencia", canon_licencia[licencia], rev, "Corrección aplicada",
                    "Licencia homologada a una sola escritura")

        composicion = df.at[i, "WB Composición"]
        if composicion:
            nueva = re.sub(r"[A-Za-zÁÉÍÓÚáéíóúñ]+", lambda m: MATERIAL_ESCRITURA.get(
                g.sin_acentos(m.group(0)), m.group(0)), composicion)
            if nueva != composicion:
                cambiar(df, i, "WB Composición", nueva, rev, "Corrección aplicada",
                        "Nombre del material escrito con acentos y mayúscula inicial")
            porcentajes = [float(p) for p in re.findall(r"(\d+(?:\.\d+)?)\s*%", nueva)]
            if porcentajes and not re.search(r"[:/]", nueva) and \
                    abs(sum(porcentajes) - 100) > 0.01:
                rev.add(df.loc[i], "WB Composición", nueva, nueva, "Requiere revisión",
                        "Los porcentajes no suman 100 % o el texto está truncado; "
                        "confirmar con la etiqueta", f"Suma: {sum(porcentajes):g} %")


# Criterios › 1, pasos 5, 8 y 9: talla de EE. UU., Fit y Silueta.
FIT_CLAVES = [("Relajado", ["relajado", "relaxed"]), ("Slim", ["slim"]),
              ("Clásico", ["clasico", "classic"]), ("Moderno", ["moderno", "modern"]),
              ("Recto", ["recto", "straight"]), ("Bootcut", ["bootcut", "boot cut", "corte bota"]),
              ("Regular", ["regular fit", "corte regular", "fit regular"])]
SILUETA_CLAVES = {
    "Sombreros": [(f"Copa {n}", [n.lower()]) for n in
                  ("Cattleman", "Rancher", "Pinch Front", "Teardrop", "Open Road", "Brick", "Gus")],
    "Calzado": [("Punta Redonda Ancha", ["punta redonda ancha", "broad round toe",
                                         "wide round toe"]),
                ("Punta Cuadrada Ancha", ["punta cuadrada ancha", "broad square toe",
                                          "wide square toe"]),
                ("Punta Cuadrada", ["punta cuadrada", "square toe"]),
                ("Punta Redonda", ["punta redonda", "round toe"]),
                ("Punta Ovalada", ["punta ovalada"]), ("Punta Snip", ["punta snip", "snip toe"]),
                ("Horma Alexia", ["alexia"]), ("Horma Agatha", ["agatha"])],
    "Jeans": [("Bootcut", ["bootcut", "boot cut", "corte bota"]), ("Recto", ["recto", "straight"]),
              ("Skinny", ["skinny"]), ("Tapered", ["tapered"]), ("Trouser", ["trouser"])],
}
CATEGORIA_SILUETA = {"Sombreros": "Sombreros", "Botas": "Calzado", "Zapatos": "Calzado",
                     "Jeans": "Jeans"}


def valores_clave(texto, claves):
    """Valores cuyas palabras clave aparecen; la frase más larga consume a la más corta
    (punta cuadrada ancha no cuenta también como punta cuadrada)."""
    t = " " + g.sin_acentos(texto) + " "
    hallados = []
    frases = sorted(((f, v) for v, fs in claves for f in fs), key=lambda x: -len(x[0]))
    for frase, valor in frases:
        patron = re.compile(r"\b" + re.escape(frase) + r"\b")
        if patron.search(t):
            hallados.append(valor)
            t = patron.sub(" ", t)
    return set(hallados)


def familias_de(categoria, genero, criterios):
    """Familias del catálogo de tallas (Criterios › 8) que corresponden a la categoría
    (Criterios › 3) y, cuando la familia distingue género, al género del producto."""
    texto = criterios["familias"].get(categoria, "")
    salida = set()
    for familia in {f for f, _, _ in criterios["tallas"]}:
        base = re.split(r" – | \(", familia)[0]
        sufijo = familia.split(" – ")[1].split(" ")[0] if " – " in familia else ""
        if base and base in texto and (not sufijo or not genero or sufijo == genero):
            salida.add(familia)
    return salida


def aplicar_criterios(df, rev, criterios):
    for i in df.index[~es_padre(df)]:
        r = df.loc[i]
        categoria, division = r["WB Categoría"], r["WB División"]
        talla, us = r["WB Talla"], r["WB Talla de EE. UU."]

        # Paso 5: la talla de EE. UU. sale de la misma fila del catálogo.
        if categoria and talla and not us:
            familias = familias_de(categoria, r["WB Género"], criterios)
            opciones = {u for f, mx, u in criterios["tallas"] if f in familias and mx == talla}
            if len(opciones) == 1:
                cambiar(df, i, "WB Talla de EE. UU.", opciones.pop(), rev, "Completado por regla",
                        "Talla de EE. UU. de la misma fila del catálogo de tallas (Criterios › 8)",
                        f"{categoria} · WB Talla {talla}")

        texto = f"{r['WB Descripcion']} {r['WB Descripción larga']}"
        # Paso 8: Fit solo en Ropa y Denim, con evidencia en la descripción.
        if not r["WB Fit"] and division in ("Ropa", "Denim"):
            fits = valores_clave(texto, FIT_CLAVES)
            if len(fits) == 1:
                cambiar(df, i, "WB Fit", fits.pop(), rev, "Completado por regla",
                        "Fit identificado en la descripción (Criterios › 7); confirmar",
                        texto[:300])
        # Paso 9: Silueta en Sombreros, Botas, Zapatos y Jeans.
        tipo = CATEGORIA_SILUETA.get(categoria)
        if tipo and not r["WB Silueta"]:
            siluetas = valores_clave(texto, SILUETA_CLAVES[tipo])
            if len(siluetas) == 1:
                cambiar(df, i, "WB Silueta", siluetas.pop(), rev, "Completado por regla",
                        "Silueta identificada en la descripción (Criterios › 7); confirmar",
                        texto[:300])


# --------------------------------------------------------------------------
# 4. Integrar productos iguales
# --------------------------------------------------------------------------

def es_padre(df):
    return df["Origen del registro"].str.contains("padre", na=False)


def prioridad(r):
    puntos = 0
    cb = r["Código de barras"]
    if cb.isdigit() and 12 <= len(cb) <= 14 and g.digito_control_gtin(cb):
        puntos += 100
    puntos += next((p for clave, p in PRIORIDAD_ORIGEN if clave in r["Origen del registro"]), 0)
    return puntos + sum(1 for c in ATRIBUTOS if r[c]) / 100


def compatibles(a, b, campos=("WB Marca", "WB N.º de estilo", "WB Talla", "WB Color")):
    return all(not a[c] or not b[c] or a[c].upper() == b[c].upper() for c in campos)


class Grupos:
    def __init__(self):
        self.padre = {}

    def raiz(self, x):
        while self.padre.get(x, x) != x:
            self.padre[x] = self.padre.get(self.padre[x], self.padre[x])
            x = self.padre[x]
        return x

    def unir(self, a, b):
        self.padre[self.raiz(b)] = self.raiz(a)


def integrar_duplicados(df, rev):
    """Funde en un registro los que representan el mismo producto."""
    padre = es_padre(df)
    grupos = Grupos()
    motivos = {}
    filas = df.to_dict("index")

    def ligar(indices, motivo):
        base = indices[0]
        for j in indices[1:]:
            if compatibles(filas[base], filas[j]):
                grupos.unir(base, j)
                motivos.setdefault(grupos.raiz(base), set()).add(motivo)
            else:
                rev.add(filas[j], "Código de barras" if "código" in motivo else "WB SKU",
                        filas[j]["Código de barras"] or filas[j]["WB SKU"],
                        filas[j]["Código de barras"] or filas[j]["WB SKU"],
                        "Requiere revisión",
                        f"Colisión de captura: {motivo} pero estilo, talla o color distintos; "
                        "corregir el valor equivocado",
                        f"Otra fila: ID {filas[base]['Identificador interno']} · estilo "
                        f"{filas[base]['WB N.º de estilo']} · talla {filas[base]['WB Talla']}")

    variantes = df[~padre]
    cb = variantes["Código de barras"].str.lstrip("0")
    for _, idx in variantes[cb != ""].groupby(cb[cb != ""]).groups.items():
        if len(idx) > 1:
            ligar(list(idx), "mismo código de barras")
    sku = variantes["WB SKU"].str.upper()
    for _, idx in variantes[sku != ""].groupby(sku[sku != ""]).groups.items():
        if len(idx) > 1:
            ligar(sorted(idx, key=lambda i: -prioridad(filas[i])), "mismo WB SKU")

    # Variante sin código igual (marca, estilo, talla y color) a una sola con código.
    llave = (variantes["WB Marca"] + "|" + variantes["WB N.º de estilo"].str.upper() + "|"
             + variantes["WB Talla"].str.upper())
    con_codigo = variantes[(variantes["Código de barras"] != "")
                           & (variantes["WB N.º de estilo"] != "")
                           & (variantes["WB Talla"] != "")]
    candidatas = con_codigo.groupby(llave[con_codigo.index]).groups
    for i in variantes.index[(variantes["Código de barras"] == "")
                             & (variantes["WB N.º de estilo"] != "")
                             & (variantes["WB Talla"] != "")]:
        opciones = [j for j in candidatas.get(llave[i], []) if compatibles(filas[i], filas[j])]
        if len(opciones) == 1:
            grupos.unir(opciones[0], i)
            motivos.setdefault(grupos.raiz(opciones[0]), set()).add(
                "variante sin código igual en estilo/talla/color")

    padres = df[padre & (df["WB N.º de estilo"] != "")]
    llave_padre = padres["WB Marca"] + "|" + padres["WB N.º de estilo"].str.upper()
    for _, idx in padres.groupby(llave_padre).groups.items():
        if len(idx) > 1:
            for j in list(idx)[1:]:
                grupos.unir(idx[0], j)
            motivos.setdefault(grupos.raiz(idx[0]), set()).add("padre repetido del mismo estilo")

    miembros = defaultdict(list)
    for i in df.index:
        miembros[grupos.raiz(i)].append(i)

    df["Códigos de barras alternos"] = ""
    df["Registros integrados"] = ""
    absorbidas, destino = [], {}
    for raiz, indices in miembros.items():
        if len(indices) == 1:
            continue
        indices.sort(key=lambda i: -prioridad(filas[i]))
        p, otros = indices[0], indices[1:]
        motivo = ", ".join(sorted(motivos.get(grupos.raiz(p), {"duplicado"})))
        alternos, integrados = [], []
        for j in otros:
            o = filas[j]
            destino[o["_uid"]] = df.at[p, "_uid"]
            if o["Código de barras"] and o["Código de barras"] != df.at[p, "Código de barras"] \
                    and o["Código de barras"].lstrip("0") != df.at[p, "Código de barras"].lstrip("0"):
                alternos.append(o["Código de barras"])
                rev.add(df.loc[p], "Código de barras", o["Código de barras"],
                        df.at[p, "Código de barras"], "Requiere revisión",
                        "El mismo producto tiene dos códigos de barras; se conserva el del "
                        "registro principal y el otro queda en «Códigos de barras alternos». "
                        "Confirmar cuál trae la etiqueta física",
                        f"ID {o['Identificador interno'] or '—'} · {o['Origen del registro']}")
            integrados.append(f"ID {o['Identificador interno'] or '—'} · "
                              f"{o['Origen del registro'] or 'sin origen'}"
                              + (f" · código {o['Código de barras']}" if o["Código de barras"] else ""))
            for c in CAMPOS_FUSION + SHOPIFY_ARIAT:
                if c not in df.columns or not o[c]:
                    continue
                actual = df.at[p, c]
                if not actual:
                    cambiar(df, p, c, o[c], rev, "Integrado de duplicado",
                            f"Campo vacío completado con el registro duplicado ({motivo})",
                            f"ID {o['Identificador interno'] or '—'} · {o['Origen del registro']}")
                elif g.sin_acentos(actual) != g.sin_acentos(o[c]) and c in ATRIBUTOS:
                    rev.add(df.loc[p], c, o[c], actual, "Conflicto entre duplicados",
                            "Se conserva el valor del registro principal; validar",
                            f"ID {o['Identificador interno'] or '—'} · {o['Origen del registro']}")
            for c in NUMERICAS:
                a, b = g.numero(df.at[p, c]), g.numero(o[c])
                if b is not None:
                    df.at[p, c] = f"{(a or 0) + b:g}"
            for c in TEXTOS_UNION:
                partes = [x for x in (df.at[p, c], o[c]) if x]
                df.at[p, c] = "; ".join(dict.fromkeys(partes))
        df.at[p, "Códigos de barras alternos"] = " | ".join(dict.fromkeys(alternos))
        df.at[p, "Registros integrados"] = f"{motivo}: " + " | ".join(integrados)
        rev.add(df.loc[p], "Registro", f"{len(indices)} registros", "1 registro",
                "Productos integrados", f"Se fundieron por {motivo}",
                " | ".join(integrados))
        absorbidas += otros
    return df.drop(index=absorbidas).reset_index(drop=True), destino


def completar_padres(df, rev):
    """El padre toma de sus variantes la clasificación compartida cuando es unánime."""
    padre = es_padre(df)
    variantes = df[~padre & (df["WB N.º de estilo"] != "")]
    llave = variantes["WB Marca"] + "|" + variantes["WB N.º de estilo"].str.upper()
    for campo in ("WB División", "WB Categoría", "WB Género", "WB Temporada",
                  "WB Ciclo de vida"):
        valores = variantes[variantes[campo] != ""].groupby(llave)[campo].agg(set)
        for i in df.index[padre & (df[campo] == "") & (df["WB N.º de estilo"] != "")]:
            k = f"{df.at[i, 'WB Marca']}|{df.at[i, 'WB N.º de estilo'].upper()}"
            if len(valores.get(k, ())) == 1:
                cambiar(df, i, campo, next(iter(valores[k])), rev, "Completado por regla",
                        "Atributo del modelo tomado de sus variantes (todas coinciden)",
                        f"WB N.º de estilo: {df.at[i, 'WB N.º de estilo']}")


# --------------------------------------------------------------------------
# 5. Validar
# --------------------------------------------------------------------------

def validar(df, parejas_talla):
    df = g.validar(df)
    cb, sku = df["Código de barras"], df["WB SKU"]
    rep_cb = cb.duplicated(keep=False) & (cb != "")
    rep_sku = sku.duplicated(keep=False) & (sku != "")
    talla_cero_valida = {"Vestidos", "Faldas", "Jeans", "Pantalones", "Shorts"}
    netsuite, shopify, avisos_talla = [], [], []
    for i, r in df.iterrows():
        if r["Nivel G1522"] != "Variante":
            netsuite.append("")
            shopify.append("")
            avisos_talla.append("")
            continue
        comun = []
        if not r["Código de barras"]:
            comun.append("V1: falta código de barras")
        elif not 12 <= len(r["Código de barras"]) <= 14:
            comun.append("V1: UPC debe tener 12-14 dígitos")
        if rep_cb[i]:
            comun.append("V2: UPC repetido")
        if rep_sku[i]:
            comun.append("V4: SKU repetido")
        if r["Código de barras"] and not r["WB N.º de estilo"]:
            comun.append("V6: falta estilo")
        ns = list(comun)
        talla = r["WB Talla"]
        if not talla or (talla == "0" and r["WB Categoría"] not in talla_cero_valida):
            ns.append("N2: talla cero o vacía")
        tienda = list(comun)
        venta = g.numero(r["Precio de venta"])
        if venta:
            con_iva = round(venta * 1.16, 2)
            if r["WB Marca"] == "Stetson":
                if con_iva % 50:
                    tienda.append("ST: precio con IVA no es múltiplo de 50")
            elif str(int(con_iva))[-1] != "9":
                tienda.append("WB: precio con IVA no termina en 9")
        netsuite.append(semaforo(ns))
        shopify.append(semaforo(tienda))
        us = r["WB Talla de EE. UU."]
        avisos = []
        if talla and us and (talla, us) not in parejas_talla:
            avisos.append("[Aviso] Pareja de tallas fuera del catálogo de Criterios")
        compra = g.numero(r["Precio de compra"])
        if compra and venta and compra < 20 <= venta / 10:
            # Decisión N5 del flujo NetSuite: confirmar la moneda del costo antes de cargar.
            avisos.append("[Aviso] Precio de compra posiblemente en USD")
        avisos_talla.append("; ".join(avisos))

    df["Validador NetSuite / Odoo"] = netsuite
    df["Validador Shopify"] = shopify
    extra = pd.Series(avisos_talla, index=df.index)
    con_aviso = extra != ""
    df.loc[con_aviso, "Incidencias G1522"] = (df.loc[con_aviso, "Incidencias G1522"]
                                              .where(df.loc[con_aviso, "Incidencias G1522"] == "",
                                                     df.loc[con_aviso, "Incidencias G1522"] + "; ")
                                              + extra[con_aviso])
    df.loc[con_aviso & (df["Estatus G1522"] == "Válido"), "Estatus G1522"] = "Válido con avisos"
    return df


def semaforo(motivos):
    return "✅ PASA" if not motivos else "❌ " + "; ".join(motivos)


# --------------------------------------------------------------------------
# Libros por marca
# --------------------------------------------------------------------------

def grupo_de(marca):
    return GRUPOS.get(marca, marca or "Sin marca")


def slug(texto):
    return re.sub(r"[^A-Za-z0-9]+", "_", g.sin_acentos(texto).title()).strip("_") \
        .replace("Capslab", "CAPSLAB").replace("Reflo", "REFLO")


def listas_criterios(criterios):
    """Listas de Criterios (12 Listas automáticas, 3 Categorías y 8 Tallas) en una tabla."""
    columnas = dict(criterios["listas"])
    columnas["Categoría"] = sorted(g.CATEGORIA_DIVISION)
    columnas["División de la categoría"] = [g.CATEGORIA_DIVISION[c] for c in columnas["Categoría"]]
    columnas["Familia de talla"] = [criterios["familias"].get(c, "") for c in columnas["Categoría"]]
    columnas["Catálogo de tallas: familia"] = [f for f, _, _ in criterios["tallas"]]
    columnas["Catálogo: WB Talla"] = [mx for _, mx, _ in criterios["tallas"]]
    columnas["Catálogo: Talla de EE. UU."] = [us for _, _, us in criterios["tallas"]]
    columnas["Ubicación"] = list(criterios["bodegas"])
    columnas["Bodega"] = list(criterios["bodegas"].values())
    n = max(len(v) for v in columnas.values())
    return pd.DataFrame({k: list(v) + [""] * (n - len(v)) for k, v in columnas.items()})


def escribir(ruta, tabla, desplegables=None):
    """Un archivo con una sola hoja, ligero para Google Sheets: valores sin fórmulas ni
    formato condicional, identificadores como texto y solo las celdas usadas. Los
    desplegables de Criterios › 12 son una regla por columna (aviso, no bloqueo)."""
    with pd.ExcelWriter(ruta, engine="xlsxwriter",
                        engine_kwargs={"options": {"strings_to_numbers": False,
                                                   "strings_to_urls": False,
                                                   "strings_to_formulas": False}}) as xw:
        nombre = ruta.stem[:31]
        tabla.to_excel(xw, sheet_name=nombre, index=False)
        hoja = xw.sheets[nombre]
        hoja.freeze_panes(1, 0)
        if len(tabla):
            hoja.autofilter(0, 0, len(tabla), len(tabla.columns) - 1)
        hoja.set_column(0, len(tabla.columns) - 1, 16)
        for columna, valores in (desplegables or {}).items():
            if columna not in tabla.columns or len(",".join(valores)) > 255 or not len(tabla):
                continue
            j = tabla.columns.get_loc(columna)
            hoja.data_validation(1, j, len(tabla), j, {
                "validate": "list", "source": valores, "error_type": "warning",
                "error_title": "Valor fuera de Criterios",
                "error_message": "Usa un valor de la lista de Criterios o deja la celda vacía."})


COLUMNAS_SALIDA = (["Nivel G1522"] + ATRIBUTOS
                   + ["Estatus G1522", "Incidencias G1522", "Validador NetSuite / Odoo",
                      "Validador Shopify", "Códigos de barras alternos", "Registros integrados",
                      "Origen del registro"]
                   + NUMERICAS[:2] + TEXTOS_UNION + NUMERICAS[2:])


def preparar_salida(productos, ariat):
    columnas = COLUMNAS_SALIDA + (SHOPIFY_ARIAT if ariat else [])
    tabla = productos[columnas].copy()
    for c in ["Precio de compra", "Precio de venta"] + NUMERICAS:
        numeros = pd.to_numeric(tabla[c], errors="coerce")
        # Un valor no numérico se conserva como texto para que se vea y se corrija.
        tabla[c] = numeros.astype(object).where(numeros.notna(), tabla[c].replace("", None))
    return tabla


def main():
    rev = Revision()
    productos, hojas, criterios = leer_ciclico()
    print(f"Cíclico: {len(productos)} filas con datos")
    productos["_uid"] = range(len(productos))

    base_ariat, rev_ariat = leer_ariat()
    productos, ariat = integrar_base_ariat(productos, base_ariat, rev_ariat, rev)
    print(f"Con variantes solo Shopify Ariat: {len(productos)}")

    # Diferencias con los precios vigentes antes de retirar esas columnas duplicadas.
    for campo, vigente in (("Precio de compra", "Precio compra vigente"),
                           ("Precio de venta", "Precio venta vigente")):
        a, b = productos[campo].map(g.numero), productos[vigente].map(g.numero)
        for i in productos.index[a.notna() & b.notna() & ((a - b).abs() >= 0.01)]:
            rev.add(productos.loc[i], campo, productos.at[i, vigente], productos.at[i, campo],
                    "Conflicto precio vigente",
                    "La columna de precio vigente del Cíclico difiere; se conserva el precio "
                    "del catálogo", f"{vigente}: {productos.at[i, vigente]}")

    inferir_marcas(productos, rev)
    codigo_de_sku(productos, rev)
    normalizar_extra(productos, rev)
    g.normalizar(productos, rev)
    completar_desde_ariat(productos, ariat, rev)  # La ficha de Shopify es mejor evidencia.
    aplicar_criterios(productos, rev, criterios)
    productos, destino = integrar_duplicados(productos, rev)
    print(f"Tras integrar productos iguales: {len(productos)}")
    completar_padres(productos, rev)
    productos = validar(productos, criterios["parejas"])

    revision = rev.tabla()
    revision["_uid"] = revision["_uid"].map(lambda u: destino.get(u, u))

    # Colisiones de código entre Productos y Shopify ya detectadas en el Cíclico.
    dup = hojas["Revisión Duplicados"]
    for _, r in dup[dup["Fuente"] != dup["Fuente"].iloc[0]].iterrows():
        revision.loc[len(revision)] = {
            "_uid": -1, "Código de barras": r["Código de barras"], "WB SKU": r["WB SKU"],
            "Identificador interno": "", "WB Marca": r["WB Marca"], "Campo": "Código de barras",
            "Valor origen": r["Código de barras"], "Valor final": r["Código de barras"],
            "Tipo": "Conflicto plataforma", "Incidencia / acción": r["Motivo"]
            + "; corregir el código en la plataforma", "Evidencia": f"{r['Fuente']} · grupo "
            f"{r['Grupo']} · {r['Identificador interno']}", "Responsable de validación": ""}

    # Stock por ubicación y escaneos, ligados al registro integrado por código o ID.
    llave_cb = {}
    for uid, principal, alternos in productos[["_uid", "Código de barras",
                                               "Códigos de barras alternos"]].itertuples(index=False):
        for c in [principal] + alternos.split(" | "):
            if c:
                llave_cb[c.lstrip("0")] = uid
    uid_id = productos[productos["Identificador interno"] != ""].set_index(
        "Identificador interno")["_uid"]
    stock = hojas["Stock por Ubicación"].drop(columns=["Fila en Productos"])
    stock.insert(1, "Bodega", stock["Ubicación (NetSuite / Plataforma)"].map(
        criterios["bodegas"]).fillna(""))
    stock["_uid"] = stock["Código de barras"].str.lstrip("0").map(llave_cb)
    stock["_uid"] = stock["_uid"].fillna(stock["Identificador interno"].map(uid_id)).fillna(-1)
    stock["Stock en ubicación (Físico)"] = pd.to_numeric(stock["Stock en ubicación (Físico)"],
                                                         errors="coerce")
    escaneos = hojas["Escaneos"].rename(columns={"Marca": "WB Marca"})
    escaneos.insert(3, "Bodega", escaneos["Ubicación / Rack"].map(criterios["bodegas"]).fillna(""))
    escaneos["_uid"] = escaneos["UPC CODE"].str.lstrip("0").map(llave_cb).fillna(-1)
    escaneos["Piezas Contadas"] = pd.to_numeric(escaneos["Piezas Contadas"], errors="coerce")

    # Libro de cada fila: Marca principal → Licencia → WB Marca (Multimarca no es libro).
    productos["Libro"] = productos.apply(marca_archivo, axis=1).map(grupo_de)
    for i in productos.index[(productos["Libro"] != productos["WB Marca"].map(grupo_de))
                             & (productos["WB Marca"] != "")]:
        revision.loc[len(revision)] = {
            "_uid": productos.at[i, "_uid"], "Código de barras": productos.at[i, "Código de barras"],
            "WB SKU": productos.at[i, "WB SKU"],
            "Identificador interno": productos.at[i, "Identificador interno"],
            "WB Marca": productos.at[i, "WB Marca"], "Campo": "WB Marca",
            "Valor origen": productos.at[i, "WB Marca"], "Valor final": productos.at[i, "WB Marca"],
            "Tipo": "Requiere revisión", "Incidencia / acción":
            "Marca principal o licencia apuntan a otra marca; el archivo sigue a la Marca "
            "principal / licencia", "Evidencia": f"Marca principal: "
            f"{productos.at[i, 'Marca principal']} · WB Licencia: {productos.at[i, 'WB Licencia']}",
            "Responsable de validación": ""}
    tamano = productos["Libro"].map(productos["Libro"].value_counts())
    productos["Parte"] = productos["WB División"].replace("", "Sin división") \
        .where(tamano > MAX_FILAS_LIBRO, "")
    orden_partes = ["", "Ropa", "Calzado", "Denim", "Accesorios", "Sin división"]
    partes = productos.groupby("Libro")["Parte"].agg(
        lambda x: sorted(set(x), key=orden_partes.index))
    destino_uid = productos.set_index("_uid")[["Libro", "Parte"]]
    for tabla in (revision, stock, escaneos):
        tabla["_uid"] = tabla["_uid"].astype(int)
        tabla["Libro"] = tabla["_uid"].map(destino_uid["Libro"])
        tabla["Parte"] = tabla["_uid"].map(destino_uid["Parte"])
        sin_fila = tabla["Libro"].isna()
        libro = tabla.loc[sin_fila, "WB Marca"].map(grupo_de)
        tabla.loc[sin_fila, "Libro"] = libro.where(libro.isin(partes.index), "Sin marca")
        tabla.loc[sin_fila, "Parte"] = tabla.loc[sin_fila, "Libro"].map(lambda l: partes[l][0])

    if SALIDA.exists():
        for viejo in sorted(SALIDA.rglob("*.xlsx")):
            viejo.unlink()
    SALIDA.mkdir(exist_ok=True)
    desplegables = {"Marca principal": criterios["listas"]["Marca principal"]}
    desplegables.update({f"WB {k}" if f"WB {k}" in ATRIBUTOS else k: v
                         for k, v in criterios["listas"].items() if k != "Marca principal"})
    indice = []

    def registrar(ruta, tabla, grupo, parte, contenido, filas=None):
        fila = {"Carpeta": ruta.parent.name, "Archivo": ruta.name, "Contenido": contenido,
                "Marca / grupo": grupo, "División": parte or "Todas", "Filas": len(tabla),
                "Columnas": len(tabla.columns), "Celdas": tabla.size,
                "Tamaño (MB)": round(ruta.stat().st_size / 1e6, 2)}
        if filas is not None:
            estatus = filas["Estatus G1522"].value_counts()
            fila.update({
                "Variantes": int((filas["Nivel G1522"] == "Variante").sum()),
                "Válido": int(estatus.get("Válido", 0)),
                "Válido con avisos": int(estatus.get("Válido con avisos", 0)),
                "Con incidencias": int(estatus.get("Con incidencias", 0)),
                "Productos integrados": int((filas["Registros integrados"] != "").sum()),
                "Validador NetSuite ✅": int((filas["Validador NetSuite / Odoo"] == "✅ PASA").sum()),
                "Validador Shopify ✅": int((filas["Validador Shopify"] == "✅ PASA").sum())})
        indice.append(fila)
        print(f"{ruta.relative_to(SALIDA)}: {len(tabla)} filas, {tabla.size:,} celdas", flush=True)

    for grupo in productos["Libro"].value_counts().index:
        carpeta = SALIDA / slug(grupo)
        carpeta.mkdir(exist_ok=True)
        dividido = partes[grupo] != [""]
        archivo_parte = {p: f"Productos_{slug(grupo)}{'_' + slug(p) if p else ''}.xlsx"
                         for p in partes[grupo]}
        for parte in partes[grupo]:
            filas = productos[(productos["Libro"] == grupo) & (productos["Parte"] == parte)]
            ruta = carpeta / archivo_parte[parte]
            tabla = preparar_salida(filas, grupo == "Ariat")
            escribir(ruta, tabla, desplegables)
            registrar(ruta, tabla, grupo, parte, "Productos", filas)
        for nombre, tabla, columnas in (
                ("Revision", revision, Revision.COLUMNAS),
                ("Stock_por_ubicacion", stock, [c for c in stock.columns
                                               if c not in ("_uid", "Libro", "Parte")]),
                ("Escaneos", escaneos, [c for c in escaneos.columns
                                        if c not in ("_uid", "Libro", "Parte")])):
            propia = tabla[tabla["Libro"] == grupo]
            if not len(propia):
                continue
            salida = propia[columnas].copy()
            if dividido:  # Con Ariat partido por División, cada renglón dice a qué archivo va.
                salida.insert(0, "Archivo de Productos", propia["Parte"].map(archivo_parte))
            ruta = carpeta / f"{nombre}_{slug(grupo)}.xlsx"
            escribir(ruta, salida)
            registrar(ruta, salida, grupo, "", nombre.replace("_", " "))

    listas = listas_criterios(criterios)
    escribir(SALIDA / "Listas_Criterios_G1522.xlsx", listas)
    registrar(SALIDA / "Listas_Criterios_G1522.xlsx", listas, "Todas", "", "Listas de Criterios")
    tabla = pd.DataFrame(indice)
    escribir(SALIDA / "Indice_bases_G1522.xlsx", tabla)
    print(tabla[tabla["Contenido"] == "Productos"].drop(columns=["Carpeta", "Contenido"])
          .to_string(index=False))


if __name__ == "__main__":
    main()
