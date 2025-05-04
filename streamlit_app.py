import streamlit as st
import hmac

# Inicializar el estado de la sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

def check_password(username, password):
    # Verificar si el usuario existe en secrets.toml
    if username in st.secrets["users"]:
        # Comparar la contraseña de forma segura
        stored_password = st.secrets["users"][username]["password"]
        if hmac.compare_digest(stored_password, password):
            return True
    return False

def login():
    st.title("SPS Alarmas - Sistema de Gestión de Leads")
    
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar Sesión")
        
        if submit:
            if check_password(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = st.secrets["users"][username]["role"]
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()

# Mostrar login o contenido principal
if not st.session_state.authenticated:
    login()
else:
    st.title(f"Bienvenido, {st.session_state.username}")
    st.write(f"Rol: {st.session_state.role}")
    
    if st.button("Cerrar Sesión"):
        logout()