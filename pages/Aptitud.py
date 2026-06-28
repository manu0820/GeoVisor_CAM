import streamlit as st

from core.data_engine import (
    cargar_datos,
    obtener_centro,
    obtener_fragmentos,
    obtener_fragmento_por_click,
    traducir_codigo,
)

from core.map_engine import (
    crear_mapa,
    agregar_suelos,
    agregar_aptitud,
    agregar_perimetro,
    agregar_lotes,
    agregar_fragmentos,
    mostrar_mapa,
)

from config import COL_CULTIVOS

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="GeoVisor CAM",
    layout="wide"
)

from core.ui_engine import ocultar_sidebar

ocultar_sidebar()

st.title("🌱 GeoVisor CAM - Aptitud y Tipo de Suelo")

if st.button("⬅ Volver al inicio"):
    st.switch_page("app.py")

# =====================================================
# SESSION STATE
# =====================================================

if "fragmento" not in st.session_state:
    st.session_state.fragmento = None

if "vista_cultivos" not in st.session_state:
    st.session_state.vista_cultivos = False

# =====================================================
# CARGAR DATOS
# =====================================================

datos = cargar_datos()

lotes = datos["lotes"]
perimetro = datos["perimetro"]
suelos = datos["suelos"]
aptitud = datos["aptitud"]

fragmentos = obtener_fragmentos()

# =====================================================
# MAPA
# =====================================================

centro = obtener_centro(lotes)

m = crear_mapa(centro)

agregar_suelos(m, suelos)
agregar_aptitud(m, aptitud)
agregar_perimetro(m, perimetro)
agregar_lotes(m, lotes)
agregar_fragmentos(m, fragmentos)

# =====================================================
# LAYOUT
# =====================================================

colMapa, colPanel = st.columns([4, 1])

with colMapa:
    evento = mostrar_mapa(m)

# =====================================================
# IDENTIFICAR FRAGMENTO
# =====================================================

if evento and evento.get("last_clicked"):

    lat = evento["last_clicked"]["lat"]
    lon = evento["last_clicked"]["lng"]

    resultado = obtener_fragmento_por_click(fragmentos, lat, lon)

    if resultado is not None:

        idx, _ = resultado

        if st.session_state.fragmento != idx:
            st.session_state.fragmento = idx
            st.session_state.vista_cultivos = False

# =====================================================
# PANEL DERECHO
# =====================================================

with colPanel:

    if st.session_state.fragmento is None:

        st.header("🌱 Aptitud")
        st.info("Haz clic sobre un fragmento del mapa.")

    else:

        fragmento = fragmentos.loc[st.session_state.fragmento]

        # ===========================================
        # VISTA: CULTIVOS
        # ===========================================
        if st.session_state.vista_cultivos:

            if st.button("⬅ Volver"):
                st.session_state.vista_cultivos = False
                st.rerun()

            st.caption(f"📍 {fragmento['Nombre']} · {fragmento['UT_Aptitud']}")
            st.markdown("### 🌱 Tipos de utilización de la tierra (TUT)")

            filas_html = ""

            for cultivo in COL_CULTIVOS:

                valor = str(fragmento[cultivo])
                traduccion = traducir_codigo(valor)

                if traduccion:
                    celda = (
                        f"<td title='{traduccion}' "
                        "style='padding:5px 0;font-weight:700;"
                        "border-bottom:1px dotted #999;cursor:help;'>"
                        f"{valor}</td>"
                    )
                else:
                    celda = f"<td style='padding:5px 0;color:#999;'>{valor}</td>"

                filas_html += (
                    "<tr style='border-bottom:1px solid #eee;'>"
                    f"<td style='padding:5px 10px 5px 0;'>{cultivo}</td>"
                    f"{celda}</tr>"
                )

            tabla_html = (
                "<table style='width:100%;border-collapse:collapse;font-size:13px;'>"
                f"{filas_html}</table>"
            )

            st.markdown(tabla_html, unsafe_allow_html=True)
            st.caption("Pasa el cursor sobre un código para ver su significado.")

        # ===========================================
        # VISTA: INFO DEL FRAGMENTO
        # ===========================================
        else:

            st.header("🌱 Aptitud")
            st.success(f"📍 {fragmento['Nombre']}")

            st.divider()

            st.markdown(f"**Símbolo del suelo**\n\n{fragmento['Simbolo']}")
            st.markdown(f"**Unidad de tierra**\n\n{fragmento['UT_Aptitud']}")
            st.markdown(
                "**Características principales**\n\n"
                + str(fragmento["Caracteristicas principales"])
            )
            st.markdown(f"**Limitaciones**\n\n{fragmento['Limitaciones']}")

            st.divider()

            if st.button("🌱 Ver cultivos", use_container_width=True):
                st.session_state.vista_cultivos = True
                st.rerun()