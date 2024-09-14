from util import *
from nltk.corpus import stopwords #Importing the curated list of stopwords from NLTK


class StopwordRemoval():

	def fromList(self, text):
		"""
		Sentence Segmentation using the Punkt Tokenizer

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of tokens
			representing a sentence with stopwords removed
		"""

		stopwordRemovedText=[]
		removedstopwords=[]
		# nltk.download('stopwords') #Downloading the list of stopwords from NLTK
		stop_words=set(stopwords.words('english')) #Initialising the list of stopwords for English language
		for word in text:
			if word not in stop_words:
				stopwordRemovedText.append(word) #Dropping the tokens that match with the list
			else:
				removedstopwords.append(word) #Creating the list of stopwords removed
		return stopwordRemovedText

