import streamlit as st


def ocultar_sidebar():
    """Oculta el panel izquierdo de navegación multipágina."""

    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="collapsedControl"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)