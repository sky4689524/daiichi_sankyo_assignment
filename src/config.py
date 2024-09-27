import os


class Config:
    DB_NAME = "business"
    DB_USER = "postgres"
    DB_HOST = "localhost"
    DB_PASSWORD = "thepassword"
    DB_ADMIN_USER = "postgres"
    DB_ADMIN_PASSWORD = "thepassword"
    DB_PORT = 5432
    ENV = "dev"
    
    # Build the SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    DB_HOST = "business-db"

    SQLALCHEMY_DATABASE_URI = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"


def load_config(testing: bool):
    # Ignore env vars if testing is passed
    if testing:
        return TestConfig

    env = os.getenv("ENV")

    if env == "dev":
        return Config
    elif env == "preprod":
        return TestConfig
    elif env == "prod":
        return Config
    raise RuntimeError("Unexpected value of environment variable `ENV`: ", env)
