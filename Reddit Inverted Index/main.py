import json
import project2
import query_method
import query_response



def getResponse(queries):

    invertedIndex = project2.createInvertedIndex()
    ''''
    query = {
        "queries" : ["the novel coronavirus","from an epidemic to a pandemic","is hydroxychloroquine effective?"]
    }
    '''

    #processedQuery = query_method.preProcess(query['queries'][3])

    #postingList = query_method.datWithSkip(invertedIndex,processedQuery)


    finalPostingListSkipless = dict()
    finalDaatSkipless = dict()
    finalPostingListSkip = dict()
    finalDaatSkip = dict()
    finalIdfSkipless = dict()
    finalIdfSkip = dict()



    for query in queries:

        processedQuery = query_method.preProcess(query)

        postingSkiplessTemp = query_method.getPostingsList(invertedIndex,processedQuery)
        finalPostingListSkipless = query_response.finalPostingList(postingSkiplessTemp,finalPostingListSkipless)




        daatSkiplessTemp = query_method.datWithoutSkip(invertedIndex,processedQuery)
        finalDaatSkipless = query_response.finalQueryList(daatSkiplessTemp,query,finalDaatSkipless)

        postingSkipTemp = query_method.getPostingWithSkip(invertedIndex,processedQuery)
        finalPostingListSkip= query_response.finalPostingList(postingSkipTemp,finalPostingListSkip)

        daatSkipTemp = query_method.datWithSkip(invertedIndex,processedQuery)
        finalDaatSkip= query_response.finalQueryList(daatSkipTemp,query,finalDaatSkip)

        daatIdfSkipless = query_method.datWithoutSkip(invertedIndex,processedQuery,True)
        finalIdfSkipless = query_response.finalQueryList(daatIdfSkipless,query,finalIdfSkipless)

        daatIdfSkip = query_method.datWithSkip(invertedIndex,processedQuery,True)
        finalIdfSkip = query_response.finalQueryList(daatIdfSkip,query,finalIdfSkip)


        

    response = query_response.createResponse(finalPostingListSkipless,finalPostingListSkip,finalDaatSkipless,finalDaatSkip,finalIdfSkipless,finalIdfSkip)
    responseBody =json.dumps(response)
    return responseBody

