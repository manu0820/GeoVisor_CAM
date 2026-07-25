import streamlit as st
import requests

st.set_page_config(
    page_title="Prueba Asistencia"
)

st.title("Prueba de conexión con Apps Script")

URL = "https://script.google.com/a/macros/unal.edu.co/s/AKfycbxYBU1HUeNZgaLb9eZtnWEf8XkBKi9bikF7jvvIWGEBJY6gzjX1ddZdvDCHCHFNU7Tq/exec"


if st.button("Probar conexión"):

    try:

        respuesta = requests.post(
            URL,
            json={
                "accion": "consultar_estudiante",
                "correo": "mreyesre@unal.edu.co"
            },
            timeout=30
        )

        st.write("Código HTTP:")
        st.write(respuesta.status_code)

        st.write("Respuesta:")
        st.code(respuesta.text)

    except Exception as e:

        st.error(
            f"Error de conexión: {e}"
        )