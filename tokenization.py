from util import * #Importing Python NLTK from util.py module
from nltk import word_tokenize #Importing the Penn Treebank word tokenizer


class Tokenization():

	def naive(self, text):
		"""
		Tokenization using a Naive Approach

		Parameters
		----------
		arg1 : list
			A list of strings where each string is a single sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
		"""


		tokenizedText=[]
		pattern = r'\s+|[,.;!?()-]+'
		for sentence in text:
			tokenizedText.extend(re.split(pattern,sentence)) #Tokenization such that every word separated by whitespace and puntuations is a token
		# print(tokenizedText)
		return tokenizedText #Returning tokenized text



	def pennTreeBank(self, text):
		"""
		Tokenization using the Penn Tree Bank Tokenizer

		Parameters
		----------
		arg1 : list
			A list of strings where each string is a single sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
		"""

		#Fill in code here
		tokenizedText=[]
		for sentence in text:
			tokenizedText.extend(word_tokenize(sentence)) #Function call to the in-built Penn Treebank Word Tokenizer
		return tokenizedText #Returning tokenized text