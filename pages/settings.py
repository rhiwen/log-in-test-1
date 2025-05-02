import streamlit as st
import sys
import os

# Verificar autenticación
if not st.session_state.get("authenticated", False):
    st.warning("Debes iniciar sesión primero")
    st.switch_page("streamlit_app.py")
    st.stop()

# Importar función de navegación
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamlit_app import show_navigation

# Configuración de la página
st.set_page_config(
    page_title="Configuración",
    page_icon="🔧",
    initial_sidebar_state="collapsed"
)

# Mostrar navegación
show_navigation()

# Contenido principal
st.title("🔧 Configuración")
st.write(f"Configuración de cuenta para {st.session_state.username}")

# Inicializar valores en el estado de la sesión si no existen
if "theme" not in st.session_state:
    st.session_state.theme = "Claro"
if "notifications" not in st.session_state:
    st.session_state.notifications = True
if "language" not in st.session_state:
    st.session_state.language = "Español"

# Usar pestañas para organizar la configuración
tab1, tab2, tab3, tab4 = st.tabs(["Perfil", "Apariencia", "Notificaciones", "Seguridad"])

with tab1:
    st.header("Perfil de Usuario")
    
    # Información de perfil
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre", value="Usuario Demo")
        with col2:
            email = st.text_input("Correo Electrónico", value="usuario@ejemplo.com")
        
        biografia = st.text_area("Biografía", value="Esta es una biografía de ejemplo para el perfil de usuario.")
        
        # Configuración de idioma
        st.subheader("Idioma y Región")
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.language = st.selectbox(
                "Idioma",
                options=["Español", "English", "Français", "Deutsch"],
                index=["Español", "English", "Français", "Deutsch"].index(st.session_state.language)
            )
        with col2:
            timezone = st.selectbox(
                "Zona horaria",
                options=["(GMT-03:00) Buenos Aires", "(GMT-05:00) Ciudad de México", "(GMT+01:00) Madrid", "(GMT+00:00) UTC"]
            )
        
        if st.form_submit_button("Actualizar Perfil"):
            st.success("¡Perfil actualizado correctamente!")

with tab2:
    st.header("Apariencia")
    
    st.subheader("Tema de la Aplicación")
    st.session_state.theme = st.radio(
        "Selecciona un tema",
        options=["Claro", "Oscuro", "Sistema"],
        index=["Claro", "Oscuro", "Sistema"].index(st.session_state.theme),
        horizontal=True
    )
    
    st.write(f"Tema seleccionado: **{st.session_state.theme}**")
    
    st.subheader("Personalización")
    col1, col2 = st.columns(2)
    with col1:
        compact_mode = st.toggle("Modo compacto", value=False)
    with col2:
        high_contrast = st.toggle("Alto contraste", value=False)
    
    font_size = st.slider("Tamaño de fuente", min_value=12, max_value=20, value=14)
    
    if st.button("Guardar Preferencias de Apariencia"):
        st.success("Preferencias de apariencia guardadas")

with tab3:
    st.header("Notificaciones")
    
    st.session_state.notifications = st.toggle(
        "Activar notificaciones", 
        value=st.session_state.notifications
    )
    
    if st.session_state.notifications:
        st.subheader("Canales de Notificación")
        email_notif = st.checkbox("Notificaciones por correo", value=True)
        push_notif = st.checkbox("Notificaciones push", value=False)
        
        st.subheader("Tipos de Notificaciones")
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Actualizaciones del sistema", value=True)
            st.checkbox("Nuevos mensajes", value=True)
        with col2:
            st.checkbox("Eventos", value=False)
            st.checkbox("Recordatorios", value=True)
        
        st.subheader("Frecuencia")
        notif_freq = st.radio(
            "Frecuencia de notificaciones",
            options=["Inmediata", "Diaria", "Semanal"],
            horizontal=True
        )
        
        if st.button("Guardar Preferencias de Notificaciones"):
            st.success("Preferencias de notificaciones guardadas")
    else:
        st.info("Las notificaciones están desactivadas")

with tab4:
    st.header("Seguridad")
    
    st.subheader("Cambiar Contraseña")
    with st.form("change_password"):
        current_password = st.text_input("Contraseña actual", type="password")
        new_password = st.text_input("Nueva contraseña", type="password")
        confirm_password = st.text_input("Confirmar nueva contraseña", type="password")
        
        submitted = st.form_submit_button("Cambiar contraseña")
        if submitted:
            if not current_password or not new_password or not confirm_password:
                st.error("Por favor completa todos los campos")
            elif new_password != confirm_password:
                st.error("Las contraseñas no coinciden")
            else:
                st.success("¡Contraseña actualizada correctamente!")
    
    st.subheader("Sesiones Activas")
    st.info("Sesión actual: Navegador Web - Iniciada hace 10 minutos")
    
    if st.button("Cerrar todas las sesiones"):
        st.success("Todas las sesiones han sido cerradas excepto la actual")
    
    # Opciones adicionales de seguridad
    st.subheader("Opciones Adicionales")
    two_factor = st.toggle("Autenticación de dos factores", value=False)
    
    if two_factor:
        st.info("La autenticación de dos factores está en desarrollo")

# Sección de opciones avanzadas (solo para administradores)
if st.session_state.role == "admin":
    st.divider()
    st.header("Opciones Avanzadas (Admin)")
    
    with st.expander("Configuración del Sistema"):
        st.subheader("Opciones de Depuración")
        debug_mode = st.toggle("Modo de depuración", value=False)
        logs_level = st.select_slider(
            "Nivel de logs", 
            options=["Error", "Warning", "Info", "Debug", "Verbose"]
        )
        
        st.subheader("Backup de Datos")
        backup_freq = st.selectbox(
            "Frecuencia de backup",
            options=["Diario", "Semanal", "Mensual"]
        )
        
        if st.button("Ejecutar backup manual"):
            st.success("Backup iniciado correctamente. Recibirás una notificación cuando finalice.")