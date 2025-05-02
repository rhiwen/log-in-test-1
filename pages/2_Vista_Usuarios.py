import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

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
    page_title="Vista de Usuarios",
    page_icon="📄",
    initial_sidebar_state="collapsed"
)

# Mostrar navegación
show_navigation()

# Contenido principal
st.title("📄 Vista de Usuarios")
st.write(f"Bienvenido a la vista de usuarios, {st.session_state.username}")

# Inicializar variables de sesión si no existen
if "current_doc" not in st.session_state:
    st.session_state.current_doc = None
if "editing_doc" not in st.session_state:
    st.session_state.editing_doc = False

# Datos de ejemplo para los documentos
docs = [
    {
        "id": 1,
        "nombre": "Informe mensual",
        "fecha": "2023-03-15",
        "estado": "Completado",
        "contenido": "Este es el contenido del informe mensual. Incluye métricas y análisis del rendimiento durante el mes de marzo."
    },
    {
        "id": 2,
        "nombre": "Presupuesto Q2",
        "fecha": "2023-04-01",
        "estado": "En progreso",
        "contenido": "Presupuesto para el segundo trimestre. Incluye proyecciones de gastos e ingresos para abril, mayo y junio."
    },
    {
        "id": 3,
        "nombre": "Plan estratégico",
        "fecha": "2023-02-28",
        "estado": "Pendiente revisión",
        "contenido": "Plan estratégico para el año fiscal. Incluye objetivos, metas y acciones clave para los próximos 12 meses."
    }
]

# Tabs para organizar el contenido
tab1, tab2 = st.tabs(["Mis Documentos", "Subir Nuevo Documento"])

with tab1:
    st.header("Mis Documentos")
    
    # Vista de lista de documentos
    for doc in docs:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{doc['nombre']}** - {doc['fecha']} ({doc['estado']})")
        
        with col2:
            if st.button("Ver", key=f"view_{doc['id']}"):
                st.session_state.current_doc = doc
                st.session_state.editing_doc = False
        
        with col3:
            if st.button("Editar", key=f"edit_{doc['id']}"):
                st.session_state.current_doc = doc
                st.session_state.editing_doc = True
    
    st.divider()
    
    # Vista detallada del documento seleccionado
    if st.session_state.current_doc:
        doc = st.session_state.current_doc
        
        # Mostrar detalles del documento
        st.subheader(doc['nombre'])
        st.write(f"**Fecha:** {doc['fecha']} | **Estado:** {doc['estado']}")
        
        if st.session_state.editing_doc:
            # Formulario de edición
            with st.form(key=f"edit_form_{doc['id']}"):
                nuevo_nombre = st.text_input("Nombre", value=doc['nombre'])
                nuevo_estado = st.selectbox("Estado", 
                                           ["Completado", "En progreso", "Pendiente revisión"],
                                           ["Completado", "En progreso", "Pendiente revisión"].index(doc['estado']))
                nuevo_contenido = st.text_area("Contenido", value=doc['contenido'], height=200)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Guardar Cambios"):
                        # Aquí se implementaría la lógica para guardar los cambios
                        st.success("Cambios guardados correctamente")
                        st.session_state.editing_doc = False
                with col2:
                    if st.form_submit_button("Cancelar"):
                        st.session_state.editing_doc = False
        else:
            # Vista de documento
            st.write(doc['contenido'])
            
            # Opciones adicionales
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Descargar", key=f"download_{doc['id']}"):
                    st.success(f"Descargando {doc['nombre']}...")
            with col2:
                if st.button("Compartir", key=f"share_{doc['id']}"):
                    st.info("Opción de compartir en desarrollo")
            with col3:
                if st.button("Historial", key=f"history_{doc['id']}"):
                    st.info("Historial de versiones en desarrollo")

with tab2:
    st.header("Subir Nuevo Documento")
    
    # Formulario para subir documento
    with st.form("upload_form"):
        doc_name = st.text_input("Nombre del documento")
        doc_type = st.selectbox("Tipo de documento", ["Informe", "Presupuesto", "Plan", "Otro"])
        
        col1, col2 = st.columns(2)
        with col1:
            doc_estado = st.selectbox("Estado", ["Completado", "En progreso", "Pendiente revisión"])
        with col2:
            doc_fecha = st.date_input("Fecha", datetime.now())
        
        doc_content = st.text_area("Contenido", height=200)
        file_uploader = st.file_uploader("Adjuntar archivo (opcional)", type=["pdf", "docx", "xlsx"])
        
        submitted = st.form_submit_button("Subir Documento")
        if submitted:
            if doc_name and doc_content:
                st.success(f"¡Documento '{doc_name}' subido correctamente!")
                # Aquí se implementaría la lógica para guardar el documento
            else:
                st.error("Por favor completa los campos requeridos")

    # Consejos útiles
    with st.expander("Consejos para documentos"):
        st.write("""
        **Consejos para crear documentos efectivos:**
        
        - Utiliza títulos claros y descriptivos
        - Incluye la fecha y el estado del documento
        - Organiza el contenido en secciones
        - Revisa ortografía y gramática antes de finalizar
        """)