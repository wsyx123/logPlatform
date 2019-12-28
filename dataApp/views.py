from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch import Elasticsearch #  6.4.0
from elasticsearch import RequestError
from .search_condition import generate_query_body,generate_count_query_body
from adminApp.grafana_api import get_dashboards
from adminApp.models import EsCluster,Business
import json

class LogSearch(APIView):
    '''
    搜索日志,接收参数: 当前页号, 每页数, 当前记录最后一条的time
    '''
    
    def post(self,request):
        querydata = request.data
        #获取es master主机
        esqueryset = EsCluster.objects.get(is_enabled=True)
        esmaster = esqueryset.master
        eshosts = [esmaster+":9200"]
        #获取es 索引
        businessobj = Business.objects.get(id=querydata['business'])
        indexname = businessobj.shortname+'-*'
        
        query_body = generate_query_body(querydata)
        count_query_body = generate_count_query_body(querydata)
        if querydata['searchStr']:
            highlight = True
        else:
            highlight = False
        logdata = self.testdata(eshosts,indexname,query_body,count_query_body,highlight)
        return Response(logdata)
    
    def testdata(self,eshosts,indexname,query_body,count_query_body,highligth):
        es = Elasticsearch(eshosts)
        logtotal = es.count(indexname,body=count_query_body)
        logkey = es.indices.get_mapping(index=indexname)
        try:
            logdata = es.search(indexname,body=query_body)
        except RequestError:
            return {'status':False,'msg':'有不存在的field被当作条件查询'}
        logstatis = logdata['aggregations']['groupDate']['buckets']
        logstatis = self.generate_echart_data(logstatis)
        logdata = logdata['hits']['hits']
        logdata = self.format_logdata(logdata,highligth)

        logkey = self.get_key(logkey)
        return {'logkey':logkey,'logtotal':logtotal,'status':True,
                'logdata':logdata,'echart':logstatis}
        
    def get_key(self,logkey):
        for k,v in logkey.items():
            return v['mappings']['doc']['properties'].keys()
            
            
        
    def format_logdata(self,logdata,highflag):
        logdatalist = []
        for data in logdata:
            sourcedata = data['_source']
            if highflag:
                highlightdata = data['highlight']
                onedata = {}
                for key in highlightdata.keys():
                    onedata[key] = highlightdata[key][0]
                onedata = dict(sourcedata,**onedata)
                logdatalist.append(onedata)
            else:
                logdatalist.append(sourcedata)
        return logdatalist
    
    def generate_echart_data(self,aggdatas):
        xdata = []
        statisdata = []
        for aggdata in aggdatas:
            xdata.append(aggdata['key_as_string'])
            statisdata.append(aggdata['doc_count'])
        return {'xdata':xdata,'statisdata':statisdata}
    
class Dashboards(APIView):
    
    def get(self,request):
        url = 'http://localhost:8080/grafana/api/search?folderIds=4'
        auth=('yangxu','yangxu')
        res = get_dashboards(url,auth)
        if res.status_code == 200:
            jsondata = json.loads(res.text)
            dashboards = [{"title":data['title'],"url":data['url']} for data in jsondata]
        else:
            dashboards = []
        
        return Response(dashboards)

class DashboardsFavorite(APIView):
    pass
