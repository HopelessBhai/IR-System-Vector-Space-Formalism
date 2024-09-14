from util import *
from nltk.stem import PorterStemmer #Importing the Porter's Algorithm for stemming

# Add your import statements here
class InflectionReduction:

	def reduce(self, text):
		"""
		Stemming/Lemmatization

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list a sequence of tokens
			representing a sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of
			stemmed/lemmatized tokens representing a sentence
		"""

		reducedText = None

		#Fill in code here
		porter_stemmer=PorterStemmer() #Initialising the Porter's Stemmer
		reducedText=[porter_stemmer.stem(token) for token in text] #Function call to the Porter's Stemmer for stemming every token in the text
	

		return reducedText
	
	def lemmatize(self, text):

		"""
		Stemming/Lemmatization

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list a sequence of tokens
			representing a sentence

		Returns
		-------
		list
			A list of lists where each sub-list is a sequence of
			stemmed/lemmatized tokens representing a sentence
		"""

		def pos_tagger(nltk_tag): #Function to tag the POS of the tokens
			if nltk_tag.startswith('J'): #Checking if the token is an adjective
				return wordnet.ADJ
			elif nltk_tag.startswith('V'): #Checking if the token is a verb
				return wordnet.VERB
			elif nltk_tag.startswith('N'): #Checking if the token is a noun
				return wordnet.NOUN
			elif nltk_tag.startswith('R'): #Checking if the token is an adverb
				return wordnet.ADV
			else:          
				return None

		reducedText=None

		lemmatizer=WordNetLemmatizer() #Initialising the WordNet Lemmatizer

		pos_tagged = nltk.pos_tag(text) #POS tagging the tokens in the text

		wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged)) #Mapping the POS tags to the tokens

		lemmatized_sentence=[] #Initialising the list to store the lemmatized tokens

		for word, tag in wordnet_tagged:
			if tag is None:
				# if there is no available tag, append the token as is
				lemmatized_sentence.append(word)
			else:        
				# else use the tag to lemmatize the token
				lemmatized_sentence.append(lemmatizer.lemmatize(word, tag)) #Lemmatizing the tokens

		reducedText=lemmatized_sentence #Assigning the lemmatized tokens to the reducedText variable

		return reducedText




