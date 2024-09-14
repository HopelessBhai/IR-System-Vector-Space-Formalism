from util import *

class Evaluation():

    def queryPrecision(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of precision of the Information Retrieval System
        at a given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The precision value as a number between 0 and 1
        """

        precision = -1
        countDocs = 0  # variable to count the number of relevant documents retrieved

        for doc_id in query_doc_IDs_ordered[:k]:  # looping over first k documents reteived
            if str(doc_id) in true_doc_IDs: # checking if the document is relevant
                countDocs += 1
        precision = countDocs / k  # number of relevant documents by number of retieved documents
        return precision

    def meanPrecision(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of precision of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean precision value as a number between 0 and 1
        """

        meanPrecision = -1

        # Fill in code here
        tempPrec = 0
        for query in query_ids: # looping over all the queries
            rel_docs = [d['id'] for d in qrels if int(d['query_num']) == query] # Getting the relevant documents for the query
            tempPrec += self.queryPrecision(doc_IDs_ordered[query - 1], query, rel_docs, k) # Calculating the precision for the query
        meanPrecision = tempPrec / len(query_ids)
        return meanPrecision

    def queryRecall(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of recall of the Information Retrieval System
        at a given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The recall value as a number between 0 and 1
        """

        recall = -1
        countDocs = 0
        relDocs = len(true_doc_IDs) 
        for doc_id in query_doc_IDs_ordered[:k]: # looping over first k documents reteived
            if str(doc_id) in true_doc_IDs: # checking if the document is relevant
                countDocs += 1

        recall = countDocs / relDocs # number of relevant documents by number of relevant documents
        return recall

    def meanRecall(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of recall of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean recall value as a number between 0 and 1
        """

        meanRecall = -1

        tempRecall = 0
        for query in query_ids: # looping over all the queries
            rel_docs = [d['id'] for d in qrels if int(d['query_num']) == query] # Getting the relevant documents for the query

            tempRecall += self.queryRecall(doc_IDs_ordered[query - 1], query, rel_docs, k) # Calculating the recall for the query

        meanRecall = tempRecall / len(query_ids) # Calculating the mean recall

        return meanRecall

    def queryFscore(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of fscore of the Information Retrieval System
        at a given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The fscore value as a number between 0 and 1
        """

        fscore = -1

        beta = 0.5

        precision = self.queryPrecision(query_doc_IDs_ordered, query_id, true_doc_IDs, k) # Calculating the precision for the query
        recall = self.queryRecall(query_doc_IDs_ordered, query_id, true_doc_IDs, k) # Calculating the recall for the query

        if precision == 0 and recall == 0:
            fscore = 0

        else:
            fscore = (1 + beta ** 2) * precision * recall / (beta ** 2 * precision + recall) # Calculating the fscore

        return fscore

    def meanFscore(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of fscore of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean fscore value as a number between 0 and 1
        """

        meanFscore = -1

        tempFscore = 0

        for query in query_ids: # looping over all the queries
            rel_docs = [d['id'] for d in qrels if int(d['query_num']) == query] # Getting the relevant documents for the query

            tempFscore += self.queryFscore(doc_IDs_ordered[query - 1], query, rel_docs, k) # Calculating the fscore for the query

        meanFscore = tempFscore / len(query_ids) # Calculating the mean fscore

        return meanFscore # Returning the mean fscore

    def queryNDCG(self, query_doc_IDs_ordered, query_id, qrels_doc, k):
        """
        Computation of nDCG of the Information Retrieval System
        at given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of dictionaries of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The nDCG value as a number between 0 and 1
        """

        nDCG = -1
        DCG = 0
        IDCG = 0
        rel_docs=[]
        true_docs_ids = [d['id'] for d in qrels_doc] # Getting the relevant documents for the query
        for i, doc_id in enumerate(query_doc_IDs_ordered[:k]): # Looping over the first k documents
            if str(doc_id) in true_docs_ids: # Checking if the document is relevant
                rel_score = [5 - d['position'] for d in qrels_doc if int(d['id']) == doc_id][0] # Getting the relevance score of the document
                DCG+= rel_score / (np.log2(i + 2)) # Calculating DCG
                rel_docs.append(rel_score)

        true_docs_sorted = sorted(qrels_doc, key=lambda x: x['position'])[:k] # Sorting the relevant documents

        for i, rel_score_dict in enumerate(true_docs_sorted): # Looping over the first k relevant documents
            rel_score = 5 - rel_score_dict['position'] # Getting the relevance score of the document
            IDCG += (2 ** rel_score - 1) / (np.log2(i + 2)) # Calculating IDCG

        if IDCG==0:
            return 0
    
        nDCG = DCG / IDCG

        return nDCG


    def meanNDCG(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of nDCG of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean nDCG value as a number between 0 and 1
        """

        meanNDCG = -1
        tempNDCG = 0
        for query_id in query_ids: # Looping over all the queries
            true_docs = [d for d in qrels if int(d['query_num']) == query_id] # Getting the relevant documents for the query
            query_docs = doc_IDs_ordered[query_id - 1] # Getting the documents for the query
            tempNDCG += self.queryNDCG(query_docs, query_id, true_docs, k) # Calculating nDCG for the query

        meanNDCG = tempNDCG / len(query_ids) # Calculating the mean nDCG

        return meanNDCG

    def queryAveragePrecision(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of average precision of the Information Retrieval System
        at a given value of k for a single query (the average of precision@i
        values for i such that the ith document is truly relevant)

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The average precision value as a number between 0 and 1
        """

        avgPrecision = -1
        count = 0
        precision = 0  # Initialising precision for query
        for i in range(1,k+1):
            if str(query_doc_IDs_ordered[i-1]) in true_doc_IDs:
                count += 1
                precision += self.queryPrecision(query_doc_IDs_ordered, query_id, true_doc_IDs,
                                                 i)  # Adding precision for every values of k
            # print(precision)
        if count == 0:
            avgPrecision = 0
        else:
            avgPrecision = precision / count  # Summation of precision values by k(position for which average precision is calculated)
        return avgPrecision

    def meanAveragePrecision(self, doc_IDs_ordered, query_ids, q_rels, k):
        """
        Computation of MAP of the Information Retrieval System
        at given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The MAP value as a number between 0 and 1
        """

        meanAveragePrecision = -1

        tempMAP = 0
        # Fill in code here
        for query_id in query_ids: # Looping over all the queries
            true_docs_ids = [d['id'] for d in q_rels if int(d['query_num']) == query_id] # Getting the relevant documents for the query
            tempMAP += self.queryAveragePrecision(doc_IDs_ordered[query_id - 1], query_id, true_docs_ids, k) # Calculating the average precision for the query

        meanAveragePrecision = tempMAP / len(query_ids) # Calculating the mean average precision
        return meanAveragePrecision

