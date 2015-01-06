import os
import unittest

# Configure our app to use the testing configuration
os.environ["CONFIG_PATH"] = "mad_libs.config.TestingConfig"

from mad_libs import app
from mad_libs.models import Story
from mad_libs.helpers import *
from mad_libs.database import Base, engine, session

class TestViews(unittest.TestCase):
	""" Tests for the mad-libs view functions """

	def setup(self):
		""" Test setup """
		self.client = app.test_client()

		# Set up the tables in the database
		Base.metadata.create_all(engine)

	def tear_down(self):
		""" Test teardown """
		# Remove the tables and their data from the database
		Base.metadata.drop_all(engine)

	def test_new_story_post(self):
		""" Adding a new story to the database """
		pass