# ==========================
# Carpetas
# ==========================

DATA = "data"
IMAGES = "images"

# ==========================
# Mapa
# ==========================

CRS = 4326

ZOOM = 15

SATELLITE = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"

SATELLITE_ATTR = "Esri"

# ==========================
# Colores
# ==========================

COLOR_LOTES = "#4f81bd"

COLOR_PERIMETRO = "black"

COLOR_FRAGMENTOS = "#bbbbbb"

# ==========================
# Aptitud
# ==========================

COL_UT = "Unidad de tierra (UT)"

COL_CULTIVOS = [
    'Papa', 'Cebolla bulbo', 'Remolacha', 'Puerro', 'Ajo',
    'Arveja', 'Maiz', 'Quinua', 'Apio', 'Esparrago',
    'Manzano', 'Feijoa', 'Kikuyo', 'Trebol Rojo', 'Alfalfa',
    'Nabo forrajero', 'Avena forrajera', 'Raygrass Tetraploide'
]

APTITUD_DICT = {
    "A1": "Altamente apta",
    "A2": "Moderadamente apta",
    "A3": "Marginalmente apta",
    "N":  "No apta",
}

LIMIT_DICT = {
    "o": "disponibilidad de oxígeno",
    "h": "pH",
    "r": "penetrabilidad de raíces",
    "s": "contenido de sales",
    "w": "disponibilidad de agua",
}

COLOR_SUELOS = "#d95f02"
COLOR_APTITUD = "#1b9e77"