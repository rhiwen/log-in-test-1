import streamlit as st

# Verificar autenticación
if not st.session_state.get("authenticated", False):
    st.warning("Por favor inicie sesión para acceder a esta página")
    st.stop()

st.title("Opciones")
st.write(f"Usuario: {st.session_state.username}")
st.write(f"Rol: {st.session_state.role}")

st.subheader("Configuración de SPS Alarmas")
st.write("Aquí puede cambiar sus preferencias de usuario")