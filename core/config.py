
class DevConfig:
    # Should be stored in environment variables.
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./store.sqlite3'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class TestConfig:
    # Should be stored in environment variables.
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./store.sqlite3'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
