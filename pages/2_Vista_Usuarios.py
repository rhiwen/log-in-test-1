import streamlit as st

# Verificar autenticación
if not st.session_state.get("authenticated", False):
    st.warning("Por favor inicie sesión para acceder a esta página")
    st.stop()

st.title("Panel de Usuario")
st.write(f"Bienvenido {st.session_state.username}")

st.subheader("Mis Leads Asignados - SPS Alarmas")
st.write("Aquí puede ver los leads que tiene asignados")