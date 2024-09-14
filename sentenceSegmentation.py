from util import *


class SentenceSegmentation():

	def naive(self, text):

		segmentedText=text.split('.') #splitting the sentences at each occurrence of '.'

		return segmentedText





	def punkt(self, text):

		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle') #Importing the pre-trained english tokenizer

		segmentedText=sent_detector.tokenize(text.strip()) #Tokenizing the text into sentences

		return segmentedText
	