import streamlit as st

st.set_page_config(
    page_title="GeoVisor CAM",
    page_icon="🌱",
    layout="wide"
)

from core.ui_engine import ocultar_sidebar

ocultar_sidebar()

st.title("🌱CAM🌱")

st.write("""
Querid@ estudiante de Ciclo II, bienvenido al Centro Agropecuario Marengo.

Seleccione un módulo.
""")

st.markdown("---")

st.subheader("Módulos disponibles")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌿 Plantas Arvenses", use_container_width=True):
        st.switch_page("pages/Malezas.py")

with col2:
    if st.button("🌱 Aptitud y Tipo de Suelo", use_container_width=True):
        st.switch_page("pages/Aptitud.py")

with col3:
    if st.button("📋 Asistencia", use_container_width=True):
        st.switch_page("pages/Asistencia.py")