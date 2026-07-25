import streamlit as st

st.set_page_config(
    page_title="Prueba Login",
    page_icon="🔐"
)

st.title("🔐 Prueba de inicio de sesión")

if not st.user.is_logged_in:
    st.write("Inicie sesión para continuar.")

    if st.button("🔐 Iniciar sesión con Google"):
        st.login("google")

else:
    st.success("¡Inicio de sesión exitoso!")

    st.write("### Información del usuario")

    st.write("Nombre:", st.user.name)
    st.write("Correo:", st.user.email)

    st.write("Información completa:")

    st.json(st.user.to_dict())

    if st.button("Cerrar sesión"):
        st.logout()