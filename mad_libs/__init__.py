import os
from flask import Flask

app = Flask(__name__)

config_path = os.environ.get("CONFIG_PATH", "mad_libs.config.DeploymentConfig")
app.config.from_object(config_path)

import mad_libs.views
import mad_libs.filters
