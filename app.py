import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from flask import Flask
from src.adapters.primary.http.routes.auth_routes import auth_routes
from src.infrastructure.config import DEBUG
from src.infrastructure.database import engine
from src.infrastructure.database_base import Base
from src.adapters.secondary.persistence.models.user_model import User  

app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(auth_routes)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    app.run(debug=DEBUG) 