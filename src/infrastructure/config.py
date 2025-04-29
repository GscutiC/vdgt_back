import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()


# Configuración de la aplicación
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

# Otras configuraciones
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} 

