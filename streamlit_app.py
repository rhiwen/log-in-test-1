import streamlit as st
import hmac

# Inicializar estado de sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Autenticación", 
    page_icon="🔒",
    initial_sidebar_state="collapsed"
)

# Función para la navegación
def show_navigation():
    with st.sidebar:
        st.title("Navegación")
        st.page_link("streamlit_app.py", label="🏠 Inicio", use_container_width=True)
        st.page_link("pages/2_Vista_Usuarios.py", label="📄 Vista de Usuarios", use_container_width=True)
        
        # Páginas solo para administradores
        if st.session_state.role == "admin":
            st.page_link("pages/1_Vista_Admin.py", label="⚙️ Panel de Administración", use_container_width=True)
        
        st.page_link("pages/settings.py", label="🔧 Configuración", use_container_width=True)
        
        st.divider()
        # Botón de cierre de sesión en la barra lateral
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.role = None
            st.session_state.username = None
            st.rerun()

def login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Ingresar", use_container_width=True)
            
            if submitted:
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
        
        # Información de ayuda
        with st.expander("ℹ️ Información de acceso"):
            st.write("""
            Para acceder al sistema, utiliza las credenciales proporcionadas por tu administrador.
            
            **Usuarios de prueba:**
            - Usuario: user1, Contraseña: user123
            - Usuario: admin1, Contraseña: admin123
            """)

def main_content():
    st.title(f"Bienvenido, {st.session_state.username}")
    
    # Tarjeta de usuario
    user_card = f"""
    <div style="padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px;">
        <h3>Información de Sesión</h3>
        <p><strong>Usuario:</strong> {st.session_state.username}</p>
        <p><strong>Rol:</strong> {st.session_state.role}</p>
        <p><strong>Estado:</strong> Activo</p>
    </div>
    """
    st.markdown(user_card, unsafe_allow_html=True)
    
    # Contenido según el rol
    if st.session_state.role == "admin":
        st.header("Panel de Control")
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Usuarios Totales", value="24", delta="2")
        with col2:
            st.metric(label="Actividad Diaria", value="92%", delta="5%")
        with col3:
            st.metric(label="Solicitudes Pendientes", value="7", delta="-2")
            
        # Acciones rápidas
        st.subheader("Acciones Rápidas")
        action_col1, action_col2, action_col3 = st.columns(3)
        with action_col1:
            st.button("Añadir Usuario", key="add_user_home")
        with action_col2:
            st.button("Generar Informe", key="gen_report_home")
        with action_col3:
            st.button("Revisar Permisos", key="check_perms_home")
            
    elif st.session_state.role == "usuario":
        st.header("Mi Dashboard")
        
        # Notificaciones
        st.info("Tienes 3 notificaciones pendientes")
        
        # Actividad reciente
        st.subheader("Actividad Reciente")
        st.write("• Documento actualizado: Reporte mensual")
        st.write("• Tarea completada: Actualización de perfil")
        st.write("• Comentario añadido: Proyecto principal")
        
        # Próximas tareas
        st.subheader("Próximas Tareas")
        st.checkbox("Completar informe mensual", value=False)
        st.checkbox("Revisar documentación", value=True)
        st.checkbox("Actualizar estado del proyecto", value=False)

# Control de flujo principal
if st.session_state.authenticated:
    show_navigation()  # Mostrar navegación
    main_content()     # Mostrar contenido principal
else:
    login()