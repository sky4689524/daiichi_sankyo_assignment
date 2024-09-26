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


class TestConfig(Config):
    DB_HOST = "business-db"


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
