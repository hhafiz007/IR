# -*- coding: utf-8 -*-



import json
# if you are using python 3, you should
#import urllib.request
import urllib.request
import requests


# change the url according to your own corename and query
def getScore(inurl,model,queryId,**params):
    #inurl = "http://34.125.120.91:8983/solr/BM25/select?q=text_en%3AWegen Flüchtlingskrise: Angela Merkel stürzt in Umfragen&fl=id%2Cscore&wt=json&indent=true&rows=20"
    #inurl = inurl.replace(" ", "%20")
    outfn = f'{model}/{int(queryId)}.txt'
    #outfn = f'{model}_output.txt'


    # change query id and IRModel name accordingly
    qid = queryId
    IRModel=model #either bm25 or vsm
    outf = open(outfn, 'a+')
    response = requests.get(inurl,params)
    print(response.content.decode())
    #data =  urllib.request.urlopen(inurl)
    # if you're using python 3, you should use
    # data = urllib.request.urlopen(inurl)
    
    docs = json.loads(response.content.decode())['response']['docs']
    # the ranking should start from 1 and increase
    rank = 1
    for doc in docs:
        outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
        rank += 1
    outf.close()
    
