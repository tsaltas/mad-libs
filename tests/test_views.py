import os
import unittest
from urlparse import urlparse

# Configure our app to use the testing configuration
os.environ["CONFIG_PATH"] = "mad_libs.config.TestingConfig"

from mad_libs import app
from mad_libs import helpers
from mad_libs.models import Story
from mad_libs.database import Base, engine, session

class TestViews(unittest.TestCase):
	""" Tests for the mad-libs view functions """

	def setUp(self):
		""" Test setup """
		self.client = app.test_client()

		# Set up the tables in the database
		Base.metadata.create_all(engine)

	def tearDown(self):
		""" Test teardown """
		# Remove the tables and their data from the database
		Base.metadata.drop_all(engine)

	def test_new_story_post(self):
		""" Adding a new story to the database """
		# Simulate request object
		data = dict(title="Test Story", author="Shannon", content="This is just a test.")

		# Make the http request
		response = self.client.post("/new_story", data=data)

		# Check that the story is created and user is redirected to the form to play Mad Libs with the story
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, "/mad_libs/1")

		# Make sure story made it into database
		stories = session.query(Story).all()
		self.assertEqual(len(stories), 1)

		story = stories[0]
		self.assertEqual(story.title, "Test Story")
		self.assertEqual(story.content, "This is just a test.")
		self.assertEqual(story.author, "Shannon")
