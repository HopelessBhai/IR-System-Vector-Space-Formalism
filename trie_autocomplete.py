from util import *

def find_vocab_size(): #find the highest ASCII size (maximum trie child index)
    queries_json = json.load(open("cranfield/cran_queries.json", 'r'))[:]

    queries=[d['query'] for d in queries_json]
    flatList=[c for query in queries for c in query] #flatten the list of queries
    vocab_size=-1

    for c in np.unique(flatList):
        vocab_size=max(vocab_size, ord(c)+1) #find the maximum ASCII size of the characters present in the queries.

    return vocab_size

vocab_size=find_vocab_size() #Find the maximum ASCII size of the characters present in the queries.

class TrieNode(): #Trie node class
    def __init__(self):
        self.children=[None for _ in range(vocab_size)] #initialize the children of the node to None

class Trie():

    def __init__(self):
        self.vocab_size=vocab_size
        queries_json = json.load(open("cranfield/cran_queries.json", 'r'))[:]
        self.queries=[d['query'] for d in queries_json] #load the queries from the json file

    def isTerminal(self, node): #check if the node is terminal
        for _ in node.children:
            if _!=None:
                return False
        return True

    def insert_key(self, root, key): #insert the key in the trie
        currNode=root
        for c in key:
            if currNode.children[ord(c)]==None: #if the child is None, create a new node
                newNode=TrieNode()
                currNode.children[ord(c)]=newNode
            currNode=currNode.children[ord(c)]

    def print_tree(self, currNode, s1, l1): #helper function to print the trie
        if currNode==None:
            return
        for i in range(self.vocab_size):
            self.candidateQueries(currNode.children[i], s1+chr(i), l1)
        l1.append(s1)

    def search_prefix(self, root, pref): #search the prefix in the trie and return the autocompleted query
        pref=pref.lower()
        currNode=root
        fString="" #final string
        for c in pref: #traverse the trie
            trgt_idx=ord(c)
            trgt_node=currNode.children[trgt_idx] #get the child node
            if trgt_node==None: #if the child is None, return False
                return False
        
            fString+=c #append the character to the final string
            currNode=trgt_node
        query_list=[]

        self.candidateQueries(currNode, "", query_list) #find the candidate queries using DFS

        for i, s in enumerate(query_list):
            query_list[i]=fString+s
        return self.print_query_list(query_list) #print the query list

    def print_query_list(self, query_list): #helper function to print the query list
        if(len(query_list)==1):
            return query_list[0]
        print('Multiple queries found: Choose one') #if multiple queries are found, ask the user to choose one
        for i, query in enumerate(query_list):
            print(f'{i+1}. {query}')
        idx=int(input())-1
        return query_list[idx]

    def candidateQueries(self, currNode, s1, l1): #helper function to find the candidate queries using DFS
        if currNode==None:
            return
        for i in range(self.vocab_size):
            self.candidateQueries(currNode.children[i], s1+chr(i), l1)
        if self.isTerminal(currNode):
            l1.append(s1)
 
    def create_trie(self): #create a trie data structure from the query list
        root=TrieNode()
        for query in self.queries:
            self.insert_key(root, query)
        return root

    def take_input(self, query): #take the input query and return the autocompleted query
        root=self.create_trie() #create the trie
        automated_query=self.search_prefix(root, query) #search the prefix in the trie
        if(automated_query==False):
            print('No queries found')
            return query
        else:
            print(f'The autocompleted query is: {automated_query}')
            return automated_query
