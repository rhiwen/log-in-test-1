import streamlit as st
import pandas as pd
import sys
import os

# Verificar autenticación
if not st.session_state.get("authenticated", False):
    st.warning("Debes iniciar sesión primero")
    st.switch_page("streamlit_app.py")
    st.stop()

# Verificar rol
if st.session_state.get("role") != "admin":
    st.warning("No tienes permiso para ver esta página")
    st.switch_page("streamlit_app.py")
    st.stop()

# Importar función de navegación
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from streamlit_app import show_navigation

# Configuración de la página
st.set_page_config(
    page_title="Panel de Administración",
    page_icon="⚙️",
    initial_sidebar_state="collapsed"
)

# Mostrar navegación
show_navigation()

# Contenido principal
st.title("⚙️ Panel de Administración")
st.write(f"Bienvenido al panel de administración, {st.session_state.username}")

# Inicializar variables de estado si no existen
if "show_add_user" not in st.session_state:
    st.session_state.show_add_user = False
if "show_delete_user" not in st.session_state:
    st.session_state.show_delete_user = False

# Tabs para organizar contenido
tab1, tab2, tab3 = st.tabs(["Gestión de Usuarios", "Estadísticas", "Configuración"])

with tab1:
    st.header("Gestión de Usuarios")
    
    # Datos de ejemplo para la tabla de usuarios
    users_data = {
        "Usuario": ["user1", "user2", "admin1", "user3"],
        "Rol": ["usuario", "usuario", "admin", "usuario"],
        "Última Conexión": ["2023-04-01", "2023-04-02", "2023-04-03", "2023-04-01"],
        "Estado": ["Activo", "Inactivo", "Activo", "Activo"]
    }
    
    df = pd.DataFrame(users_data)
    st.dataframe(df, use_container_width=True)
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Añadir Usuario", key="add_user"):
            st.session_state.show_add_user = True
            st.session_state.show_delete_user = False
    with col2:
        if st.button("Eliminar Usuario", key="delete_user"):
            st.session_state.show_delete_user = True
            st.session_state.show_add_user = False
    with col3:
        if st.button("Editar Permisos", key="edit_perms"):
            st.info("Funcionalidad en desarrollo")
    
    # Formulario para añadir usuario
    if st.session_state.show_add_user:
        st.subheader("Añadir Nuevo Usuario")
        with st.form("add_user_form"):
            new_username = st.text_input("Nombre de Usuario")
            new_password = st.text_input("Contraseña", type="password")
            new_role = st.selectbox("Rol", ["usuario", "admin"])
            
            submit_button = st.form_submit_button("Guardar Usuario")
            if submit_button:
                if new_username and new_password:
                    st.success(f"Usuario {new_username} creado exitosamente")
                    st.session_state.show_add_user = False
                else:
                    st.error("Por favor complete todos los campos")
    
    # Formulario para eliminar usuario
    if st.session_state.show_delete_user:
        st.subheader("Eliminar Usuario")
        user_to_delete = st.selectbox("Seleccione usuario a eliminar", users_data["Usuario"])
        if st.button("Confirmar Eliminación", key="confirm_delete"):
            st.success(f"Usuario {user_to_delete} eliminado correctamente")
            st.session_state.show_delete_user = False

with tab2:
    st.header("Estadísticas del Sistema")
    
    # Métricas generales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Usuarios Activos", value="18", delta="2")
    with col2:
        st.metric(label="Documentos Totales", value="142", delta="7")
    with col3:
        st.metric(label="Espacio Usado", value="4.2 GB", delta="-0.3 GB")
    
    # Gráfico de actividad
    st.subheader("Actividad del Sistema")
    
    # Datos de ejemplo para los gráficos
    chart_data = pd.DataFrame({
        "Fecha": ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"],
        "Logins": [12, 19, 15, 21, 17, 8, 5],
        "Documentos Creados": [5, 12, 8, 14, 10, 3, 2]
    }).set_index("Fecha")
    
    # Mostrar gráfico de barras
    st.bar_chart(chart_data, use_container_width=True)
    
    # Mostrar distribución de usuarios
    st.subheader("Distribución de Usuarios por Rol")
    role_data = pd.DataFrame({
        "Rol": ["Admin", "Usuario"],
        "Cantidad": [2, 16]
    }).set_index("Rol")
    
    st.bar_chart(role_data, use_container_width=True)

with tab3:
    st.header("Configuración del Sistema")
    
    # Sección de backups
    st.subheader("Gestión de Backups")
    backup_col1, backup_col2 = st.columns(2)
    
    with backup_col1:
        st.selectbox("Frecuencia de backup", ["Diario", "Semanal", "Mensual"])
    with backup_col2:
        if st.button("Ejecutar Backup Manual"):
            st.success("Backup iniciado correctamente")
    
    # Sección de logs
    st.subheader("Logs del Sistema")
    log_level = st.select_slider(
        "Nivel de logs", 
        options=["Error", "Warning", "Info", "Debug", "Verbose"]
    )
    
    st.text_area("Últimos logs", 
                 value="2023-04-03 15:42:23 [INFO] Usuario admin1 ha iniciado sesión\n"
                       "2023-04-03 15:40:12 [WARNING] Intento fallido de login para usuario unknown\n"
                       "2023-04-03 15:35:45 [INFO] Backup automático completado\n"
                       "2023-04-03 14:22:10 [ERROR] Error al conectar con el servicio externo",
                 height=200)
    
    # Sección de mantenimiento
    st.subheader("Mantenimiento")
    maint_col1, maint_col2 = st.columns(2)
    
    with maint_col1:
        if st.button("Limpiar Caché"):
            st.success("Caché limpiada correctamente")
    with maint_col2:
        if st.button("Verificar Integridad"):
            st.success("Sistema verificado: Todo en orden")