import streamlit as st

from core.data_engine import (
    cargar_datos,
    obtener_centro,
    obtener_lote_por_click,
    obtener_malezas_lote,
    obtener_ruta_imagen,
)

from core.map_engine import (
    crear_mapa,
    agregar_lotes,
    agregar_perimetro,
    mostrar_mapa,
)

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="GeoVisor CAM",
    layout="wide"
)

from core.ui_engine import ocultar_sidebar

ocultar_sidebar()

st.markdown("""
<style>
div[class*="st-key-lista_especies"] button {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 2px 0 !important;
    margin: 0 !important;
    text-align: left !important;
    color: #2e7d32 !important;
    font-style: italic !important;
    font-size: 15px !important;
}
div[class*="st-key-lista_especies"] button p {
    font-style: italic !important;
    margin: 0 !important;
}
div[class*="st-key-lista_especies"] button:hover {
    text-decoration: underline !important;
    color: #1b5e20 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🌿 GeoVisor CAM - Plantas Arvenses")

if st.button("⬅ Volver al inicio"):
    st.switch_page("app.py")

# =====================================================
# SESSION STATE
# =====================================================

if "lote" not in st.session_state:
    st.session_state.lote = None

if "especie" not in st.session_state:
    st.session_state.especie = None

# =====================================================
# CARGAR DATOS
# =====================================================

datos = cargar_datos()

lotes = datos["lotes"]
perimetro = datos["perimetro"]
malezas = datos["malezas"]

# =====================================================
# MAPA
# =====================================================

centro = obtener_centro(lotes)

m = crear_mapa(centro)

agregar_lotes(m, lotes)

agregar_perimetro(m, perimetro)

# =====================================================
# LAYOUT
# =====================================================

colMapa, colPanel = st.columns([4,1])

# =====================================================
# MAPA
# =====================================================

with colMapa:

    evento = mostrar_mapa(m)

# =====================================================
# IDENTIFICAR LOTE
# =====================================================

if evento and evento.get("last_clicked"):

    lat = evento["last_clicked"]["lat"]
    lon = evento["last_clicked"]["lng"]

    lote = obtener_lote_por_click(
        lotes,
        lat,
        lon
    )

    if lote is not None:

        # Solo actualiza cuando cambia de lote
        if st.session_state.lote != lote["Nombre"]:

            st.session_state.lote = lote["Nombre"]
            st.session_state.especie = None

# =====================================================
# PANEL DERECHO
# =====================================================

with colPanel:

    # ===========================================
    # SIN LOTE SELECCIONADO
    # ===========================================
    if st.session_state.lote is None:

        st.header("🌿 Plantas Arvenses")
        st.info("Haz clic sobre un lote.")

    else:

        especies = obtener_malezas_lote(
            malezas,
            st.session_state.lote
        )

        # ===========================================
        # VISTA: FICHA DE ESPECIE (ocupa todo el panel)
        # ===========================================
        if st.session_state.especie is not None:

            ficha = next(
                (e for e in especies
                 if e["Nombre Cientifico"] == st.session_state.especie),
                None
            )

            if ficha is None:
                st.session_state.especie = None
                st.rerun()

            if st.button("⬅ Volver"):
                st.session_state.especie = None
                st.rerun()

            st.caption(f"📍 {st.session_state.lote}")

            st.markdown(f"### *{ficha['Nombre Cientifico']}*")

            ruta_imagen = obtener_ruta_imagen(ficha["Nombre Cientifico"])

            if ruta_imagen:
                st.image(str(ruta_imagen), use_container_width=True)

            st.markdown(f"**Nombre común**\n\n{ficha['Nombre Comun']}")
            st.markdown(f"**Descripción**\n\n{ficha['Descripcion']}")
            st.markdown(f"**Datos generales**\n\n{ficha['Datos generales']}")
            st.markdown(
                "**Cultivos donde se reportó**\n\n"
                + str(ficha["Cultivos en los que se reporto"])
            )

        # ===========================================
        # VISTA: LISTA DE ESPECIES DEL LOTE
        # ===========================================
        else:

            st.header("🌿 Plantas Arvenses")
            st.success(f"📍 {st.session_state.lote}")

            st.divider()

            st.markdown("### Especies registradas")

            if len(especies) == 0:

                st.write("No hay especies registradas.")

            else:

                with st.container(key="lista_especies"):

                    for especie in especies:

                        nombre = especie["Nombre Cientifico"]

                        if st.button(
                            nombre,
                            key=f"btn_{nombre}",
                            use_container_width=True
                        ):
                            st.session_state.especie = nombre
                            st.rerun()