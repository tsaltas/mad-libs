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
    """ Seed stories to database """
    file_names = [
        "LaLaLa.txt"
        , "ArielsStory.txt"
        , "BeautyandtheBeast.txt"
        , "HanselGretel.txt"
        , "Rapunzel.txt"
        , "SeaAdventure.txt"
        , "SleepingBeauty.txt"
        , "LittleRedCap.txt"
    ]
    
    for filename in file_names:
        file_path = app.root_path + '/static/stories/' + filename

        try:
            with open(file_path, "r") as f:
                story = Story(
                    title = f.readline(),
                    author = f.readline(),
                    content = unicode(f.read(), errors='ignore')
                )
                session.add(story)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        
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