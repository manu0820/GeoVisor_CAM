import folium
from folium.plugins import FloatImage
from streamlit_folium import st_folium
from config import COLOR_SUELOS, COLOR_APTITUD

def crear_mapa(centro):
    """
    Crea el mapa base con Esri World Imagery.
    """

    m = folium.Map(
        location=centro,
        zoom_start=16,
        tiles=None,
        control_scale=True
    )

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri World Imagery",
        overlay=False,
        control=False,
    ).add_to(m)

    FloatImage(
        "https://raw.githubusercontent.com/manu0820/GeoVisor_CAM/main/images/rosa_vientos.png",
        bottom=5,
        left=5
        width="80px"
    ).add_to(m)

    return m


def agregar_lotes(m, gdf):

    estilo = {
        "color": "#00B7FF",
        "weight": 2,
        "fillColor": "#000000",
        "fillOpacity": 0,
    }

    folium.GeoJson(
        gdf,
        name="Lotes",
        style_function=lambda x: estilo,
        highlight_function=lambda x: {
            "color": "#00FFFF",
            "weight": 4,
            "fillColor": "#00FFFF",
            "fillOpacity": 0.15,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["Nombre"],
            aliases=["Lote"],
            sticky=False,
        ),
    ).add_to(m)


def agregar_perimetro(m, gdf):

    folium.GeoJson(
        gdf,
        name="Perímetro",
        style_function=lambda x: {
            "color": "black",
            "weight": 3,
            "fillOpacity": 0,
        },
    ).add_to(m)


def mostrar_mapa(m):

    salida = st_folium(
        m,
        width=None,
        height=700,
        returned_objects=[
            "last_clicked"
        ],
        use_container_width=True,
    )

    return salida

def agregar_suelos(m, gdf):

    folium.GeoJson(
        gdf,
        name="Suelos",
        interactive=False,
        style_function=lambda x: {
            "fillColor": COLOR_SUELOS,
            "color": COLOR_SUELOS,
            "weight": 1,
            "fillOpacity": 0.18,
        },
    ).add_to(m)


def agregar_aptitud(m, gdf):

    folium.GeoJson(
        gdf,
        name="Aptitud",
        interactive=False,
        style_function=lambda x: {
            "fillColor": COLOR_APTITUD,
            "color": COLOR_APTITUD,
            "weight": 1,
            "fillOpacity": 0.12,
        },
    ).add_to(m)


def agregar_fragmentos(m, fragmentos):
    """
    Capa invisible que solo muestra tooltip al pasar el mouse.
    El clic se captura aparte vía st_folium (last_clicked).
    """

    folium.GeoJson(
        fragmentos[["Nombre", "Simbolo", "UT_Aptitud", "geometry"]],
        name="Info hover",
        smooth_factor=0,
        style_function=lambda x: {
            "fillOpacity": 0.01,
            "color": "transparent",
            "weight": 0,
        },
        highlight_function=lambda x: {
            "fillColor": "#00ffff",
            "fillOpacity": 0.18,
            "color": "#00ffff",
            "weight": 2,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["Nombre", "Simbolo", "UT_Aptitud"],
            aliases=["🟦 Lote", "🟤 Suelo", "🟢 Aptitud"],
            sticky=False,
        ),
    ).add_to(m)
