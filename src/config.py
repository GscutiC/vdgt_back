import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")