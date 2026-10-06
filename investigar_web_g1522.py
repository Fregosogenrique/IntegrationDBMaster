"""Investigación en línea para completar el catálogo G1522.

Consulta lo que cada marca o su distribuidor publica y lo traduce a los valores de
Criterios. El resultado, Investigacion_web_G1522.csv, lo aplica homologar_ciclico_g1522.py
solo sobre campos vacíos, con la URL como evidencia en «Fuentes de consulta».

Fuentes (catálogos públicos):
  · westernbrothers.mx, ariat.com.mx      Shopify, en español; el SKU es el código de barras.
  · stetson.mx, stetson.com               Shopify; el SKU es el WB SKU de NetSuite.
  · montanawestworld.com                  Shopify; Montana West y bolsos Wrangler.
  · www.willowlanehats.com, reflo.com     Shopify (REFLO: código de barras por variante).
  · ariat.com                             Ficha por número de estilo (Ariat).

Reglas (Anatomia_productos_atributos_G1522.md y hoja Criterios):
  · Solo se escribe un valor que existe en las listas de Criterios: color base por la
    tabla de sinónimos, categoría por palabra clave, género de la lista básica.
  · Si la fuente da más de un valor posible, no se escribe nada.
  · Composición solo con porcentajes que suman 100 %; país solo si la ficha lo declara
    («Made in USA», «Hecho en México»), nunca a partir de «Imported».
  · No se toman de internet llaves internas (SKU, código de barras), temporada,
    ciclo de vida ni precios.

Uso:  python3 investigar_web_g1522.py [--cache DIR]
      Las descargas se guardan en DIR (por omisión .cache_web) y se reutilizan.
"""

import argparse
import csv
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

import homologar_ariat_g1522 as g
import homologar_ciclico_g1522 as h

BASE = Path(__file__).resolve().parent
SALIDA = BASE / "Investigacion_web_G1522.csv"
FECHA = "06/10/2026"
AGENTE = {"User-Agent": "Mozilla/5.0 (investigacion catalogo G1522)"}

TIENDAS = {
    # tienda: (llave con la que empata, idioma, marca por omisión)
    "westernbrothers.mx": ("Código de barras", "es", ""),
    "ariat.com.mx": ("Código de barras", "es", "Ariat"),
    "stetson.mx": ("WB SKU", "es", "Stetson"),
    "www.stetson.com": ("WB SKU", "en", "Stetson"),
    "montanawestworld.com": ("WB SKU", "en", "Montana West"),
    "www.willowlanehats.com": ("WB SKU", "en", "Willow Lane"),
    "reflo.com": ("Código de barras", "en", "REFLO"),
}

# Palabras en inglés de las fichas → categoría de Criterios (misma idea que la tabla
# «Palabra clave → Categoría», traducida). La primera coincidencia manda.
EN_CATEGORIA = [
    ("boot care", "Cuidado de Botas"), ("hat care", "Cuidado de Sombreros"),
    ("hat band", "Plumas para sombrero"), ("feather", "Plumas para sombrero"),
    ("cap", "Gorras"), ("trucker", "Gorras"), ("snapback", "Gorras"), ("beanie", "Gorras"),
    ("cowboy hat", "Sombreros"), ("hat", "Sombreros"), ("bandana", "Bandanas"),
    ("wild rag", "Bandanas"), ("wallet", "Carteras"), ("money clip", "Carteras"),
    ("belt", "Cinturones"), ("buckle", "Hebillas"), ("backpack", "Mochilas"),
    ("handbag", "Bolsos"), ("purse", "Bolsos"), ("tote", "Bolsos"), ("crossbody", "Bolsos"),
    ("satchel", "Bolsos"), ("clutch", "Bolsos"), ("bag", "Bolsos"), ("keychain", "Llaveros"),
    ("blanket", "Cobijas"), ("scarf", "Bufandas"), ("knife", "Cuchillos"),
    ("fragrance", "Fragancias"), ("cologne", "Fragancias"), ("perfume", "Fragancias"),
    ("jeans", "Jeans"), ("jean", "Jeans"), ("boot", "Botas"), ("sneaker", "Tenis"),
    ("slipper", "Pantuflas"), ("shoe", "Zapatos"), ("sock", "Calcetines"),
    ("t-shirt", "Playeras"), ("tee", "Playeras"), ("polo", "Playeras"), ("shirt", "Camisas"),
    ("vest", "Chalecos"), ("jacket", "Chamarras"), ("coat", "Chamarras"), ("skirt", "Faldas"),
    ("jumpsuit", "Jumpsuits"), ("pant", "Pantalones"), ("trouser", "Pantalones"),
    ("shorts", "Shorts"), ("hoodie", "Sudaderas"), ("sweatshirt", "Sudaderas"),
    ("sweater", "Sueteres"), ("cardigan", "Sueteres"), ("dress", "Vestidos"),
]
GENERO_CLAVES = [("Hombre", ["hombre", "caballero", "men", "mens", "men's", "male"]),
                 ("Mujer", ["mujer", "dama", "women", "womens", "women's", "ladies", "female"]),
                 ("Niño", ["niño", "boys", "boy's"]),
                 ("Niña", ["niña", "girls", "girl's"]),
                 ("Unisex", ["unisex"])]
PAIS_CLAVES = [("Estados Unidos", r"made in (?:the )?u\.?s\.?a?\.?\b|hecho en (?:los )?(?:usa|e\.?u\.?a?\.?|estados unidos)"),
               ("México", r"made in mexico|hecho en mexico"),
               ("China", r"made in china|hecho en china"),
               ("India", r"made in india|hecho en india"),
               ("Vietnam", r"made in vietnam|hecho en vietnam")]
# Fit solo cuando la ficha nombra el corte («Relaxed Fit», «Corte Recto»), no por una
# palabra suelta como «classic» en el texto publicitario.
WEB_FIT_CLAVES = [("Relajado", ["relaxed fit", "corte relajado", "fit relajado"]),
                  ("Slim", ["slim fit", "corte slim", "fit slim"]),
                  ("Clásico", ["classic fit", "corte clasico", "fit clasico"]),
                  ("Moderno", ["modern fit", "corte moderno", "fit moderno"]),
                  ("Regular", ["regular fit", "corte regular", "fit regular"]),
                  ("Recto", ["straight fit", "straight leg", "corte recto", "pierna recta"]),
                  ("Bootcut", ["bootcut", "boot cut", "corte de bota", "corte bota"])]
COLOR_SINONIMOS = dict(g.COLORES)
COLOR_SINONIMOS["Azul"] = COLOR_SINONIMOS["Azul"] + ["Mezclilla", "Denim"]
COLOR_SINONIMOS["Beige"] = COLOR_SINONIMOS["Beige"] + ["Tan"]
PATRONES_COLOR = [(g.patron_palabra(s), base) for base, sin in COLOR_SINONIMOS.items()
                  for s in [base] + sin]


# --------------------------------------------------------------------------
# Descargas (reutilizan la caché)
# --------------------------------------------------------------------------

def pedir_json(url, intentos=6):
    for intento in range(intentos):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=AGENTE),
                                        timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return None
            time.sleep(20 * (intento + 1) if e.code == 429 else 5)
        except Exception:
            time.sleep(10)
    return None


def catalogo_shopify(tienda, cache):
    destino = cache / f"{tienda}.json"
    if destino.exists():
        return json.loads(destino.read_text())
    productos, pagina = [], 1
    while True:
        datos = pedir_json(f"https://{tienda}/products.json?limit=250&page={pagina}")
        if not datos or not datos.get("products"):
            break
        productos += datos["products"]
        pagina += 1
        time.sleep(4)
    destino.write_text(json.dumps(productos, ensure_ascii=False))
    return productos


def codigos_shopify(tienda, productos, cache):
    """Código de barras por variante (products.json no lo trae; /products/<handle>.js sí)."""
    destino = cache / f"{tienda}.barcodes.json"
    if destino.exists():
        return json.loads(destino.read_text())
    codigos = {}
    for p in productos:
        d = pedir_json(f"https://{tienda}/products/{p['handle']}.js")
        if d:
            codigos[p["handle"]] = {str(v["id"]): v.get("barcode") for v in d.get("variants", [])}
        time.sleep(2)
    destino.write_text(json.dumps(codigos))
    return codigos


def fichas_ariat(estilos, cache):
    """Ficha de ariat.com por número de estilo (caché en líneas JSON, reanudable)."""
    fichas = {}
    for archivo in sorted(cache.glob("ariat_com_estilos*.jsonl")):
        for linea in archivo.open():
            d = json.loads(linea)
            fichas[d["estilo"]] = d
    url = ("https://www.ariat.com/on/demandware.store/Sites-Ariat-Site/en_US/"
           "Product-Variation?pid={}&quantity=1")
    with (cache / "ariat_com_estilos.jsonl").open("a") as out:
        for e in estilos:
            if e in fichas:
                continue
            p = (pedir_json(url.format(urllib.parse.quote(e))) or {}).get("product") or {}
            imagenes = (p.get("images") or {}).get("zoom") or []
            sel = (p.get("selectedVariationAttributesObject") or {}).get("color") or {}
            d = {"estilo": e, "estado": "ok" if p.get("productName") else "sin producto",
                 "nombre": p.get("productName"), "genero": p.get("genderID") or p.get("gender"),
                 "categoria": p.get("category"), "departamento": p.get("department"),
                 "grupo": p.get("productGroup"), "subgrupo": p.get("subGroup"),
                 "color": sel.get("displayValue"),
                 "imagen": imagenes[0]["url"] if imagenes else None,
                 "descripcion": p.get("longDescription"),
                 "url": p.get("detailPageUrl") or p.get("productUrl")}
            out.write(json.dumps(d, ensure_ascii=False) + "\n")
            fichas[e] = d
            time.sleep(1)
    return fichas


# --------------------------------------------------------------------------
# Traducción a Criterios
# --------------------------------------------------------------------------

def color_base(valor):
    """Color base del nombre comercial; si trae dos colores, el primero (dominante)."""
    if not valor:
        return ""
    primero = re.split(r"[/|,]| - ", valor)[0]
    t = g.sin_acentos(primero)
    bases = {base for patron, base in PATRONES_COLOR if patron.search(t)}
    return bases.pop() if len(bases) == 1 else ""


def categoria(texto, idioma):
    if idioma == "es":
        encontradas = g.categorias_por_palabra(texto)
        return encontradas[0] if len(encontradas) == 1 else ""
    t = " " + g.sin_acentos(texto).replace("’", "'") + " "
    for clave, cat in EN_CATEGORIA:
        if re.search(r"\b" + re.escape(clave) + r"(?:s|es)?\b", t):
            return cat
    return ""


def genero(textos):
    t = " ".join(g.sin_acentos(x) for x in textos if x)
    hallados = {gen for gen, claves in GENERO_CLAVES
                if any(re.search(r"(?<![a-z])" + re.escape(g.sin_acentos(c)) + r"(?![a-z])", t)
                       for c in claves)}
    return hallados.pop() if len(hallados) == 1 else ""


def pais(texto):
    t = g.sin_acentos(texto)
    hallados = {p for p, patron in PAIS_CLAVES if re.search(patron, t)}
    return hallados.pop() if len(hallados) == 1 else ""


def composicion(texto):
    for linea in re.split(r"\n|•|;|\. ", texto):
        if "%" in linea:
            limpia = re.sub(r"(?i)^.*?(composici[oó]n|materiales?|material|fabric|shell)\s*:?", "", linea)
            compuesto = g.normalizar_composicion(limpia)
            if compuesto:
                return compuesto
    return ""


def unico(texto, claves):
    valores = h.valores_clave(texto, claves)
    return valores.pop() if len(valores) == 1 else ""


def silueta(texto):
    todas = set()
    for claves in h.SILUETA_CLAVES.values():
        todas |= h.valores_clave(texto, claves)
    return todas.pop() if len(todas) == 1 else ""


def registros_tienda(tienda, productos, codigos, cache):
    llave, idioma, marca = TIENDAS[tienda]
    filas = []
    for p in productos:
        url = f"https://{tienda}/products/{p['handle']}"
        cuerpo = g.html_a_texto(p.get("body_html") or "")
        titulo = p.get("title") or ""
        tags = p.get("tags") or []
        nombres = [o["name"].lower() for o in p.get("options", [])]
        pos_color = next((i for i, n in enumerate(nombres) if n in ("color", "colour")), None)
        pos_talla = next((i for i, n in enumerate(nombres) if n in ("talla", "size", "tamaño")), None)
        imagen_producto = (p.get("images") or [{}])[0].get("src", "")
        comunes = {
            "WB Categoría": categoria(f"{titulo} {p.get('product_type') or ''}", idioma),
            "WB Género": genero([titulo, p.get("product_type")] + tags),
            "WB Composición": composicion(cuerpo),
            "WB País de origen": pais(cuerpo),
            "WB Silueta": silueta(f"{titulo} {cuerpo}"),
            "WB Fit": unico(f"{titulo} {cuerpo}", WEB_FIT_CLAVES),
        }
        if idioma == "es" and len(cuerpo) >= 40:
            comunes["WB Descripción larga"] = cuerpo
        estilos = [t for t in tags if re.fullmatch(r"\d{7,8}", t)]
        if llave == "Código de barras" and len(estilos) == 1:
            comunes["WB N.º de estilo"] = estilos[0]
        for v in p.get("variants", []):
            if llave == "Código de barras":
                valor = (codigos.get(p["handle"], {}).get(str(v["id"])) if codigos
                         else v.get("sku")) or ""
                if not re.fullmatch(r"\d{12,14}", valor):
                    continue
            else:
                valor = v.get("sku") or ""
                if not valor:
                    continue
            propios = dict(comunes)
            imagen = (v.get("featured_image") or {}).get("src") or imagen_producto
            if imagen.startswith("//"):
                imagen = "https:" + imagen
            if imagen:
                propios["Enlace de imagen"] = imagen
            if pos_color is not None:
                propios["WB Color"] = color_base(v.get(f"option{pos_color + 1}"))
            if pos_talla is not None and codigos:
                talla = (v.get(f"option{pos_talla + 1}") or "").strip().upper()
                talla = {"2XL": "XXL", "3XL": "XXXL", "O/S": "Talla única", "OS": "Talla única",
                         "ONE SIZE": "Talla única"}.get(talla, talla)
                if talla in g.TALLAS_ALFA + ["Talla única"]:
                    propios["WB Talla"] = talla
                    propios["WB Talla de EE. UU."] = "One Size" if talla == "Talla única" else talla
            if tienda == "reflo.com":
                propios["WB Descripcion"] = titulo
            for campo, dato in propios.items():
                if dato:
                    filas.append({"Llave": llave, "Valor_llave": valor, "Marca": marca,
                                  "Campo": campo, "Valor": dato, "Fuente": url, "Fecha": FECHA,
                                  "Evidencia": f"{tienda}: {titulo}"[:200]})
    return filas


def registros_ariat(fichas):
    filas = []
    for e, d in fichas.items():
        if d.get("estado") != "ok":
            continue
        texto = f"{d.get('nombre') or ''} {d.get('subgrupo') or ''} {d.get('descripcion') or ''}"
        datos = {
            "WB Color": color_base(d.get("color")),
            "WB Género": {"men": "Hombre", "women": "Mujer", "boys": "Niño", "girls": "Niña",
                          "unisex": "Unisex"}.get((d.get("genero") or "").lower(), ""),
            "WB Categoría": categoria(f"{d.get('nombre') or ''} {d.get('subgrupo') or ''}", "en"),
            "WB Silueta": silueta(texto),
            "WB Fit": unico(texto, WEB_FIT_CLAVES),
            "WB País de origen": pais(d.get("descripcion") or ""),
            # Sin foto, Ariat devuelve una imagen de relleno («zoom_missing»).
            "Enlace de imagen": d.get("imagen") if str(d.get("imagen")).startswith("http")
            and "missing" not in str(d.get("imagen")) else "",
        }
        url = d.get("url") or f"https://www.ariat.com/{e}.html"
        for campo, dato in datos.items():
            if dato:
                filas.append({"Llave": "WB N.º de estilo", "Valor_llave": e, "Marca": "Ariat",
                              "Campo": campo, "Valor": dato, "Fuente": url, "Fecha": FECHA,
                              "Evidencia": f"ariat.com: {d.get('nombre')} · {d.get('color') or ''}"})
    return filas


def estilos_ariat_pendientes():
    """Estilos Ariat del Cíclico con color, imagen, clasificación o silueta vacíos."""
    df = pd.read_excel(h.CICLICO, sheet_name="Productos", dtype=str, engine="calamine").fillna("")
    a = df[(df["WB Marca"] == "Ariat") & (df["WB N.º de estilo"] != "")
           & ~df["Origen del registro"].str.contains("padre")]
    falta = (a[["WB Color", "Enlace de imagen", "WB Categoría", "WB Género"]] == "").any(axis=1) \
        | ((a["WB Silueta"] == "") & a["WB Categoría"].isin(["Botas", "Zapatos", "Jeans", "Sombreros"]))
    return sorted(set(a.loc[falta, "WB N.º de estilo"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", default=str(BASE / ".cache_web"))
    cache = Path(parser.parse_args().cache)
    cache.mkdir(exist_ok=True)
    filas = []
    for tienda in TIENDAS:
        productos = catalogo_shopify(tienda, cache)
        codigos = codigos_shopify(tienda, productos, cache) if tienda == "reflo.com" else None
        nuevas = registros_tienda(tienda, productos, codigos, cache)
        print(f"{tienda}: {len(productos)} productos, {len(nuevas)} datos")
        filas += nuevas
    fichas = fichas_ariat(estilos_ariat_pendientes(), cache)
    nuevas = registros_ariat(fichas)
    print(f"ariat.com: {sum(d.get('estado') == 'ok' for d in fichas.values())} de "
          f"{len(fichas)} estilos encontrados, {len(nuevas)} datos")
    filas += nuevas
    tabla = pd.DataFrame(filas).drop_duplicates(["Llave", "Valor_llave", "Campo", "Valor"])
    # Solo lo que corresponde a un producto del Cíclico.
    ciclico = pd.read_excel(h.CICLICO, sheet_name="Productos", dtype=str,
                            engine="calamine").fillna("")
    norm = lambda t: re.sub(r"[^A-Z0-9]", "", str(t).upper())
    existentes = {"Código de barras": set(ciclico["Código de barras"].str.lstrip("0")) - {""},
                  "WB SKU": set(ciclico["WB SKU"].map(norm)) - {""},
                  "WB N.º de estilo": set(ciclico["WB N.º de estilo"].map(norm)) - {""}}
    llave = [v.lstrip("0") if k == "Código de barras" else norm(v)
             for k, v in zip(tabla["Llave"], tabla["Valor_llave"])]
    tabla = tabla[[v in existentes[k] for k, v in zip(tabla["Llave"], llave)]]
    # Si dos fuentes dan valores distintos al mismo campo, no se usa ninguno.
    conflicto = tabla.groupby(["Llave", "Valor_llave", "Campo"])["Valor"].transform("nunique") > 1
    tabla = tabla[~conflicto].drop_duplicates(["Llave", "Valor_llave", "Campo"])
    tabla.to_csv(SALIDA, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"{SALIDA.name}: {len(tabla)} datos ({int(conflicto.sum())} descartados por conflicto)")
    print(tabla.groupby(["Marca", "Campo"]).size().to_string())


if __name__ == "__main__":
    main()
