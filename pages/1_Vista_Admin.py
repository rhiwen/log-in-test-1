import streamlit as st
import sys
import os

# Verificar autenticación
if not st.session_state.get("authenticated", False):
    st.warning("Debes iniciar sesión primero")
    st.switch_page("streamlit_app.py")
    st.stop()

# Verificar rol
if st.session_state.role != "admin":
    st.warning("No tienes permiso para ver esta página")
    st.switch_page("streamlit_app.py")
    st.stop()

# Importar la función de navegación desde el archivo principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamlit_app import show_navigation

# Registrar las páginas para que st.page_link funcione correctamente
pages = [
    st.Page("streamlit_app.py", title="Inicio"),
    st.Page("pages/2_Vista_Usuarios.py", title="Vista de Usuarios"),
    st.Page("pages/1_Vista_Admin.py", title="Panel de Administración"),
    st.Page("pages/settings.py", title="Configuración")
]
st.navigation(pages, position="hidden")

# Mostrar navegación
show_navigation()

# Contenido de la página
st.title("Panel de Administración")
st.write(f"Bienvenido al panel de administración, {st.session_state.username}")

# Aquí va el contenido específico de la página de administración