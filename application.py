from flask import Flask
from flask import request
from flask import json
import string
from flask import jsonify
from newsapi.newsapi_exception import NewsAPIException
from newsapi.newsapi_client import NewsApiClient
import os
import datetime

 
title_list=[]
url_list=[]
description_list=[]
imageurl=[]

'''headlines details'''

newsapi = NewsApiClient(api_key="c747f9b3847443a8a69714fd926d1d15")
top_headlines = newsapi.get_top_headlines(q=None ,language='en',country='us',page_size=30)
#print(top_headlines)

#print(top_headlines)
tph=[]
for x in top_headlines['articles']:
    dat= x
    if dat['author']!=None and dat['publishedAt']!=None and dat['title']!=None and dat['description']!=None and dat['url']!=None and dat['urlToImage']!=None:
        dat2= dat['source']
        if dat2['id']!=None and dat2['name']!=None:
            tph.append(dat)

#print(tph)
#print(json.dumps(tph))

newsapi = NewsApiClient(api_key='c747f9b3847443a8a69714fd926d1d15')
cnn_top_headlines = newsapi.get_top_headlines(q=None,sources='cnn' ,language='en',page_size=30)
#print(cnn_top_headlines)

ctph=[]
for x in cnn_top_headlines['articles']:
    dat= x
    if dat['author']!=None and dat['publishedAt']!=None and dat['title']!=None and dat['description']!=None and dat['url']!=None and dat['urlToImage']!=None:
        dat2= dat['source']
        if dat2['id']!=None and dat2['name']!=None:
            ctph.append(dat)

newsapi = NewsApiClient(api_key='c747f9b3847443a8a69714fd926d1d15')
fox_top_headlines = newsapi.get_top_headlines(q=None,sources='fox-news' ,language='en',page_size=30)
#print(fox_top_headlines)

ftph=[]
for x in fox_top_headlines['articles']:
    dat= x
    if dat['author']!=None and dat['publishedAt']!=None and dat['title']!=None and dat['description']!=None and dat['url']!=None and dat['urlToImage']!=None:
        dat2= dat['source']
        if dat2['id']!=None and dat2['name']!=None:
            ftph.append(dat)



i=0;
for x in top_headlines['articles']:
    title_list.insert(i,x['title'])
    url_list.insert(i,x['urlToImage'])
    description_list.insert(i,x['description'])
    imageurl.insert(i,x['url'])
    i=i+1
    
'''for x in range(len(title_list)):
    print("title")
    print(title_list[x])
    print("url")
    print(url_list[x])
    print("description")
    print(description_list[x])
    print("\n")
    print("\n")
    print("\n")'''


application = Flask(__name__)

@application.route('/top_headlines')
def getheadlines():
  return jsonify(tph)

@application.route('/cnn_top_headlines')
def getcnnheadlines():
  return jsonify(ctph)


@application.route('/fox_top_headlines')
def getfoxheadlines():
  return jsonify(ftph)


'''word cloud '''

ans_list = []
words = {}

#making list of each word
for i in title_list:
    myList = i.split()
    for j in myList:
        for char in string.punctuation:
            j = j.strip(char)
        if len(j) == 0:
            continue
        ans_list.append(j)

#counting frequency of each word
for i in ans_list:
    if i in words:
        words[i] += 1
    else:
        words[i] = 1

#print(words)
#sorting dictionary to get most frequent word
sorted_words = dict(sorted(words.items(), key=lambda kv: kv[1], reverse = True))
#print(sorted_words)
#print(len(sorted_words))

#print("\n \n")

file = open('stopwords_en.txt', 'r')
stop_words = file.readlines()

#formatting stop words
for i in range(0,len(stop_words)):
    stop_words[i] = stop_words[i].strip('\n')
    stop_words[i] = stop_words[i].strip('\r')
    stop_words[i] = stop_words[i].lower()

#print(stop_words)
#print(sorted_words)
#print("\n\n")

temp_dict = sorted_words.copy()

#removing stopwords
for key_word,freq in temp_dict.items():
    if key_word.lower() in stop_words:
        del sorted_words[key_word]

#print(sorted_words)
#print(len(sorted_words))

#print("\n \n")

freq_words = {}
#30 most frequent words
for word,freq in sorted_words.items():
    freq_words[word]=freq
    if len(freq_words) == 30:
        break;

#print(freq_words)

freq_list=[]
for word,freq in freq_words.items():
    freq_list.append([freq,word])
    
    
#print(freq_list)
#print(json.dumps(freq_list))

sources = newsapi.get_sources(language='en',country='us')
#sources = json.dumps(sources)
#print(sources);

source_list = list(sources['sources'])

#for data in source_list:
#    print(data['id'])
#print(source_list)
#print(len(source_list))

#source_temp = source_list.copy()

for i in range(0, len(source_list)):
    data = dict(source_list[i])
    data['id'] = data['id'].encode('ascii','ignore')
    data['name'] = data['name'].encode('ascii','ignore')
    #print(data['id'])
    if data['id'] == "None" or data['name'] == "None" :
        #print("None detected")
        del source_list[i]
        
#print(source_list)
#print("aaaaa")

form_list={}
for data in source_list:
    data = dict(data)
    data['id'] = data['id'].encode('ascii','ignore')
    data['name'] = data['name'].encode('ascii','ignore')
    if data['name'] not in form_list:
        form_list[data['name']] = []
        form_list[data['name']].append(data['id'])
    

#print(form_list)

source = {}

for data in source_list:
    data = dict(data)
    data['category'] = data['category'].encode('ascii','ignore')
    data['name'] = data['name'].encode('ascii','ignore')
    if data['category'] not in source:
        source[data['category']] = []
        source[data['category']].append(data['name'])
    else:
        source[data['category']].append(data['name'])
    
    
#print(source['health'])

'''
reta_dict = {}
reta_dict['business'] = source['business']
print(json.dumps(reta_dict))
'''
        
'''
ret_dict = {}
ret_dict[category_sent_from_JS] = source['category']
return json.dumps(ret_dict)
'''

#print(source)
@application.route('/sourcesall')
def getallsources():
    global source;
    rect_dict={}
    rect_dict['all'] = []
    for key, data in source.items():
        for val in data:
            rect_dict['all'].append(val)
    return jsonify(rect_dict)
    

@application.route('/sources')
def getsources():
    global source
    ret_dict = {}
    category = request.args.get('category')
    print(category)
    #category= category.encode('ascii','ignore')
    if category != "all" :
        ret_dict[category] = source[category]
    else:
        ret_dict[category] = []
        for key, data in source.items():
            for val in data:
                ret_dict[category].append(val)
    return json.dumps(ret_dict)
'''
keyword_form='abc';
source_form='all';
from_form='2020-03-01'
to_form='2020-03-01'
newsapi = NewsApiClient(api_key="c747f9b3847443a8a69714fd926d1d15")
'''

foundsource=''
@application.route('/geteverything')
def geteverything():
    keyword_form=request.args.get('q')
    keyword_form= keyword_form.encode('ascii','ignore')
    #print(keyword_form)
    from_form=request.args.get('from')
    
    from_form= from_form.encode('ascii','ignore')
    #console.log(from_form)
    format_str = '%Y-%m-%d'
    # The format
    datetime_obj = datetime.datetime.strptime(from_form, format_str)
    #print(datetime_obj.date())
    #fromdate=datetime_obj.date()
    #print(type(fromdate))
    #print(from_form)
    #print(type(from_form))
    to_form=request.args.get('to')
    to_form= to_form.encode('ascii','ignore')
    datetime_obj2 = datetime.datetime.strptime(to_form, format_str)
    #print(datetime_obj2.date())
    todate=datetime_obj2.date()
    #print(to_form)
    source_form=request.args.get('source')
    source_form= source_form.encode('ascii','ignore')
    #print(source_form)
    founds='all'
    for key,value in form_list.items():
        if key==source_form:
            foundsource= form_list.get(key)
            for x in foundsource:
                founds=x;
    newsapi = NewsApiClient(api_key="c747f9b3847443a8a69714fd926d1d15")
    #print(founds)
    try:
        if founds == 'all':
            all_articles = newsapi.get_everything(q=keyword_form,from_param=from_form,to=to_form, language='en', sort_by='publishedAt',page_size=30)
        else:
            all_articles = newsapi.get_everything(q=keyword_form,sources=founds,from_param=from_form,to=to_form, language='en', sort_by='publishedAt',page_size=30)
            
    except NewsAPIException as e:
        #print(str(e.get_message()))
        return e.get_message()
    #print(all_articles)
    form_datas=all_articles['articles']
    #print(form_datas)
    datas= list(form_datas)
    #print(len(datas))
    #print datas
    another=[]
    for i in range(0,len(datas)):
        data = dict(datas[i])
        #data['description'] = data['description'].encode('ascii','ignore')
        #data['author'] = data['author'].encode('ascii','ignore')
        #print(data['author'])
        if data['author'] != None and data['description'] != None and len(data['author'])!=0 and data['urlToImage']!= None and data['title']!= None and data['url']!=None and len(data['description'])!=0 and data['urlToImage']!="null" :
            another.append(data)
    #print(another)
    #print(len(another))
    return (json.dumps(another));

@application.route('/words')
def getwords():
  return (json.dumps(freq_list))
  
@application.route("/")
def get_index():
    return application.send_static_file('aaaa.html')

if __name__ == "__main__":
    application.debug = True
    application.run()



