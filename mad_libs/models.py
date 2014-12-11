import datetime

from sqlalchemy import Column, Integer, String, Sequence, Text, DateTime

from database import Base, engine

# ----Story class for mad libs app---- #

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, Sequence("post_id_sequence"), primary_key=True)
    title = Column(String(1024))
    author = Column(String(1024))
    content = Column(Text)
    datetime = Column(DateTime, default=datetime.datetime.now)

# Create the app model
Base.metadata.create_all(engine)