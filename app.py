import os
import sys
import sqlalchemy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from flask import Flask
from flask_cors import CORS
from src.adapters.primary.http.routes.auth_routes import auth_routes
from src.infrastructure.config import DEBUG
from src.infrastructure.database import engine
from src.infrastructure.database_base import Base
from src.adapters.secondary.persistence.models.user_model import User  
from src.adapters.secondary.persistence.models.facial_embeding_model import FacialEmbedding
from flask_mail import Mail
from src.infrastructure.config import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
        
        },  # Permitir todas las solicitudes de origen cruzado
})


# Configurar Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Cambia esto según el proveedor de correo
app.config['MAIL_PORT'] = 587  # Generalmente 587 para Gmail
app.config['MAIL_USE_TLS'] = True  # Habilita la encriptación
app.config['MAIL_USE_SSL'] = False  # No usar SSL
app.config['MAIL_USERNAME'] = 'shonencamilo923@gmail.com'  # Tu correo electrónico
app.config['MAIL_PASSWORD'] = 'slwn vnyn jwyn hgog'  # Tu contraseña (considera usar una variable de entorno)
app.config['MAIL_DEFAULT_SENDER'] = 'shonencamilo923@gmail.com'  # Remitente por defecto

# Inicializa Flask-Mail
mail = Mail(app)

# Registrar blueprints
app.register_blueprint(auth_routes)

with engine.connect() as connection:
    connection.execute(sqlalchemy.text("Create extension if not exists vector;"))
    connection.commit()
# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    app.run(debug=DEBUG) 