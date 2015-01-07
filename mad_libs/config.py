import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///mad-libs-development.db"
    DEBUG = True
    SECRET_KEY = os.environ.get("MADLIBS_SECRET_KEY", "")

class TestingConfig(object):
	SQLALCHEMY_DATABASE_URI = "sqlite:///mad-libs-testing.db"
	DEBUG = True
	SECRET_KEY = "Not secret"

class DeploymentConfig(object):
	SQLALCHEMY_DATABASE_URI = "sqlite:///mad-libs.db"
	DEBUG = False
	SECRET_KEY = os.environ.get("MADLIBS_SECRET_KEY", "")