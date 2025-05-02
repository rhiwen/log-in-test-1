# Aplicación Streamlit con Sistema de Autenticación y Roles

Esta aplicación demuestra cómo implementar un sistema de autenticación y control de acceso basado en roles en Streamlit.

## Características

- Sistema de login nativo sin uso de API
- Control de acceso basado en roles (admin, usuario)
- Páginas protegidas según el rol del usuario
- Gestión segura de credenciales con secrets.toml

## Estructura del Proyecto

```proyecto/
├── .streamlit/ 
│ └── secrets.toml (no incluido en el repositorio) 
├── streamlit_app.py 
├── pages/ 
│ ├── 1_Vista_Admin.py 
│ ├── 2_Vista_Usuarios.py 
│ └── settings.py 
├── README.md 
└── requirements.txt
└── packages.txt
└── .gitignore
```

# Configuración

1. Clonar este repositorio
2. Instalar las dependencias:

```pip install -r requirements.txt```

3. Crear un archivo `.streamlit/secrets.toml` con la siguiente estructura:

```[users]
admin1 = {password = "contraseña_segura1", role = "admin"}
user1 = {password = "contraseña_usuario1", role = "usuario"}
```

## Ejecución Local

```streamlit run streamlit_app.py```

## Despliegue
Para desplegar en Streamlit Community Cloud:

- Sube el código a GitHub (asegúrate de no incluir el archivo secrets.toml)
- Conéctate a Streamlit Community Cloud
- Despliega tu aplicación desde el repositorio
- En la configuración avanzada, añade el contenido de tu archivo secrets.toml en la sección "Secrets"

## Seguridad

- Las contraseñas se almacenan en el archivo secrets.toml que no debe incluirse en el repositorio
- Se utiliza hmac.compare_digest() para comparaciones seguras de contraseñas
- La autenticación se mantiene a través de st.session_state
