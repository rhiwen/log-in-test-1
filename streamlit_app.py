import streamlit as st
import hmac

# Inicializar estado de sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None

# Ocultar la navegación predeterminada
st.set_page_config(initial_sidebar_state="collapsed")

# Registrar las páginas para que st.page_link funcione correctamente
if "authenticated" in st.session_state and st.session_state.authenticated:
    pages = [
        st.Page("streamlit_app.py", title="Inicio"),
        st.Page("pages/2_Vista_Usuarios.py", title="Vista de Usuarios"),
        st.Page("pages/1_Vista_Admin.py", title="Panel de Administración"),
        st.Page("pages/settings.py", title="Configuración")
    ]
    st.navigation(pages, position="hidden")

def show_navigation():
    with st.sidebar:
        st.page_link(st.Page("streamlit_app.py"), label="Inicio")
        
        # Páginas para todos los usuarios
        st.page_link(st.Page("pages/2_Vista_Usuarios.py"), label="Vista de Usuarios")
        
        # Páginas solo para administradores
        if st.session_state.role == "admin":
            st.page_link(st.Page("pages/1_Vista_Admin.py"), label="Panel de Administración")
        
        st.page_link(st.Page("pages/settings.py"), label="Configuración")
        
        # Botón de cierre de sesión en la barra lateral
        if st.button("Cerrar sesión"):
            st.session_state.authenticated = False
            st.session_state.role = None
            st.rerun()

def login():
    st.title("Login")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        # Verificar credenciales desde secrets.toml
        if username in st.secrets["users"]:
            stored_password = st.secrets["users"][username]["password"]
            if hmac.compare_digest(password, stored_password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = st.secrets["users"][username]["role"]
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        else:
            st.error("Usuario no encontrado")

def main_content():
    st.title(f"Bienvenido, {st.session_state.username}")
    st.write(f"Tu rol es: {st.session_state.role}")
    
    # Mostrar opciones según el rol
    if st.session_state.role == "admin":
        st.write("Tienes acceso a todas las páginas")
    elif st.session_state.role == "usuario":
        st.write("Tienes acceso limitado")

# Control de flujo principal
if st.session_state.authenticated:
    show_navigation()  # Mostrar navegación
    main_content()     # Mostrar contenido principal
else:
    login()