import streamlit as st
import requests
import streamlit.components.v1 as components
import json
import time


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Asistencia CAM",
    page_icon="📋",
    layout="centered"
)


# ============================================================
# URL DE GOOGLE APPS SCRIPT
# ============================================================

APPS_SCRIPT_URL = (
    "https://script.google.com/a/macros/unal.edu.co/s/"
    "AKfycbxYBU1HUeNZgaLb9eZtnWEf8XkBKi9bikF7jvvIWGEBJY6gzjX1ddZdvDCHCHFNU7Tq/exec"
)


# ============================================================
# OBTENER DEVICE ID PERSISTENTE
# ============================================================

def obtener_device_id():

    componente = components.html(
        """
        <script>

        const STORAGE_KEY = "asistencia_cam_device_id";

        let deviceId = localStorage.getItem(STORAGE_KEY);

        if (!deviceId) {

            deviceId =
                crypto.randomUUID();

            localStorage.setItem(
                STORAGE_KEY,
                deviceId
            );

        }

        document.write(
            '<div id="device_id">' +
            deviceId +
            '</div>'
        );

        </script>
        """,
        height=0
    )

    return componente


# ============================================================
# COMUNICACIÓN CON APPS SCRIPT
# ============================================================

def enviar_apps_script(datos):

    try:

        respuesta = requests.post(
            APPS_SCRIPT_URL,
            json=datos,
            timeout=30
        )

        respuesta.raise_for_status()

        return respuesta.json()

    except Exception as e:

        return {
            "ok": False,
            "mensaje": str(e)
        }


# ============================================================
# INICIO
# ============================================================

st.title("📋 Registro de asistencia")


# ============================================================
# AUTENTICACIÓN GOOGLE
# ============================================================

if not st.user.is_logged_in:

    st.info(
        "Inicie sesión con su correo institucional "
        "para registrar su asistencia."
    )

    if st.button(
        "🔐 Iniciar sesión con Google",
        use_container_width=True
    ):

        st.login("google")

    st.stop()


# ============================================================
# DATOS DE GOOGLE
# ============================================================

correo = st.user.email.lower().strip()

nombre_google = st.user.name

sub_google = st.user.sub


# ============================================================
# VALIDAR DOMINIO
# ============================================================

if not correo.endswith("@unal.edu.co"):

    st.error(
        "❌ Debe utilizar un correo institucional "
        "@unal.edu.co."
    )

    if st.button("Cerrar sesión"):

        st.logout()

    st.stop()


# ============================================================
# DEVICE ID
# ============================================================

device_id = obtener_device_id()


# ============================================================
# CONSULTAR ESTUDIANTE
# ============================================================

if "estudiante" not in st.session_state:

    with st.spinner(
        "Verificando estudiante..."
    ):

        resultado = enviar_apps_script({

            "accion":
                "consultar_estudiante",

            "correo":
                correo

        })


    if not resultado.get("ok"):

        st.error(
            resultado.get(
                "mensaje",
                "Error consultando estudiante."
            )
        )

        st.stop()


    if not resultado.get("encontrado"):

        st.error(
            "❌ Su correo institucional "
            "no aparece en la lista de estudiantes."
        )

        st.write(
            f"Correo detectado: {correo}"
        )

        if st.button("Cerrar sesión"):

            st.logout()

        st.stop()


    st.session_state.estudiante = {

        "nombre":
            resultado.get(
                "nombre"
            ),

        "cultivo":
            resultado.get(
                "cultivo"
            )

    }


# ============================================================
# DATOS DEL ESTUDIANTE
# ============================================================

estudiante = (
    st.session_state.estudiante
)

nombre = estudiante["nombre"]

cultivo = estudiante["cultivo"]


# ============================================================
# BIENVENIDA
# ============================================================

st.success(
    f"👋 Bienvenido, {nombre}"
)

st.write(
    f"🌱 Cultivo: **{cultivo}**"
)

st.write(
    f"📧 Correo: **{correo}**"
)


# ============================================================
# CONSULTAR BLOQUEO
# ============================================================

if "bloqueo" not in st.session_state:

    with st.spinner(
        "Verificando disponibilidad..."
    ):

        bloqueo = enviar_apps_script({

            "accion":
                "consultar_bloqueo",

            "device_id":
                device_id

        })


    st.session_state.bloqueo = bloqueo


bloqueo = st.session_state.bloqueo


# ============================================================
# DISPOSITIVO BLOQUEADO
# ============================================================

if bloqueo.get("bloqueado"):

    st.warning(
        "🔒 Este dispositivo está temporalmente "
        "bloqueado para registrar asistencia."
    )

    if bloqueo.get("bloqueo_hasta"):

        st.info(
            "Puede volver a registrar asistencia después de:"
        )

        st.write(
            bloqueo.get(
                "bloqueo_hasta"
            )
        )

    st.stop()


# ============================================================
# REGISTRO
# ============================================================

st.markdown("---")

st.subheader(
    "Registrar asistencia"
)


# ============================================================
# FUNCIÓN REGISTRO
# ============================================================

def registrar(tipo):

    with st.spinner(
        "Registrando..."
    ):

        resultado = enviar_apps_script({

            "accion":
                "registrar_asistencia",

            "correo":
                correo,

            "nombre":
                nombre,

            "cultivo":
                cultivo,

            "sub":
                sub_google,

            "device_id":
                device_id,

            "tipo":
                tipo

        })


    if resultado.get("ok"):

        st.success(
            "✅ Registro realizado correctamente."
        )

        if resultado.get(
            "bloqueo_hasta"
        ):

            st.info(
                "🔒 El dispositivo queda bloqueado "
                "hasta:"
            )

            st.write(
                resultado[
                    "bloqueo_hasta"
                ]
            )

        st.session_state.bloqueo = {

            "bloqueado":
                True,

            "bloqueo_hasta":
                resultado.get(
                    "bloqueo_hasta"
                )

        }

        time.sleep(2)

        st.rerun()


    else:

        st.error(
            resultado.get(
                "mensaje",
                "No fue posible registrar."
            )
        )


# ============================================================
# BOTONES
# ============================================================

col1, col2 = st.columns(2)


with col1:

    if st.button(
        "🟢 ENTRAR",
        use_container_width=True,
        type="primary"
    ):

        registrar(
            "ENTRADA"
        )


with col2:

    if st.button(
        "🔴 SALIR",
        use_container_width=True
    ):

        registrar(
            "SALIDA"
        )


# ============================================================
# CERRAR SESIÓN
# ============================================================

st.markdown("---")

if st.button(
    "Cerrar sesión",
    use_container_width=True
):

    st.session_state.clear()

    st.logout()