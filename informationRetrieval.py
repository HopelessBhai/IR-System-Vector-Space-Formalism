from util import *

class InformationRetrieval():

	def __init__(self):
		self.index = None
		self.docs = None

	def buildIndex(self, docs, docIDs):
		"""
		Builds the document index in terms of the document
		IDs and stores it in the 'index' class variable

		Parameters
		----------
		arg1 : list
			A list of lists of lists where each sub-list is
			a document and each sub-sub-list is a sentence of the document
		arg2 : list
			A list of integers denoting IDs of the documents
		Returns
		-------
		None
		"""

		index={} #Dictionary to store the index

		for id in docIDs: #Iterating over the document IDs
			doc=docs[id-1]
			for word in doc: #Iterating over the words in the document
				if word.isalpha(): #Checking if the word is an alphabet
					if word not in index: #Checking if the word is already in the index
						index[word]=[]

					index[word].append(id)


		self.index=index
		self.docs=docs

		self.buildIDF(self.docs,self.index)
		self.tf_idf_docs()

	def buildIDF(self, docs, index): #Function to build the IDF values
		"""
		Builds the IDF values for the terms in the index

		Parameters
		----------
		arg1 : list
			A list of lists of lists where each sub-list is
			a document and each sub-sub-list is a sentence of the document
		arg2 : dict
			A dictionary where the keys are terms and the values are
			lists of document IDs containing the term
			
		Returns
		-------
		None
		"""
		

		idf_values={}
		D=len(docs) #Number of documents
		for term in index.keys(): #Iterating over the terms in the inverted index
			d = len(index[term]) #Number of documents containing the term
			idf_values[term]=math.log2(D/d) #Computing the IDF value

		self.idf = idf_values
	

	def tf_idf_docs(self): #Function to compute the TF-IDF values for the documents
		"""
		Builds the TF-IDF values for the documents

		Parameters
		----------
		None

		Returns
		-------
		None
		"""
		

		D=len(self.docs)
		docvectors=[]

		for docid in range(D): #Iterating over the documents
			docvector=np.zeros(len(self.index))
			for termid , term in enumerate(self.index): #Iterating over the terms in the index
				if self.docs[docid]!=None: #Checking if the document is not empty
					tfd = self.docs[docid].count(term) #Computing the term frequency
					docvector[termid]=tfd*self.idf.get(term,0) #Computing the TF-IDF value

			docvectors.append(docvector)

		self.docvectors=docvectors #Storing the document vectors (with TF-IDF values)

		# print(np.array(docvectors).shape)

	def tf_idf_query(self, queries): #Function to compute the TF-IDF values for the queries

		"""
		Builds the TF-IDF values for the queries

		Parameters
		----------
		arg1 : list
			A list of lists of lists where each sub-list is a query and
			each sub-sub-list is a sentence of the query
		
		Returns
		-------
		list
			A list of lists where each sub-list is a TF-IDF vector for a query
		"""
		

		queryvectors=[] #List to store the query vectors

		for queryid in range(len(queries)): #Iterating over the queries
			queryvector = np.zeros(len(self.index)) #Initializing the query vector
			for termid , term in enumerate(self.index): #Iterating over the terms in the index
				tfq=queries[queryid].count(term) #Computing the term frequency
				queryvector[termid]=tfq*self.idf.get(term,0) #Computing the TF-IDF value

			queryvectors.append(queryvector.tolist()) #Appending the query vector to the list

		return queryvectors
	
	def create_dist_sim(self, index, docs, k=2): #Function to create the term-term matrix
		"""
		Creates the term-term matrix using the co-occurrence values

		Parameters
		----------
		arg1 : dict
			A dictionary where the keys are terms and the values are
			lists of document IDs containing the term
		arg2 : list
			A list of lists of lists where each sub-list is
			a document and each sub-sub-list is a sentence of the document
		arg3 : int
			The window size for co-occurrence

		Returns
		-------
		None
		"""

		co_occurrence = np.zeros((len(index), len(index)), dtype=int) #Initializing the co-occurrence matrix
		N = 0
		revdocs = [] #List to store the reversed documents
		for doc in docs: #Iterating over the documents
			revdoc = []
			for term in doc: #Iterating over the terms in the document
				if term in index: #Checking if the term is in the index
					revdoc.append(term) #Appending the term to the reversed document
			revdocs.append(revdoc) #Appending the reversed document to the list
			print(revdocs[0])
		for id, revdoc in enumerate(revdocs): #Iterating over the reversed documents
			for i, term1 in enumerate(revdoc): #Iterating over the terms in the reversed document
				start = max(0, i - k) #Computing the start index for the window
				end = min(len(revdoc), i + k + 1) #Computing the end index for the window

				for term2 in revdoc[start:end]: #Iterating over the terms in the window
					co_occurrence[list(index.keys()).index(term1), list(index.keys()).index(term2)] += 1 #Incrementing the co-occurrence value

		print('Co-occurrence done')
		np.save('saved_inputs/co_occurrence_matrix.npy', co_occurrence) #Saving the co-occurrence matrix
		co_occurrence = np.load('saved_inputs/co_occurrence_matrix.npy') #Loading the co-occurrence matrix
		N=np.sum(co_occurrence) #Computing the total number of co-occurrences
		pmi = np.zeros((len(index), len(index)), dtype=float) #Initializing the PMI matrix
		row_sum=np.sum(co_occurrence,axis=1) #Computing the row sum of the co-occurrence matrix
		for i in range(len(index)): #Iterating over the terms in the index
			for j in range(len(index)): #Iterating over the terms in the index
				denominator = float(row_sum[i]/N)*float(row_sum[j]/N) #Computing the denominator for PMI
				if co_occurrence[i][j] > 0 and denominator > 0:
					pmi[i][j] = math.log2(float(co_occurrence[i][j]/N) / denominator) #Computing the PMI value
				else:
					pmi[i][j] = 0.0 #Set PMI to zero if the co-occurrence is zero to avoid math domain error
				print(i,j)
		print('PMI done')
		for i in range(len(index)): #Iterating over the terms in the index
			for j in range(len(index)): #Iterating over the terms in the index
				if pmi[i][j] < 0: #Checking if the PMI value is negative
					pmi[i][j] = 0.0 #Setting the PMI value to zero
				
				print(i, j)

		print('PPMI done')
		np.save('saved_inputs/pmi.npy',pmi)
		pmi=np.load('saved_inputs/pmi.npy')
		termterm = np.zeros((len(index), len(index)), dtype=float) #Initializing the term-term matrix
		temp = np.dot(pmi, pmi)
		norms=[] #List to store the norms of the PMI vectors
		for i in range(len(index)): #Iterating over the terms in the index
			tempnorm=np.linalg.norm(pmi[i]) #Computing the norm of the PMI vector
			norms.append(tempnorm) #Appending the norm to the list
			print(i)
		for i in range(len(index)): #Iterating over the terms in the index
			for j in range(len(index)): 
				a = norms[i] #Getting the norm of the ith term
				b = norms[j] #Getting the norm of the jth term
				if a != 0 and b != 0 and temp[i][j]>0: #Checking if the norms are non-zero
					termterm[i][j] = temp[i][j] / (a * b) #Computing the term-term value
				else:
					termterm[i][j] = 0
				print(i,j)

		print('Term-Term done')
		np.save('saved_inputs/termterm.npy',termterm) #Saving the term-term matrix

	
	def LSI(self, k, docvectors, queryvectors): #Function to perform Latent Semantic Indexing
		"""
		Perform Latent Semantic Indexing (LSI) on the document vectors

		Parameters
		----------
		arg1 : int
			The number of concepts to retain
		arg2 : list
			A list of lists where each sub-list is a document and
			each sub-sub-list is a sentence of the document
		arg3 : list
			A list of lists where each sub-list is a query and
			each sub-sub-list is a sentence of the query
		
		Returns
		-------
		tuple
			A tuple of two numpy arrays where the first array is the
			transformed document vectors and the second array is the
			transformed query vectors
		"""
		

		U, S, VT = np.linalg.svd(np.array(docvectors).T) #Performing SVD on the document vectors (shape: (terms, docs))

		U_approx = U[:,:k] #Approximating the U matrix
		VT_approx = VT[:k,:] #Approximating the VT matrix
		S_approx = np.diag(S[:k]) #Approximating the S matrix


		transformed_docs=[]
		transformed_queries=[]

		for query in queryvectors: #Iterating over the queries
			query_transformed=np.dot(query, U_approx)@np.linalg.inv(S_approx) #Transforming the query vector (to concept space)
			transformed_queries.append(query_transformed)

		for doc_id in range(len(docvectors)): #Iterating over the documents
			doc_transformed=VT_approx.T[doc_id] #Transforming the document vector (to concept space)
			transformed_docs.append(doc_transformed)
	
		return np.array(transformed_docs), np.array(transformed_queries)
	

	def rank(self, queries, method):
		"""
		Rank the documents according to relevance for each query

		Parameters
		----------
		arg1 : list
			A list of lists of lists where each sub-list is a query and
			each sub-sub-list is a sentence of the query
		
		Returns
		-------
		list
			A list of lists of integers where the ith sub-list is a list of IDs
			of documents in their predicted order of relevance to the ith query
		"""

		
		queryvectors=self.tf_idf_query(queries) #Computing the TF-IDF values for the queries

		docvectors=self.docvectors #Getting the document vectors

		if method=='LSI':
			_docvectors_, _queryvectors_=self.LSI(k=130, docvectors=docvectors, queryvectors=queryvectors) #Performing LSI
			return self.orderDocs(_docvectors_, _queryvectors_)
		
		elif method=="VSM":
			return self.orderDocs(docvectors, queryvectors)
		
		elif method=="CRN":
			try:
				tt_sim = np.load('saved_inputs/termterm.npy')

			except FileNotFoundError:
				print('Creating term-term matrix')
				self.create_dist_sim(self.index, self.docvectors)
				tt_sim = np.load('saved_inputs/termterm.npy')

			docvectors=np.array(docvectors)@tt_sim
			queryvectors=np.array(queryvectors)@tt_sim

			return self.orderDocs(docvectors, queryvectors)

		else:

			print(f'Invalid model argument: {method}')
			print(f'Available Methods: VSM, LSI, CRN')
			quit()
	
	def orderDocs(self, docvectors, queryvectors): #Function to rank the documents based on the cosine similarity with the queries
		"""
		Rank the documents based on the cosine similarity with the queries

		Parameters
		----------
		arg1 : list
			A list of lists where each sub-list is a document vector
		arg2 : list
			A list of lists where each sub-list is a query vector

		
		Returns
		-------
		list
			A list of lists of integers where the ith sub-list is a list of IDs
			of documents in their predicted order of relevance to the ith query
		"""
		

		doc_IDs_ordered=[]
		for query_num, query in enumerate(queryvectors): #Iterating over the queries
			tempDict={}
			for doc_id in range(len(docvectors)): #Iterating over the documents

				queryNorm=np.linalg.norm(query) #Computing the norm of the query vector
				docNorm=np.linalg.norm(docvectors[doc_id]) #Computing the norm of the document vector

				if queryNorm!=0 and docNorm!=0:
					sim=np.dot(query, docvectors[doc_id])/(queryNorm*docNorm) #Computing the cosine similarity

				else:
					sim=0

				tempDict[doc_id+1] = sim #Storing the similarity score

			fList = sorted(tempDict.items(), key=lambda item: item[1], reverse=True)[:10] #Sorting the documents based on the similarity score (only the first 10 are chosen)

			doc_IDs_ordered.append([doc[0] for doc in fList]) #Appending the document IDs to the list

		return doc_IDs_ordered