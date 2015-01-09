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
		""" Load the POS tags """
		pos_tags = helpers.load_POS_tags()
		self.assertEqual(len(pos_tags), 17)
		self.assertEqual(pos_tags["NNS"], "Noun, plural")

	def test_words_to_replace(self):
		""" Find n most common words to replace """
		# Should find most common words regardless of caps
		test_string1 = "The dolphin likes to play with the other Dolphin who likes to pretend he is not a DOLPHIN. They often Pretend and PLAY together."
		test_string2 = "Most hats that I wear are black but some HaTs are brown and other HATS are blue. Some people wear crazy Hats."
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

		self.assertEqual(words1, ["dolphin", "likes", "play", "pretend"])
		self.assertEqual(words2, ["hats", "wear"])

	def test_replace_words(self):
		""" Replace words in original text with new words """
		# Should find most common word regardless of caps
		test_string1 = "The dolphin likes to play with the other Dolphin who likes to pretend he is not a DOLPHIN. They often Pretend and PLAY together."
		test_string2 = "Most hats that I wear are black but some Hats are brown and other HATS are blue. Some people wear crazy Hats."

		# Create replacement
		replacement1 = (("dolphin", "frog"), ("likes", "hates"), ("play", "sleep"), ("pretend", "remember"))
		replacement2 = (("hats", "scarves"), ("wear", "toss"))

		# Do replacement
		text1 = helpers.replace_words(test_string1, replacement1)
		text2 = helpers.replace_words(test_string2, replacement2)

		self.assertEqual(text1, "The <span class=\"replaced\">frog</span> <span class=\"replaced\">hates</span> to <span class=\"replaced\">sleep</span> with the other <span class=\"replaced\">Frog</span> who <span class=\"replaced\">hates</span> to <span class=\"replaced\">remember</span> he is not a <span class=\"replaced\">FROG</span>. They often <span class=\"replaced\">Remember</span> and <span class=\"replaced\">SLEEP</span> together.")
		self.assertEqual(text2, "Most <span class=\"replaced\">scarves</span> that I <span class=\"replaced\">toss</span> are black but some <span class=\"replaced\">Scarves</span> are brown and other <span class=\"replaced\">SCARVES</span> are blue. Some people <span class=\"replaced\">toss</span> crazy <span class=\"replaced\">Scarves</span>.")