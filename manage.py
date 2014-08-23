import os
from flask.ext.script import Manager

from mad_libs import app

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    manager.run()