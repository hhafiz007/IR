
from collections import OrderedDict

def finalPostingList(postingListCurrent,postingList):
    for term in postingListCurrent:
        if term not in postingList:
            postingList[term] = postingListCurrent[term]
     

    #finalPostingListTemp = sorted(postingList.items())
    #finalPostingList = {k:v for k,v in finalPostingListTemp} 
    return postingList


def finalQueryList(daatSkiplessTemp,query,finalDaatSkipless):
    finalDaatSkipless[query] = daatSkiplessTemp
    return finalDaatSkipless


def createResponse(finalPostingListSkipless,finalPostingListSkip,finalDaatSkipless,finalDaatSkip,finalIdfSkipless,finalIdfSkip):
    responseDict = dict()
    responseDict['postingsList'] =  finalPostingListSkipless
    responseDict['postingsListSkip'] =  finalPostingListSkip
    responseDict['daatAnd'] = finalDaatSkipless
    responseDict['daatAndSkip'] = finalDaatSkip
    responseDict['daatAndTfIdf'] = finalIdfSkipless
    responseDict['daatAndSkipTfIdf'] = finalIdfSkip

    return responseDict

