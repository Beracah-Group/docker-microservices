from src.api.v1.servicepackage import *
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from src.instance.config import application_configuration

app = Flask(__name__)


def EnvironmentName(environment):
    app.config.from_object(application_configuration[environment])


EnvironmentName('DevelopmentEnvironment')
databases = SQLAlchemy(app)