import os
import unittest

# Configure our app to use the testing configuration
os.environ["CONFIG_PATH"] = "mad_libs.config.TestingConfig"

from mad_libs import app
from mad_libs import helpers

class TestHelpers(unittest.TestCase):
	""" Tests for the mad-libs helper functions """

	def setUp(self):
		""" Test setup """
		self.client = app.test_client()

	def test_load_pos_tags(self):
		""" Test that pos tags are loading properly """
		pos_tags = helpers.load_POS_tags()
		self.assertEqual(len(pos_tags), 17)
		self.assertEqual(pos_tags["NNS"], "Noun, plural")

	def test_words_to_replace(self):
		""" Test function that finds n most common words to replace """
		test_string1 = "Hello Hello Hello Goodbye Goodbye Goodbye What What What He He He"
		test_string2 = "Hello Hello Hello Goodbye Goodbye What"
		tokenized1 = helpers.tokenize_text(test_string1)
		tokenized2 = helpers.tokenize_text(test_string2)
		
		to_replace1 = helpers.words_to_replace(tokenized1, 4)
		to_replace2 = helpers.words_to_replace(tokenized2, 2)

		# Test that the output is in expected format
		self.assertEqual(len(to_replace1), 4)
		self.assertEqual(len(to_replace2), 2)

		self.assertEqual(type(to_replace1[0]), tuple)
		self.assertEqual(type(to_replace1[0][0]), str)
		self.assertEqual(type(to_replace1[0][1]), str)

		# Test that the output has expected values
		words1 = [element[0] for element in to_replace1]
		words1.sort()
		words2 = [element[0] for element in to_replace2]
		words2.sort()

		self.assertEqual(words1, ["Goodbye", "He", "Hello", "What"])
		self.assertEqual(words2, ["Goodbye", "Hello"])