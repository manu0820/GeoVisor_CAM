import streamlit as st

from streamlit_js_eval import streamlit_js_eval

from math import radians, sin, cos, sqrt, atan2

from datetime import datetime


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Asistencia Ciclo II 2026B",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# CONFIGURACIÓN DEL CAM
# ============================================================

LATITUD_CAM = 4.681785
LONGITUD_CAM = -74.216075

# Radio máximo permitido
RADIO_PERMITIDO = 100  # metros


# ============================================================
# TÍTULO
# ============================================================

st.title("📋 Asistencia Ciclo II 2026B")


st.write(
    "Seleccione su cultivo y registre su asistencia."
)


# ============================================================
# CULTIVOS
# ============================================================

cultivos = [
    "🥬 Acelga",
    "🌿 Alcachofa",
    "🔵 Arándano",
    "🌾 Avena",
    "🌱 Bulbo",
    "🥒 Calabacín",
    "🌿 Espárrago",
    "🌳 Feijoa",
    "🧅 Puerro",
    "🟠 Uchuva"
]


# ============================================================
# ESTUDIANTES
# ============================================================

estudiantes_por_cultivo = {

    "🥬 Acelga": [
        "Nancy Ximena Carrero",
        "Juan Esteban Huertas",
        "Daniel Cortés",
        "Gabriel Andres Guitierrez",
        "Liliana Maria Zea",
        "Paula Gabriela Riveros"
    ],

    "🌿 Alcachofa": [
        "Daniela Castillo",
        "Sergio Castellanos",
        "Alejandro Rojas",
        "Daniel Olivar",
        "Jhon Gómez",
        "jon Rodríguez"
    ],

    "🔵 Arándano": [
        "Angie Vanesa Lazo Sierra",
        "Harvey Steeven Ramos Puentes",
        "Sebastian Aparicio Guagua",
        "Jhon Alez Esquivel Benavides",
        "Alejandro Gil Cepeda",
        "Gustavo Andrés Garzón Pasachoa"
    ],

    "🌾 Avena": [
        "Ana Gabriela Rojas Gonzáles",
        "Emma Natalia Muñoz Jiménez",
        "Yuliana Henao Campuzano",
        "Jesus DAvid Manzano",
        "Daniel Alberto Robles Sanchez",
        "Brayan Hair Recaman Montaño"
    ],

    "🌱 Bulbo": [
        "Marcos Fuerte Martinez",
        "Maria Paula Gonzales Urrego",
        "Becky Ortiz Rivas",
        "Cesar Augusto Ospino Nieto",
        "Luisa Rojas Rincón",
        "Stefany Julieth Torres Pinzón",
        "Ana Maria Valero Parra"
    ],

    "🥒 Calabacín": [
        "Edna Valentina Acosta Romero",
        "Juan Sebastian Camelo Garcia",
        "Luis Fernando Gaitan Pinto",
        "Sofia Molano Jara",
        "Luis MArio Pardo Fontecha",
        "David Felipe Robles Saavedra"
    ],

    "🌿 Espárrago": [
        "Sergio Castellanos Bello",
        "Karen Daniela Pineda Aldana",
        "Damián Nicolás Piracún Farfán",
        "Karen DAyana Gonzalés Prieto",
        "Brayan Stive Vanegas León"
    ],

    "🌳 Feijoa": [
        "Paula Andrea Rodríguez Mosquera",
        "Danna Kendris Castañeda Montealegre",
        "Juan Nicolás Aguilera Forero",
        "Javier Stiven Chávez Muñoz",
        "Jhon Ferney Derazo Fuelpaz",
        "Manuel Ricardo Vargas Alejo",
        "Darwin Alejandro Linares Cardenas"
    ],

    "🧅 Puerro": [
        "Ardila Penagos Valentina Vanessa Alexandra",
        "Cetina Díaz Juan Carlos",
        "Daza Juan Sebastian",
        "Reyes Junco Nicolás David",
        "Sánchez Villegas Luisa Fernanda",
        "Quevedo Viviana",
        "Quintero Camacho Daniel Andrés"
    ],

    "🟠 Uchuva": [
        "Angie Valentina Castillo Martín",
        "Tomás Leonardo Casas",
        "Andrés Felipe Aranguren",
        "erónica Andrea Junco Trejos",
        "Raúl Mateo Vanegas",
        "Ingrid Tatiana Linares Anzola",
        "Daniel Alejandro Sánchez González"
    ]
}


# ============================================================
# VARIABLES DE SESIÓN
# ============================================================

if "cultivo_seleccionado" not in st.session_state:
    st.session_state.cultivo_seleccionado = None

if "estudiante_seleccionado" not in st.session_state:
    st.session_state.estudiante_seleccionado = None

if "accion" not in st.session_state:
    st.session_state.accion = None

if "solicitar_gps" not in st.session_state:
    st.session_state.solicitar_gps = False


# ============================================================
# FUNCIÓN PARA CALCULAR DISTANCIA
# ============================================================

def calcular_distancia(latitud, longitud):

    R = 6371000

    lat1 = radians(LATITUD_CAM)
    lat2 = radians(latitud)

    diferencia_latitud = radians(
        latitud - LATITUD_CAM
    )

    diferencia_longitud = radians(
        longitud - LONGITUD_CAM
    )

    a = (
        sin(diferencia_latitud / 2) ** 2
        +
        cos(lat1)
        * cos(lat2)
        * sin(diferencia_longitud / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


# ============================================================
# PANTALLA 1
# SELECCIONAR CULTIVO
# ============================================================

if st.session_state.cultivo_seleccionado is None:

    st.subheader("🌱 Seleccione su cultivo")

    st.markdown("---")

    col1, col2 = st.columns(2)

    for i, cultivo in enumerate(cultivos):

        if i % 2 == 0:

            with col1:

                if st.button(
                    cultivo,
                    use_container_width=True,
                    key=f"cultivo_{i}"
                ):

                    st.session_state.cultivo_seleccionado = cultivo

                    st.rerun()

        else:

            with col2:

                if st.button(
                    cultivo,
                    use_container_width=True,
                    key=f"cultivo_{i}"
                ):

                    st.session_state.cultivo_seleccionado = cultivo

                    st.rerun()


# ============================================================
# PANTALLA 2
# SELECCIONAR ESTUDIANTE
# ============================================================

elif st.session_state.estudiante_seleccionado is None:

    cultivo = st.session_state.cultivo_seleccionado

    st.subheader(
        f"{cultivo}"
    )

    st.write(
        "Seleccione su nombre."
    )

    st.markdown("---")

    estudiantes = estudiantes_por_cultivo[cultivo]

    for i, estudiante in enumerate(estudiantes):

        if st.button(
            estudiante,
            use_container_width=True,
            key=f"estudiante_{i}"
        ):

            st.session_state.estudiante_seleccionado = estudiante

            st.rerun()


    st.markdown("---")

    if st.button(
        "⬅️ Cambiar de cultivo",
        use_container_width=True
    ):

        st.session_state.cultivo_seleccionado = None

        st.rerun()


# ============================================================
# PANTALLA 3
# ESTUDIANTE
# ============================================================

else:

    cultivo = st.session_state.cultivo_seleccionado

    estudiante = st.session_state.estudiante_seleccionado


    st.subheader(
        f"👤 {estudiante}"
    )

    st.write(
        f"🌱 Cultivo: {cultivo}"
    )

    st.markdown("---")


    # ========================================================
    # BOTONES ENTRADA / SALIDA
    # ========================================================

    if not st.session_state.solicitar_gps:

        st.write(
            "Seleccione la acción que desea registrar:"
        )

        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # ENTRADA
        # ----------------------------------------------------

        with col1:

            if st.button(
                "🟢 ENTRAR",
                use_container_width=True
            ):

                st.session_state.accion = "Entrada"

                st.session_state.solicitar_gps = True

                st.rerun()


        # ----------------------------------------------------
        # SALIDA
        # ----------------------------------------------------

        with col2:

            if st.button(
                "🔴 SALIR",
                use_container_width=True
            ):

                st.session_state.accion = "Salida"

                st.session_state.solicitar_gps = True

                st.rerun()


    # ========================================================
    # SOLICITAR GPS
    # ========================================================

    else:

        accion = st.session_state.accion


        if accion == "Entrada":

            st.subheader(
                "🟢 Registrando entrada"
            )

        else:

            st.subheader(
                "🔴 Registrando salida"
            )


        st.info(
            "📍 Obteniendo ubicación..."
        )


        # ====================================================
        # JAVASCRIPT PARA OBTENER GPS
        # ====================================================

        ubicacion = streamlit_js_eval(
            js_expressions="""
            new Promise((resolve, reject) => {

                navigator.geolocation.getCurrentPosition(

                    position => {

                        resolve({

                            latitude:
                            position.coords.latitude,

                            longitude:
                            position.coords.longitude,

                            accuracy:
                            position.coords.accuracy

                        });

                    },

                    error => {

                        resolve({

                            error:
                            error.message

                        });

                    },

                    {

                        enableHighAccuracy: true,

                        timeout: 10000,

                        maximumAge: 0

                    }

                );

            })
            """,

            key="obtener_gps"
        )


        # ====================================================
        # PROCESAR GPS
        # ====================================================

        if ubicacion is not None:


            # ------------------------------------------------
            # ERROR GPS
            # ------------------------------------------------

            if "error" in ubicacion:

                st.error(
                    "❌ No fue posible obtener su ubicación."
                )

                st.write(
                    ubicacion["error"]
                )


            # ------------------------------------------------
            # GPS CORRECTO
            # ------------------------------------------------

            else:

                latitud = ubicacion["latitude"]

                longitud = ubicacion["longitude"]

                precision = ubicacion["accuracy"]


                # --------------------------------------------
                # CALCULAR DISTANCIA
                # --------------------------------------------

                distancia = calcular_distancia(
                    latitud,
                    longitud
                )


                st.metric(
                    "Distancia al CAM",
                    f"{distancia:.1f} metros"
                )


                st.write(
                    f"Precisión GPS: "
                    f"{precision:.1f} metros"
                )


                # ============================================
                # UBICACIÓN AUTORIZADA
                # ============================================

                if distancia <= RADIO_PERMITIDO:


                    fecha_hora = datetime.now()


                    st.success(
                        "🟢 Ubicación autorizada"
                    )


                    st.success(
                        f"✅ {accion} registrada correctamente"
                    )


                    st.write(
                        f"👤 **Estudiante:** "
                        f"{estudiante}"
                    )


                    st.write(
                        f"🌱 **Cultivo:** "
                        f"{cultivo}"
                    )


                    st.write(
                        f"📅 **Fecha:** "
                        f"{fecha_hora.strftime('%d/%m/%Y')}"
                    )


                    st.write(
                        f"⏰ **Hora:** "
                        f"{fecha_hora.strftime('%H:%M:%S')}"
                    )


                # ============================================
                # UBICACIÓN NO AUTORIZADA
                # ============================================

                else:


                    st.error(
                        "🔴 Ubicación no autorizada"
                    )


                    st.write(
                        f"Se encuentra a "
                        f"**{distancia:.1f} metros** "
                        f"del CAM."
                    )


                    st.write(
                        f"El máximo permitido es "
                        f"**{RADIO_PERMITIDO} metros**."
                    )


    # ========================================================
    # VOLVER
    # ========================================================

    st.markdown("---")


    if st.button(
        "⬅️ Volver a lista de estudiantes",
        use_container_width=True
    ):

        st.session_state.estudiante_seleccionado = None

        st.session_state.accion = None

        st.session_state.solicitar_gps = False

        st.rerun()