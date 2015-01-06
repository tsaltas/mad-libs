import os
import unittest
import nltk_data

# Configure our app to use the testing configuration
os.environ["CONFIG_PATH"] = "mad_libs.config.TestingConfig"

from mad_libs import app
from mad_libs import helpers

class TestHelpers(unittest.TestCase):
	""" Tests for the mad-libs helper functions """

	def setUp(self):
		""" Test setup """
		self.client = app.test_client()

	def test_load_contractions(self):
		""" Make sure it's tokenizing contractions appropriately and covering different cases """
		contractions = helpers.load_contractions()
		self.assertEqual(contractions["are n't"], "aren't")
		self.assertEqual(contractions["Are n't"], "Aren't")
		self.assertEqual(contractions["ARE N'T"], "AREN'T")
		self.assertEqual(contractions["Ca n't"], "Can't")
		self.assertEqual(contractions["she 's"], "she's")
		self.assertEqual(contractions["THEY 'LL"], "THEY'LL")
		self.assertEqual(contractions["Were n't"], "Weren't")
		self.assertEqual(contractions["who 're"], "who're")

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
		self.assertEqual(type(to_replace1[0][2]), str)

		# Test that the output has expected values
		words1 = [element[0] for element in to_replace1]
		words1.sort()
		words2 = [element[0] for element in to_replace2]
		words2.sort()

		self.assertEqual(words1, ["Goodbye", "He", "Hello", "What"])
		self.assertEqual(words2, ["Goodbye", "Hello"])

	def test_join_word_tokenized_text(self):
		""" Joining back together text that has been tokenized by NLTK """
		strings = []
		# Try a simple sentence
		strings.append("Hello my name is Shannon.")
		# Add some punctuation
		strings.append("Hello, my name is Shannon.")
		# Try a question
		strings.append("What is your favorite programming language?")
		# Try some contractions, in different cases
		strings.append("What's that he's saying?")
		strings.append("CAN'T DO THAT.")
		strings.append("Isn't it a shame?")
		strings.append("He'd like that.")
		strings.append("I didn't believe it.")
		# Try some different kinds of quotations
		strings.append("My favorite book is 'The Left Hand of Darkness' by Ursula K. LeGuin.")
		strings.append("My favorite book is \"The Left Hand of Darkness\" by Ursula K. LeGuin.")
		strings.append("My favorite book is ''The Left Hand of Darkness'' by Ursula K. LeGuin.")
		strings.append("My favorite book is ``The Left Hand of Darkness`` by Ursula K. LeGuin.")
		# Try quotations and contractions together
		strings.append("\"Can we go to the store?\" 'I don't feel like it,' he answered. \"But we're out of milk!\" she exclaimed.")
		# Some random sentences from the internet.
		strings.append("The devices wound with copper are usually replaced every two-to-five years, depending on which type you have.")
		strings.append("Metallurgists among you should be aware that the strings are made from 80% copper and 20% zinc to give a clear, bright response.")

		for string in strings:
			self.assertEqual(helpers.single_to_double_quotes(string), helpers.join_word_tokenized_text(helpers.tokenize_text(string)))