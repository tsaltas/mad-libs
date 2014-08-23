import os
from flask import Flask

app = Flask(__name__)

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "mad_libs.config.DevelopmentConfig")
app.config.from_object(config_path)

import views
import filters