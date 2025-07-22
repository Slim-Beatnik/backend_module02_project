import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+mysqlconnector://root:test@localhost/repair_shop_db"
    )
    DEBUG = True
    CACH_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"check_same_thread": False}}  # noqa: RUF012
    DEBUG = True
    CACHE_TYPE = "SimpleCache"


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    CACHE_TYPE = "SimpleCache"
