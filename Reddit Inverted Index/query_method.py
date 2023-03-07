from lib2to3.pgen2.token import EQUAL, LESS
import project2
import nltk
nltk.download('stopwords')
import math


#my_dict = { key: ([item.lower() for item in my_dict[key]] if type(my_dict[key]) == type([]) else my_dict[key])  for key in my_dict}
# This box is for Pre Processing
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def mergeSkipDAAT(invertedIndex,postingListLength,weightSort = False):

    num_comparisons = 0
    num_docs = 0
    num_results = []


    numberQueryTerms = len(postingListLength)
    intermediatePostinghead =  invertedIndex[postingListLength[0][0]].head


    i = 1 

    


    while i < numberQueryTerms:
            head2 = invertedIndex[postingListLength[i][0]].head
            newPostingList = project2.linkedList()
            

            while( head2 is not None and intermediatePostinghead is not None):
                num_comparisons +=1 

                if head2.value == intermediatePostinghead.value:
                    tf_idf = max(head2.tf_idf,intermediatePostinghead.tf_idf)
                    newPostingList.insert(intermediatePostinghead.value,tf_idf)
                    head2 = head2.nextNode
                    intermediatePostinghead =   intermediatePostinghead.nextNode
                   

                elif head2.value < intermediatePostinghead.value:
                    if(head2.skipNode is not None):
                        skipValue = head2.skipNode.value
                        if(skipValue <= intermediatePostinghead.value):
                            head2 =head2.skipNode
                            continue
                        
                    head2 =head2.nextNode  
                    

                elif   head2.value > intermediatePostinghead.value:

                    if(intermediatePostinghead.skipNode is not None):
                        skipValue = intermediatePostinghead.skipNode.value
                        if(skipValue <= head2.value):
                            intermediatePostinghead =intermediatePostinghead.skipNode
                            continue
                        
                    intermediatePostinghead =intermediatePostinghead.nextNode    
                
                
                


            intermediatePostinghead = newPostingList.head        
            i=i+1
                   
    
    queryResults = dict()
    
    if(weightSort):
        finalList = newPostingList.weightSort()
    else:
        finalList = intermediatePostinghead
       
    while(finalList is not None):
        num_docs += 1
        num_results.append(finalList.value)
        finalList = finalList.nextNode
    



    

    queryResults["results"] = num_results
    queryResults["num_docs"] = num_docs
    queryResults["num_comparisons"] = num_comparisons

    #print(postingListLength,queryResults) 

    return queryResults


def mergeDAAT(invertedIndex,postingListLength,weightSort = False):

    num_comparisons = 0
    num_docs = 0
    num_results = []


    numberQueryTerms = len(postingListLength)
    intermediatePostinghead =  invertedIndex[postingListLength[0][0]].head


    i = 1 

    


    while i < numberQueryTerms:
            head2 = invertedIndex[postingListLength[i][0]].head
            newPostingList = project2.linkedList()
            

            while( head2 is not None and intermediatePostinghead is not None):

                if head2.value == intermediatePostinghead.value:
                    tf_idf = max(head2.tf_idf,intermediatePostinghead.tf_idf)
                    newPostingList.insert(intermediatePostinghead.value,tf_idf)
                    head2 = head2.nextNode
                    intermediatePostinghead =   intermediatePostinghead.nextNode
                   

                elif head2.value < intermediatePostinghead.value:
                    head2 = head2.nextNode

                elif   head2.value > intermediatePostinghead.value:
                    intermediatePostinghead =intermediatePostinghead.nextNode
                num_comparisons +=1    
            intermediatePostinghead = newPostingList.head        
            i=i+1
                   

    queryResults = dict()
    

    if(weightSort):
        finalList = newPostingList.weightSort()
    else:
        finalList = intermediatePostinghead
       
    while(finalList is not None):
        num_docs += 1
        num_results.append(finalList.value)
        finalList = finalList.nextNode
    



    queryResults["results"] = num_results
    queryResults["num_docs"] = num_docs
    queryResults["num_comparisons"] = num_comparisons


    return queryResults



        


     




def preProcess(query):
    ps = PorterStemmer()


    stop_words = set(stopwords.words('english'))

    documents = dict()


    
    line = query
    line = line.lower()
    line = re.sub("[^A-Za-z0-9\s]"," ",line)
    line = line.strip()
    wds = line.split()
    documents[1] = wds[:]

    noStopDocs = { key: ([item for item in documents[key] if not item in stop_words ] ) for key in documents}

    #lower_input_corpus = { key: ([item.lower() for item in documents[key]])  for key in documents}

    stemmedQuery = { key: ([ps.stem(item) for item in noStopDocs[key] ] ) for key in noStopDocs}

    return stemmedQuery

def getPostingsList(invertedIndex,query):
    postingList= dict()
    for key in query:
        for term in query[key]:
            postingList[term] = []
            temp = invertedIndex[term].head
            while temp is not None:
                postingList[term].append(temp.value)
                temp = temp.nextNode
    return postingList

def getPostingWithSkip(invertedIndex,query):
    postingList= dict()

    

    

    for key in query:
        for term in query[key]:
            postingList[term] = []
            if invertedIndex[term].length <= 2:
                continue
            temp = invertedIndex[term].head 
            postingList[term].append(temp.value)
            #invertedIndex[term].printPostingSkip()
            while temp is not None:
                if temp.skipNode is not None:
                    #print(temp.value,temp.skipNode.value)
                    postingList[term].append(temp.skipNode.value)
                    temp = temp.skipNode
                else:
                     temp = temp.nextNode    


    #print(postingList)            
    return postingList
    
def datWithoutSkip(invertedIndex,query,weightSort = False):

    for key in query:
        postingListlength = dict()
        for term in query[key]:
            postingListlength[term] = invertedIndex[term].length
        #print(postingListlength)

            
        temp = sorted([(v,k) for k,v in postingListlength.items()],reverse=False)
        #print(temp)
        sortedPostingTerms = [(v,k) for k,v in temp]

        #print(sortedPostingTerms[0][0])
        return mergeDAAT(invertedIndex,sortedPostingTerms,weightSort)


def datWithSkip(invertedIndex,query,weightSort = False):
     for key in query:
        postingListlength = dict()
        for term in query[key]:
            postingListlength[term] = invertedIndex[term].length
        #print(postingListlength)

            
        temp = sorted([(v,k) for k,v in postingListlength.items()],reverse=False)
        #print(temp)
        sortedPostingTerms = [(v,k) for k,v in temp]

        #print(sortedPostingTerms[0][0])
        return mergeSkipDAAT(invertedIndex,sortedPostingTerms,weightSort)        

        









                     

            
        






