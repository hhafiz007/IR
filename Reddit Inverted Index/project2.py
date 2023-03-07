import nltk
nltk.download('stopwords')
import math


#my_dict = { key: ([item.lower() for item in my_dict[key]] if type(my_dict[key]) == type([]) else my_dict[key])  for key in my_dict}
# This box is for Pre Processing
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stemmedDocs = dict()

# Here I will be creating the linked list which will be my posting list
class linkedListNode:
    def __init__(self,value,tf_idf,nextNode=None):
        self.value = value
        self.termFrequency = 0
        self.nextNode = None
        self.skipNode = None
        self.tf = None
        self.idf = None
        self.tf_idf = tf_idf

class linkedList:
    def __init__(self,head=None,tail = None):
        self.head = head
        self.tail = tail
        self.length = 0
    def insert(self,value,tf_idf=None):
        node = linkedListNode(value,tf_idf)
        if self.head is None:
            self.head = node
            self.tail = node
        else :
            self.tail.nextNode = node
            self.tail = node
        self.length +=1     
        return node    
    def print(self):
        currentNode = self.head
        while currentNode is not None:
            print(currentNode.value,currentNode.tf_idf)
            currentNode = currentNode.nextNode
    def findMid(self,head) :
        if head is None :
            return None
        slow, fast = head, head
        while fast.nextNode is not None and fast.nextNode.nextNode is not None :
            slow = slow.nextNode
            fast = fast.nextNode.nextNode
        return slow
    def merge(self,head1, head2):
        if(head1 is None):
            return head2
        if(head2 is None):
            return head1
        newHead, newTail = None, None
        if head1.value < head2.value :
            newHead = head1
            newTail = head1
            head1 = head1.nextNode
        else :
            newHead = head2
            newTail = head2
            head2 = head2.nextNode
        while head1 is not None and head2 is not None :
            if head1.value < head2.value :
                newTail.nextNode = head1
                newTail = newTail.nextNode
                head1 = head1.nextNode
            else :
                newTail.nextNode = head2
                newTail = newTail.nextNode
                head2 = head2.nextNode
        if head1 is not None :
            newTail.nextNode = head1
        if head2 is not None :
            newTail.nextNode = head2
        return newHead 
    def mergeSortHelper(self,head):
        if head is None or head.nextNode is None :
            return head
        mid = self.findMid(head)
        half1 = head
        half2 = mid.nextNode
        mid.nextNode = None
        half1 = self.mergeSortHelper(half1)
        half2 = self.mergeSortHelper(half2)
        finalHead = self.merge(half1, half2)
        return finalHead
    def mergeSort(self):
        self.head = self.mergeSortHelper(self.head)

    def weightedMerge(self,head1, head2):
        if(head1 is None):
            return head2
        if(head2 is None):
            return head1
        newHead, newTail = None, None
        if head1.tf_idf > head2.tf_idf :
            newHead = head1
            newTail = head1
            head1 = head1.nextNode
        elif head1.tf_idf < head2.tf_idf:
            newHead = head2
            newTail = head2
            head2 = head2.nextNode
        elif  head1.value < head2.value :
            newHead = head1
            newTail = head1
            head1 = head1.nextNode
        else:
            newHead = head2
            newTail = head2
            head2 = head2.nextNode  



        while head1 is not None and head2 is not None :
            if head1.tf_idf > head2.tf_idf :
                newTail.nextNode = head1
                newTail = newTail.nextNode
                head1 = head1.nextNode
            elif head1.tf_idf < head2.tf_idf :
                newTail.nextNode = head2
                newTail = newTail.nextNode
                head2 = head2.nextNode
            elif head1.value < head2.value :
                newTail.nextNode = head1
                newTail = newTail.nextNode
                head1 = head1.nextNode
            else :
                newTail.nextNode = head2
                newTail = newTail.nextNode
                head2 = head2.nextNode    

        if head1 is not None :
            newTail.nextNode = head1
        if head2 is not None :
            newTail.nextNode = head2
        return newHead    

    def weightedSortHelper(self,head):
        if head is None or head.nextNode is None :
            return head
        mid = self.findMid(head)
        half1 = head
        half2 = mid.nextNode
        mid.nextNode = None
        half1 = self.weightedSortHelper(half1)
        half2 = self.weightedSortHelper(half2)
        finalHead = self.weightedMerge(half1, half2)
        return finalHead    

    def weightSort(self):
        self.head = self.weightedSortHelper(self.head)
        #self.print()
        return self.head   

    def skipLength(self):
        return round(math.sqrt(self.length))
            

    def addSkips(self):
        skipLength = int(self.skipLength())
        if skipLength == 1:
            return 
        
        currentNodeWithSkip = self.head
        temp = self.head.nextNode
        nodePosition = 1

        while temp is not None: 
            if(nodePosition % skipLength == 0):
                 currentNodeWithSkip.skipNode = temp
                 currentNodeWithSkip = temp
            nodePosition += 1
            temp = temp.nextNode

    def printPostingSkip(self):
        print(self.head.value)
        temp = self.head

        while temp is not None:
            if temp.skipNode is not None:
                print(temp.skipNode.value)
                temp = temp.skipNode
            else :
                temp = temp.nextNode    

    def weightDocument(self,stemmedDocs):
        temp = self.head


        while temp is not None:
            temp.tf = temp.termFrequency/len(stemmedDocs[temp.value])
            temp.idf = len(stemmedDocs)/ self.length
            temp.tf_idf = temp.tf*temp.idf
            #print(temp.value,stemmedDocs[temp.value],temp.tf,temp.idf,temp.tf_idf)
            temp = temp.nextNode







                     



                   



 


def preProcess(stemmedDocs):
    ps = PorterStemmer()


    stop_words = set(stopwords.words('english'))

    input_corpus = open('input_corpus.txt', encoding="utf8")
    documents = dict()


    

    for line in input_corpus:
        line = line.lower()
        line = re.sub("[^A-Za-z0-9\s]"," ",line)
        line = line.strip()
        wds = line.split()
        documents[int(wds[0])] = wds[1:]

    noStopDocs = { key: ([item for item in documents[key] if not item in stop_words ] ) for key in documents}


    #lower_input_corpus = { key: ([item.lower() for item in documents[key]])  for key in documents}


    stemmedDocs = { key: ([ps.stem(item) for item in noStopDocs[key] ] ) for key in noStopDocs}

    return stemmedDocs


def createInvertedIndex():
    #print("hi")
    stemmedDocs = dict()
    stemmedDocs = preProcess(stemmedDocs)    
    termFrequency = dict()
    invertedIndex = dict()


    for doc in stemmedDocs:
        temp = dict()
        for term in stemmedDocs[doc]:
            if term not in invertedIndex:
                termFrequency[term] = 1
                postingListStart = linkedList()
                invertedIndex[term] = postingListStart
                currNode=postingListStart.insert(doc)
                temp[term] = currNode
                currNode.termFrequency = 1
            else :    
                if term in temp:
                    temp[term].termFrequency += 1
                    termFrequency[term] +=1
                else:
                    termFrequency[term] +=1
                    currNode = invertedIndex[term].insert(doc)
                    temp[term] = currNode
                    currNode.termFrequency = 1
    temp = dict()

    for term in invertedIndex:
        invertedIndex[term].mergeSort()
        invertedIndex[term].addSkips()
        invertedIndex[term].weightDocument(stemmedDocs)

    return invertedIndex    
        

createInvertedIndex()
         