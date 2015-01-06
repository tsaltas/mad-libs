import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///mad-libs-development.db"
    DEBUG = True
    SECRET_KEY = os.environ.get("MADLIBS_SECRET_KEY", "")

class TestingConfig(object):
	SQLALCHEMY_DATABASE_URI = "sqlite:///mad-libs-testing.db"
	DEBUG = False
	SECRET_KEY = "Not secret"