from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch
import time

client = Elasticsearch(hosts=["127.0.0.1:9200"])

def search(request):
    return render(request,'search.html')

@csrf_exempt # 表示该视图可以被跨域访问
def result(request):

    keyword = request.GET.get('text')
    p = request.GET.get('page')
    zone = request.GET.get('zone')
    edu = request.GET.get('education')
    # educated = "来源"
    print(edu)
    if keyword is None or keyword == '0':
        return render(request,'search.html')
    try:
        p = int(p)
    except:
        p = 0
    educate = {'标题':'title','关键字': 'text', '来源': 'source', '作者': 'postBy'}
    educated = educate[""+ str(edu) + ""]
    print(educated)
    try:
        if keyword != '':
            must = {"query": keyword ,"fields":[educated]}
        else:
            return render(request,'search.html')
    except:
        must = {"query": keyword ,"fields":[educated]}

    query_body = {
            "query":{
                "multi_match": must
            },
        "size":10,
        "from":p*10,
        "highlight": {
            "pre_tags": ["<font style='color:red;font-size:20px'>"],
            "post_tags": ["</font>"],
            "fields": {
                "keyword": {"type": "plain"}
            }
        }
    }
    start_time = time.time()
    res = client.search(index="scrapy-2021",body=query_body)
    end_time = time.time()

    #############
    count = res['hits']['total']['value'] #计算20条结果
    times = '%.2f' % (end_time - start_time)   #用时多少秒
    hits = res['hits']['hits']     #放入框
    contents = []                  #框放文本

    #换页
    if p < 5:
        pages = [i for i in range(0,min(count//10+1 if count%10 == 0 else count//10,10))]
    elif p > count//10 - 5 :
        pages = [i for i in range(max(0,count//10-10),count//10+1 if count%10 else count//10)]
    else:
        pages= [i for i in range(p-5,p+5)]

    if educated:
        page_urls = [[i,'?text='+ str(keyword)  + '&education='+ str(edu) + '&page='+str(i)] for i in pages]
  
    elif (not educated) :
        page_urls = [[i,'?text='+ str(keyword) + '&education='+ str(edu) + '&page='+str(i)] for i in pages]
    contents = []
    for i in hits:
        temp = dict()
        temp['url'] = '/show/?id='+i['_id']
        if "http" not in i['_source']['taskName']:
            temp['logo'] = 'http:' + i['_source']['taskName']
        else:
            temp['logo'] = i['_source']['taskName']
        temp['postBy'] = i['_source']['postBy']
        temp['title'] = i['_source']['title']
        temp['source'] = i['_source']['source']
        temp['spider'] = i['_source']['spider']
        temp['spiderTags'] = i['_source']['spiderTags']
        temp['postOn'] = i['_source']['postOn']
        if len(i['_source']['text']) <= 250:
            temp['text'] = i['_source']['text']
        else:
            temp['text'] = i['_source']['text'][:250] + '...'
        contents.append(temp)
    return render(request,'result.html',locals())

def show(request):
    id = request.GET.get('id') # id 为elasticsearch 中的 编号id
    query = {"query": { "match": { "_id": id } }}
    print(query)
    res = client.search(index="scrapy-2021",body=query)
    content = res['hits']['hits'][0]['_source']
    return render(request,'show.html',locals())
