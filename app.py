import os
import sys
import sqlalchemy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from flask import Flask
from flask_cors import CORS
from src.adapters.primary.http.routes.auth_routes import auth_routes
from src.adapters.primary.http.routes.face_route import face_routes
from src.adapters.primary.http.routes.password_route import password_routes
from src.adapters.primary.http.routes.proyecto_routes import proyecto_routes
from src.adapters.primary.http.routes.usuarios_routes import usuarios_routes
from src.infrastructure.config import DEBUG
from src.infrastructure.database import engine
from src.infrastructure.database_base import Base
from src.adapters.secondary.persistence.models.user_model import User  
from src.adapters.secondary.persistence.models.facial_embeding_model import FacialEmbedding
from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle
from src.adapters.secondary.persistence.models.cotizacion_model import Cotizacion
from src.adapters.secondary.persistence.models.proyecto_model import Proyecto
from src.adapters.secondary.persistence.models.optimizacion_model import CorteOptimizado
from src.adapters.secondary.persistence.models.vidrio_model import VidrioDetalle


from flask_mail import Mail
from src.infrastructure.config import load_dotenv, Config

# Cargar variables de entorno desde un archivo .env
load_dotenv()

app = Flask(__name__)

# Cargar las configuraciones desde la clase Config
app.config.from_object(Config)

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
        
        },  # Permitir todas las solicitudes de origen cruzado
})

# Inicializa Flask-Mail
mail = Mail(app)

# Registrar blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(face_routes)
app.register_blueprint(password_routes)
app.register_blueprint(proyecto_routes)
app.register_blueprint(usuarios_routes)

with engine.connect() as connection:
    connection.execute(sqlalchemy.text("Create extension if not exists vector;"))
    connection.commit()
# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    app.run(debug=DEBUG) 