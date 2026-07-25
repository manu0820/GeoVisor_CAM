import streamlit as st

from streamlit_geolocation import streamlit_geolocation

from math import radians, sin, cos, sqrt, atan2

from datetime import datetime


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

# Radio máximo permitido para registrar asistencia
RADIO_PERMITIDO = 100  # metros


# ============================================================
# TÍTULO
# ============================================================

st.title("📋 Asistencia Ciclo II 2026B")


# ============================================================
# LISTA DE CULTIVOS
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
        "Luis Mario Pardo Fontecha",
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
        "Verónica Andrea Junco Trejos",
        "Raúl Mateo Vanegas",
        "Ingrid Tatiana Linares Anzola",
        "Daniel Alejandro Sánchez González"
    ]
}

# ============================================================
# INICIALIZAR VARIABLES DE SESIÓN
# ============================================================

if "cultivo_seleccionado" not in st.session_state:
    st.session_state["cultivo_seleccionado"] = None

if "estudiante_seleccionado" not in st.session_state:
    st.session_state["estudiante_seleccionado"] = None

if "accion_seleccionada" not in st.session_state:
    st.session_state["accion_seleccionada"] = None

if "registro_exitoso" not in st.session_state:
    st.session_state["registro_exitoso"] = False


# ============================================================
# FUNCIÓN PARA CALCULAR DISTANCIA
# ============================================================

def calcular_distancia(latitud, longitud):

    R = 6371000  # Radio de la Tierra en metros

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
# SELECCIÓN DEL CULTIVO
# ============================================================

if st.session_state["cultivo_seleccionado"] is None:

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

                    st.session_state["cultivo_seleccionado"] = cultivo

                    st.rerun()

        else:

            with col2:

                if st.button(
                    cultivo,
                    use_container_width=True,
                    key=f"cultivo_{i}"
                ):

                    st.session_state["cultivo_seleccionado"] = cultivo

                    st.rerun()


# ============================================================
# PANTALLA 2
# SELECCIÓN DEL ESTUDIANTE
# ============================================================

elif st.session_state["estudiante_seleccionado"] is None:

    cultivo = st.session_state["cultivo_seleccionado"]

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

            st.session_state["estudiante_seleccionado"] = estudiante

            st.rerun()


    st.markdown("---")

    if st.button(
        "⬅️ Cambiar de cultivo",
        use_container_width=True
    ):

        st.session_state["cultivo_seleccionado"] = None

        st.rerun()


# ============================================================
# PANTALLA 3
# ESTUDIANTE + ENTRADA / SALIDA
# ============================================================

else:

    cultivo = st.session_state["cultivo_seleccionado"]

    estudiante = st.session_state["estudiante_seleccionado"]


    # --------------------------------------------------------
    # INFORMACIÓN DEL ESTUDIANTE
    # --------------------------------------------------------

    st.subheader(
        f"👤 {estudiante}"
    )

    st.write(
        f"🌱 Cultivo: {cultivo}"
    )

    st.markdown("---")


    # ========================================================
    # SI TODAVÍA NO SE HA PULSADO ENTRAR O SALIR
    # ========================================================

    if st.session_state["accion_seleccionada"] is None:

        st.write(
            "Seleccione la acción que desea registrar:"
        )

        st.markdown("")


        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # BOTÓN ENTRAR
        # ----------------------------------------------------

        with col1:

            if st.button(
                "🟢 ENTRAR",
                use_container_width=True
            ):

                st.session_state["accion_seleccionada"] = "Entrada"

                st.rerun()


        # ----------------------------------------------------
        # BOTÓN SALIR
        # ----------------------------------------------------

        with col2:

            if st.button(
                "🔴 SALIR",
                use_container_width=True
            ):

                st.session_state["accion_seleccionada"] = "Salida"

                st.rerun()


    # ========================================================
    # OBTENER UBICACIÓN DESPUÉS DEL CLIC
    # ========================================================

    else:

        accion = st.session_state["accion_seleccionada"]


        if accion == "Entrada":

            st.subheader(
                "🟢 Registrando entrada"
            )

        else:

            st.subheader(
                "🔴 Registrando salida"
            )


        st.info(
            "📍 Verificando su ubicación..."
        )


        # ----------------------------------------------------
        # SOLICITAR UBICACIÓN AL NAVEGADOR
        # ----------------------------------------------------

        ubicacion = streamlit_geolocation()


        # ====================================================
        # SI SE OBTUVO LA UBICACIÓN
        # ====================================================

        if ubicacion["latitude"] is not None:

            latitud_actual = ubicacion["latitude"]

            longitud_actual = ubicacion["longitude"]


            # ------------------------------------------------
            # CALCULAR DISTANCIA
            # ------------------------------------------------

            distancia = calcular_distancia(
                latitud_actual,
                longitud_actual
            )


            # ------------------------------------------------
            # MOSTRAR DISTANCIA
            # ------------------------------------------------

            st.metric(
                "Distancia al CAM",
                f"{distancia:.1f} metros"
            )


            # =================================================
            # UBICACIÓN DENTRO DEL RADIO
            # =================================================

            if distancia <= RADIO_PERMITIDO:

                # Obtener fecha y hora actual
                fecha_hora = datetime.now()

                fecha = fecha_hora.strftime(
                    "%d/%m/%Y"
                )

                hora = fecha_hora.strftime(
                    "%H:%M:%S"
                )


                st.success(
                    "🟢 Ubicación autorizada"
                )


                st.success(
                    f"✅ {accion} registrada correctamente"
                )


                st.write(
                    f"👤 **Estudiante:** {estudiante}"
                )

                st.write(
                    f"🌱 **Cultivo:** {cultivo}"
                )

                st.write(
                    f"📅 **Fecha:** {fecha}"
                )

                st.write(
                    f"⏰ **Hora:** {hora}"
                )


                # Guardar temporalmente el registro
                st.session_state["registro_exitoso"] = True


            # =================================================
            # UBICACIÓN FUERA DEL RADIO
            # =================================================

            else:

                st.error(
                    "🔴 Ubicación no autorizada"
                )

                st.write(
                    f"Se encuentra a "
                    f"**{distancia:.1f} metros** "
                    f"del punto autorizado."
                )

                st.write(
                    f"Debe encontrarse a menos de "
                    f"**{RADIO_PERMITIDO} metros** "
                    f"para registrar la asistencia."
                )


        # ====================================================
        # NO SE OBTUVO UBICACIÓN
        # ====================================================

        else:

            st.warning(
                "⚠️ No fue posible obtener su ubicación."
            )

            st.write(
                "Asegúrese de haber permitido el acceso "
                "a la ubicación en su navegador."
            )


    # ========================================================
    # VOLVER A LISTA DE ESTUDIANTES
    # ========================================================

    st.markdown("---")

    if st.button(
        "⬅️ Volver a lista de estudiantes",
        use_container_width=True
    ):

        st.session_state["estudiante_seleccionado"] = None

        st.session_state["accion_seleccionada"] = None

        st.session_state["registro_exitoso"] = False

        st.rerun()