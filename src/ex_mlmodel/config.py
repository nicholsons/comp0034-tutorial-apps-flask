"""Flask configuration class."""


class Config:
    """Base config."""
    SECRET_KEY = "saULPgD9XU8vzLVk7kyLBw"


class ProdConfig(Config):
    """Production config.

    Not currently implemented.
    """

    pass


class DevConfig(Config):
    """Development config"""

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    """Test config"""

    TESTING = True
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = False  # Needs to be turned off for testing


app_config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig
}
