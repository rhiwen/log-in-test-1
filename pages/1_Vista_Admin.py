import streamlit as st

# Verificar autenticación
if not st.session_state.get("authenticated", False):
    st.warning("Por favor inicie sesión para acceder a esta página")
    st.stop()

# Verificar rol
if st.session_state.role != "admin":
    st.error("No tiene permisos para acceder a esta página")
    st.stop()

st.title("Panel de Administración")
st.write("Esta página solo es visible para administradores")

st.subheader("Gestión de Leads - SPS Alarmas")
st.write("Aquí puede gestionar todos los leads de la empresa")