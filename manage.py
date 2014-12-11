import os
from flask.ext.script import Manager

from mad_libs import app

from mad_libs.models import Story
from mad_libs.database import session

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

@manager.command
def seed():
    """ Seed fake stories to database """
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    for i in range(25):
    	story = Story(
            title = "Test Story #{}".format(i),
            author = "Anonymous",
            content = content
        )
        session.add(story)
    session.commit()

@manager.command
def purge():
    """ Clear all stories from database """
    stories = session.query(Story).all()
    for story in stories:
        session.delete(story)
    session.commit()

if __name__ == "__main__":
    manager.run()