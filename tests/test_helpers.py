import os
import unittest

# Configure our app to use the testing configuration
os.environ["CONFIG_PATH"] = "mad_libs.config.TestingConfig"

from mad_libs import app
from mad_libs.models import Story
from mad_libs import helpers
from mad_libs.database import Base, engine, session

class TestHelpers(unittest.TestCase):
	""" Tests for the mad-libs helper functions """

	def setup(self):
		""" Test setup """
		self.client = app.test_client()

		# Set up the tables in the database
		Base.metadata.create_all(engine)

	def tear_down(self):
		""" Test teardown """
		# Remove the tables and their data from the database
		Base.metadata.drop_all(engine)

	def test_load_contractions(self):
		""" Make sure it's tokenizing contractions appropriately and covering different cases """
		contractions = helpers.load_contractions()
		self.assertEqual("are n't", contractions["aren't"])
		self.assertEqual("Are n't", contractions["Aren't"])
		self.assertEqual("ARE N'T", contractions["AREN'T"])
		self.assertEqual("Ca n't", contractions["Can't"])
		self.assertEqual("she 's", contractions["she's"])
		self.assertEqual("THEY 'LL", contractions["THEY'LL"])
		self.assertEqual("Were n't", contractions["Weren't"])
		self.assertEqual("who 're", contractions["who're"])

	def test_words_to_replace(self):
		"""XXX"""
		pass

	def test_process_user_input(self):
		"""XXX"""
		pass

	def test_replace_words(self):
		"""XXX"""
		pass

	def test_join_word_tokenized_text(self):
		""" Joining back together text that has been tokenized by NLTK """
		strings = []
		# Try a simple sentence
		strings.append("Hello my name is Shannon.")
		# Add some punctuation
		strings.append("Hello, my name is Shannon.")
		# Try a question
		strings.append("What is your favorite programming language?")
		# Try some contraction
		strings.append("What's that he's saying?")
		strings.append("Can't do that.")
		strings.append("Isn't it a shame?")
		strings.append("He'd like that.")
		# Try a quotation
		strings.append("My favorite book is 'The Left Hand of Darkness' by Ursula K. LeGuin.")
		# Try quotations and contractions
		strings.append("\"Can we go to the store?\" 'I don't feel like it,' he answered. \"But we're out of milk!\" she exclaimed.")

		for string in strings:
			#print "string:"
			#print helpers.single_to_double_quotes(string)
			#print "tokenized:"
			#print helpers.tokenize_text(string)
			#for key, value in helpers.load_contractions().iteritems():
				#print helpers.tokenize_text(key)

			self.assertEqual(helpers.single_to_double_quotes(string), helpers.join_word_tokenized_text(helpers.tokenize_text(string)))
		pass