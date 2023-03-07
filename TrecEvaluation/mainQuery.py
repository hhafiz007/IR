from textwrap import indent
import json_to_trec as queryConverter
import re
from deep_translator import GoogleTranslator
from google_trans_new import google_translator
from langdetect import detect



def getFinalQuery1(query):
    boost = 1
    if(detect(query) == "en"):
      fQuery = f"text_en:("+GoogleTranslator(source="en",target ="en").translate(query)+") OR text_de:(" +GoogleTranslator(source="en",target = "de").translate(query)+") OR text_ru:("+GoogleTranslator(source="en",target = "ru").translate(query)+")"
      fQuery += " OR text_en:\""+GoogleTranslator(source="en",target ="en").translate(query)+"\" OR text_de:\"" +GoogleTranslator(source="en",target = "de").translate(query)+"\" OR text_ru:\""+GoogleTranslator(source="en",target = "ru").translate(query)+"\" "
      return fQuery
    elif(detect(query) == "de"):
      fQuery = f"text_en:("+GoogleTranslator(source="de",target = 'en').translate(query)+") OR text_de:("+GoogleTranslator(source="de",target = 'de').translate(query)+") OR text_ru:("+GoogleTranslator(source="de",target = 'ru').translate(query)+")"
      fQuery += " OR text_en:\""+GoogleTranslator(source="de",target ="en").translate(query)+"\" OR text_de:\"" +GoogleTranslator(source="de",target = "de").translate(query)+"\" OR text_ru:\""+GoogleTranslator(source="de",target = "ru").translate(query)+"\" "
      #fQuery = "text_en:("+query+")OR text_de:("+query+") OR text_ru:("+query+")"
      return fQuery
    elif(detect(query) == "ru"):
      fQuery = f"text_en:("+GoogleTranslator(source="ru",target = 'en').translate(query)+") OR text_de:("+GoogleTranslator(source="ru",target = 'de').translate(query)+") OR text_ru:("+GoogleTranslator(source="ru",target = 'ru').translate(query)+")"
      fQuery += " OR text_en:\""+GoogleTranslator(source="ru",target ="en").translate(query)+"\" OR text_de:\"" +GoogleTranslator(source="ru",target = "de").translate(query)+"\" OR text_ru:\""+GoogleTranslator(source="ru",target = "ru").translate(query)+"\" "

      #fQuery = "text_en:("+query+") OR text_de:("+query+") OR text_ru:("+query+")^2.2"
      return fQuery
    else:
       query = "Бильд. Внутренний документ говорит, что Германия примет 1,5 млн беженцев в этом году"
       #fQuery = "text_en:("+GoogleTranslator(source=detect(query) ,target = 'en').translate(query)+") OR text_de:("+GoogleTranslator(source=detect(query) ,target = 'de').translate(query)+") OR text_ru:("+GoogleTranslator(source=detect(query),target = 'ru').translate(query)+")"
       fQuery = "text_en:("+GoogleTranslator(source="ru",target = 'en').translate(query)+") OR text_de:("+GoogleTranslator(source="ru",target = 'de').translate(query)+") OR text_ru:("+GoogleTranslator(source="ru",target = 'ru').translate(query)+")"
       fQuery += " OR text_en:\""+GoogleTranslator(source="ru",target ="en").translate(query)+"\" OR text_de:\"" +GoogleTranslator(source="ru",target = "de").translate(query)+"\" OR text_ru:\""+GoogleTranslator(source="ru",target = "ru").translate(query)+"\" "
       return fQuery

def getFinalQuery(query):
    if(detect(query) == "en"):
      fQuery = "text_en:("+GoogleTranslator(source="en",target ="en").translate(query)+") OR text_de:(" +GoogleTranslator(source="en",target = "de").translate(query)+") OR text_ru:("+GoogleTranslator(source="en",target = "ru").translate(query)+")"
      return fQuery
    elif(detect(query) == "de"):
      fQuery = "text_en:("+GoogleTranslator(source="de",target = 'en').translate(query)+") OR text_de:("+GoogleTranslator(source="de",target = 'de').translate(query)+") OR text_ru:("+GoogleTranslator(source="de",target = 'ru').translate(query)+")"
      #fQuery = "text_en:("+query+")OR text_de:("+query+") OR text_ru:("+query+")"
      return fQuery
    elif(detect(query) == "ru"):
      fQuery = "text_en:("+GoogleTranslator(source="ru",target = 'en').translate(query)+") OR text_de:("+GoogleTranslator(source="ru",target = 'de').translate(query)+") OR text_ru:("+GoogleTranslator(source="ru",target = 'ru').translate(query)+")"
      #fQuery = "text_en:("+query+") OR text_de:("+query+") OR text_ru:("+query+")^2.2"
      return fQuery
    else:
       #query = "Бильд. Внутренний документ говорит, что Германия примет 1,5 млн беженцев в этом году"
       fQuery = "text_en:("+GoogleTranslator(source=detect(query) ,target = 'en').translate(query)+") OR text_de:("+GoogleTranslator(source=detect(query) ,target = 'de').translate(query)+") OR text_ru:("+GoogleTranslator(source=detect(query),target = 'ru').translate(query)+")"
       #fQuery = "text_en:("+GoogleTranslator(source="ru",target = 'en').translate(query)+") OR text_de:("+GoogleTranslator(source="ru",target = 'de').translate(query)+") OR text_ru:("+GoogleTranslator(source="ru",target = 'ru').translate(query)+")"
       return fQuery

translator = google_translator()


file_obj = open('queries_final.txt',encoding='utf-8')
data = file_obj.readlines()

q_indent = 'true'
q_fl=['id','score']
q_wt = 'json'
q_rows = 20
fQuery =""
cores = ['BM25','VSM']
q_qf= 'text_en'+' text_de'+ ' text_ru'
q_pf= 'text_en'+' text_de'+ ' text_ru'

for model in cores:
    for line in data:
        #line = re.sub("[^A-Za-z0-9\s]"," ",line)
        qid,_,query = line.partition(" ")
        print(int(qid))
        #print(query)
        #query = query.strip('\n').replace(':', '')
        query = query.replace(":"," ")
        query = query.replace("#"," ")
        #fQuery = "text_en:("+query+") OR text_de:("+query+") OR text_ru:("+query+")"
        fQuery = getFinalQuery1(query)
        print(fQuery)
        #fQuery+= "OR tweet_hashtags:("+query+")"
        #fQuery+= "OR tweet_urls:("+query+")"
        url = f"http://34.125.120.91:8983/solr/{model}/select?"
        print(url)
        queryConverter.getScore(url,model.lower(),qid,qf=q_qf,pf=q_pf,fl=q_fl,q=fQuery,indent=q_indent,wt=q_wt,rows=q_rows,defType='edismax')





