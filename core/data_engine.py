import geopandas as gpd
import pandas as pd
import streamlit as st
from pathlib import Path
from shapely.geometry import Point

DATA = Path("data")


@st.cache_data
def cargar_datos():
    """Carga todas las capas y tablas del proyecto."""

    lotes = gpd.read_file(DATA / "Lotes del CAM.gpkg")
    perimetro = gpd.read_file(DATA / "Perimetro CAM.gpkg")
    suelos = gpd.read_file(DATA / "Poligonos del mapa de suelos.gpkg")
    aptitud = gpd.read_file(DATA / "Poligonos del mapa de Aptitud del suelo.gpkg")
    malezas = pd.read_excel(DATA / "Plantas Arvenses del CAM.xlsx")

    # Limpiar nombres de columnas
    lotes.columns = lotes.columns.str.strip()
    perimetro.columns = perimetro.columns.str.strip()
    suelos.columns = suelos.columns.str.strip()
    aptitud.columns = aptitud.columns.str.strip()
    malezas.columns = malezas.columns.str.strip()

    # Todo el proyecto trabajará en WGS84
    lotes = lotes.to_crs(4326)
    perimetro = perimetro.to_crs(4326)
    suelos = suelos.to_crs(4326)
    aptitud = aptitud.to_crs(4326)

    return {
        "lotes": lotes,
        "perimetro": perimetro,
        "suelos": suelos,
        "aptitud": aptitud,
        "malezas": malezas,
    }


from config import IMAGES, COL_UT, COL_CULTIVOS, APTITUD_DICT, LIMIT_DICT

def obtener_ruta_imagen(nombre_especie):
    """
    Busca la imagen de una especie en la carpeta IMAGES.
    Devuelve la ruta si existe, o None si no hay imagen.
    """

    carpeta = Path(IMAGES)
    nombre = nombre_especie.strip()

    for ext in [".png", ".jpg", ".jpeg", ".JPG", ".PNG", ".JPEG"]:
        ruta = carpeta / f"{nombre}{ext}"
        if ruta.exists():
            return ruta

    return None


def obtener_centro(lotes):
    """Centro del mapa."""

    centroide = lotes.unary_union.centroid

    return [
        centroide.y,
        centroide.x,
    ]

def obtener_lote_por_click(lotes, lat, lon):
    """
    Devuelve la fila del lote que contiene el punto seleccionado.
    """

    punto = Point(lon, lat)

    seleccion = lotes[lotes.contains(punto)]

    if seleccion.empty:
        return None

    return seleccion.iloc[0]

def obtener_malezas_lote(df, nombre_lote):
    """
    Devuelve todas las especies registradas en un lote.
    """

    import re

    numero = re.findall(r"\d+", nombre_lote)

    if len(numero) == 0:
        return df.iloc[0:0]

    numero = numero[0]

    seleccion = []

    for _, fila in df.iterrows():

        lotes = str(fila["Lotes"])

        numeros = re.findall(r"\d+", lotes)

        if numero in numeros:

            seleccion.append(fila)

    if len(seleccion) == 0:

        return df.iloc[0:0]

    return seleccion

@st.cache_data
def obtener_fragmentos():
    """
    Calcula la intersección triple Lotes ∩ Suelos ∩ Aptitud.
    Cada fragmento resultante tiene el símbolo del suelo, la unidad
    de tierra y la aptitud de cada cultivo en esa zona exacta.
    """

    datos = cargar_datos()

    lotes_p = datos["lotes"].to_crs(3857)
    suelos_p = datos["suelos"].to_crs(3857)
    aptitud_p = datos["aptitud"].to_crs(3857)

    paso1 = gpd.overlay(
        lotes_p[["Nombre", "geometry"]],
        suelos_p[["Simbolo", "Caracteristicas principales", "geometry"]],
        how="intersection",
        keep_geom_type=True,
    )

    fragmentos = gpd.overlay(
        paso1[["Nombre", "Simbolo", "Caracteristicas principales", "geometry"]],
        aptitud_p[[COL_UT, "Limitaciones"] + COL_CULTIVOS + ["geometry"]],
        how="intersection",
        keep_geom_type=True,
    )

    fragmentos = fragmentos[
        ~fragmentos["geometry"].is_empty
        & fragmentos["geometry"].notna()
        & fragmentos["Nombre"].notna()
    ].copy()

    fragmentos["Simbolo"] = fragmentos["Simbolo"].fillna("Sin datos")
    fragmentos[COL_UT] = fragmentos[COL_UT].fillna("Sin datos")
    fragmentos["Caracteristicas principales"] = fragmentos[
        "Caracteristicas principales"
    ].fillna("Sin datos")
    fragmentos["Limitaciones"] = fragmentos["Limitaciones"].fillna("Sin datos")

    for c in COL_CULTIVOS:
        fragmentos[c] = fragmentos[c].fillna("—")

    fragmentos = fragmentos.rename(columns={COL_UT: "UT_Aptitud"})
    fragmentos = fragmentos.to_crs(4326).reset_index(drop=True)

    return fragmentos


def obtener_fragmento_por_click(fragmentos, lat, lon):
    """
    Devuelve (indice, fila) del fragmento que contiene el punto clicado.
    """

    punto = Point(lon, lat)

    seleccion = fragmentos[fragmentos.contains(punto)]

    if seleccion.empty:
        return None

    return seleccion.index[0], seleccion.iloc[0]


def traducir_codigo(codigo):
    """
    Traduce un código de aptitud (ej: 'A2oh') a texto legible.
    Espejo de la lógica del prototipo de Colab.
    """

    if codigo is None or str(codigo).strip() in ("", "—", "nan"):
        return None

    codigo = str(codigo).strip()

    if codigo.startswith("A1"):
        clase, subclases = "A1", codigo[2:]
    elif codigo.startswith("A2"):
        clase, subclases = "A2", codigo[2:]
    elif codigo.startswith("A3"):
        clase, subclases = "A3", codigo[2:]
    elif codigo.startswith("N"):
        clase, subclases = "N", codigo[1:]
    else:
        return None

    texto_clase = APTITUD_DICT.get(clase, clase)

    limitaciones = [
        LIMIT_DICT[letra.lower()]
        for letra in subclases
        if letra.lower() in LIMIT_DICT
    ]

    if limitaciones:
        return f"{texto_clase} por limitación de {', '.join(limitaciones)}"

    return texto_clase