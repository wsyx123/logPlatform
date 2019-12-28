'''
一个查询必须 range_condition
term_condition 是点击组件时才有，query_condition 在搜索时才会有
'''
import datetime
import time

from adminApp.models import IndexRule,Business

def today_datetime():
    '''
    获取今天 00:00:00 时刻
    '''
    nowtime = datetime.datetime.now()
    num_hours = nowtime.hour
    num_minutes = nowtime.minute
    num_seconds = nowtime.second
    num_microseconds = nowtime.microsecond
    begin_dtime = datetime.datetime.now()-datetime.timedelta(
        hours=num_hours,minutes=num_minutes,
        seconds=num_seconds,microseconds=num_microseconds
        )
    return begin_dtime

def thisyear_datetime():
    '''
    获取今年1月1日 00:00:00 时刻
    '''
    bissextile = [31,60,91,121,152,182,213,244,274,305,335,366]    #leap year
    commonYear =[31,59,90,120,151,181,212,243,273,304,334,365]
    nowtime = datetime.datetime.now()
    num_year = nowtime.year
    num_month = nowtime.month
    num_day = nowtime.day
    
    if (num_year%100 !=0) and (num_year %4 == 0 ) or (num_year%400 == 0):
        if num_month > 1 :
            passed = bissextile[num_month-1] + num_day -1
        else:
            passed = num_day -1
    else:
        if num_month > 1 :
            passed = commonYear[num_month-1] + num_day -1
        else:
            passed = num_day -1
    
    begin_dtime = today_datetime() - datetime.timedelta(days=passed)
    return begin_dtime


def generate_thirteen_timestamp(timestr):
    if 'minutes' in timestr:
        number = int(timestr.split()[1])
        begin_dtime = datetime.datetime.now()-datetime.timedelta(minutes=number)
        
    elif 'hour' in timestr:
        number = int(timestr.split()[1])
        begin_dtime = datetime.datetime.now()-datetime.timedelta(hours=number)
        
    elif 'days' in timestr:
        number = int(timestr.split()[1])
        begin_dtime = datetime.datetime.now()-datetime.timedelta(days=number)
        
    elif 'Today' in timestr:
        begin_dtime = today_datetime()
        
    elif 'Yesterday' in timestr:
        begin_dtime = today_datetime() - datetime.timedelta(days=1)
        now_dtime = today_datetime() - datetime.timedelta(seconds=1)
        
    elif 'week' in timestr:
        '''
        this week
        获取这个星期 00:00:00 时刻  星期一到星期日
        '''
        nowtime = datetime.datetime.now()
        num_weekday = nowtime.weekday()
        begin_dtime = today_datetime() - datetime.timedelta(days=num_weekday)

    elif 'month' in timestr:
        '''
        this month
        '''
        nowtime = datetime.datetime.now()
        num_weekday = nowtime.day - 1
        begin_dtime = today_datetime() - datetime.timedelta(days=num_weekday)
    
    elif 'This year' in timestr:
        '''
        this year
        '''
        begin_dtime = thisyear_datetime()
        
    elif 'Last 1 year' in timestr:
        '''
        统一使用365天
        '''
        begin_dtime = datetime.datetime.now()-datetime.timedelta(days=364)
    
    else:
        '''
        默认today
        '''
        begin_dtime = today_datetime()
        
    #dtime = datetime.datetime.now()-datetime.timedelta(minutes=1) #Last 15 minutes
    begin_seconds = int(time.mktime(begin_dtime.timetuple()) * 1000 + begin_dtime.microsecond/1000)
    if 'Yesterday' in timestr:
        now_dtime = today_datetime() - datetime.timedelta(seconds=1)
    else:
        now_dtime = datetime.datetime.now()
    now_seconds = int(time.mktime(now_dtime.timetuple()) * 1000 + now_dtime.microsecond/1000)
    return (begin_seconds,now_seconds)


def generate_term_condition(querydata):
    '''
    {'business': 1,        业务id,通过此id获取业务简称
    'nodeParent': None,    
    'nodeKey': 1, 
    'nodeVal': None,
    'time': 'Last 15 minutes', 
    'searchStr': None, 
    'interval': 'a', 
    'size': 10, 
    'page': 1}
    
    elasticsearch使用term 搜索时, 大写情况需要转成小写,不然匹配不到
    '''
    indexrule = IndexRule.objects.all()
    if indexrule[0].one_to_one:
        if querydata['nodeKey'] == 'business':
            return []
        elif querydata['nodeKey'] == 'component':
            component_name = querydata["nodeVal"].split()[0]
            return [
                {"term":{"component":component_name.lower()}}
                ]
        else:
            component_name = querydata["nodeParent"].split()[0]
            return [
                {"term":{"component":component_name.lower()}},
                {"term":{"host":querydata["nodeVal"]}}
                ]
    else:
        businessobj = Business.objects.get(id=querydata['business'])
        if querydata['nodeKey'] == 'business':
            return [{"term":{"business":businessobj.shortname.lower()}}]
        elif querydata['nodeKey'] == 'component':
            component_name = querydata["nodeVal"].split()[0]
            return [
                {"term":{"business":businessobj.shortname.lower()}},
                {"term":{"component":component_name.lower()}}
                ]
        else:
            component_name = querydata["nodeParent"].split()[0]
            return [
                {"term":{"business":businessobj.shortname.lower()}},
                {"term":{"component":component_name.lower()}},
                {"term":{"host":querydata["nodeVal"]}}
                ]
        

def generate_query_condition(querydata):
    if querydata['searchStr']:
        querystring = {"query_string":{
                        "query":querydata['searchStr'],
                        "analyze_wildcard":True,
                        "default_field":"*"
                        }
                    }
        return querystring
    else:
        return False

def generate_range_condition(querydata):
    timestamp = generate_thirteen_timestamp(querydata['time'])
    timestr = querydata['time']
    range_condition = {
                    "range":{
                        "@timestamp":{
                            "gte":timestamp[0],
                            "lte":timestamp[1],
                            "format":"epoch_millis"
                        }
                    }
                }
    return range_condition

def generate_format(querydata):
    interval = querydata['interval']
    if interval == 'y':
        formatstr = 'yyyy-MM'
    elif interval == 'M':
        formatstr = 'MM-dd HH:mm'
    else:
        formatstr = 'yyyy-MM-dd HH:mm:ss'
    return formatstr

def generate_aggs_condition(querydata):
    timestr = querydata['time']
    if querydata['interval'] == 'a':
        if 'minutes' in timestr:
            intervalstr = '5m'
            formatstr = 'HH:mm:ss'
            
        elif 'hour' in timestr:
            intervalstr = '10m'
            formatstr = 'HH:mm'
            
        elif 'days' in timestr:
            intervalstr = '1d'
            formatstr = 'yyyy-MM-dd'
            
        elif 'Today' in timestr:
            intervalstr = '10m'
            formatstr = 'HH:mm'
            
        elif 'Yesterday' in timestr:
            intervalstr = '1h'
            formatstr = 'HH:mm'
            
        elif 'week' in timestr:
            intervalstr = '1h'
            formatstr = 'yyyy-MM-dd HH'
    
        elif 'month' in timestr:
            intervalstr = '12h'
            formatstr = 'yyyy-MM-dd HH'
        
        elif 'This year' in timestr:
            intervalstr = '1d'
            formatstr = 'yyyy-MM-dd'
            
        elif 'Last 1 year' in timestr:
            intervalstr = '1d'
            formatstr = 'yyyy-MM-dd'
        
    else:
        intervalstr = '1'+querydata['interval']
        formatstr = generate_format(querydata)
    aggs = {
            "groupDate":{
              "date_histogram":{
                "field":"@timestamp",
                "interval": intervalstr,
                "time_zone":"Asia/Shanghai",
                "format": formatstr
                }
            }
        }
    return aggs

def generate_highlight_condition(querydata):
    highlight = {
            "pre_tags":[
                "<span style='background-color:yellow;'>"
            ],
            "post_tags":[
                "</span>"
            ],
            "fields":{
                "*":{
    
                }
            },
            "fragment_size":2147483647
        }
    return highlight

def generate_query_body(querydata):
    item = generate_term_condition(querydata)
    query = generate_query_condition(querydata)
    timerange = generate_range_condition(querydata)
    aggs = generate_aggs_condition(querydata)
    highlight = generate_highlight_condition(querydata)
    query_body = {
        "from": 0,
        "size":querydata['size'],
        "sort": [
            {"@timestamp":{"order":"desc"}}
        ],
        "query":{
            "bool":{
                "must":[]
            }
        }
        
    }
    query_body['query']['bool']['must'].append(timerange)
    if item:
        query_body['query']['bool']['must'].extend(item)
    if query:
        query_body['query']['bool']['must'].append(query)
        query_body['highlight'] = highlight
    query_body['aggs'] = aggs
    return query_body



def generate_count_query_body(querydata):
    item = generate_term_condition(querydata)
    query = generate_query_condition(querydata)
    timerange = generate_range_condition(querydata)
    query_body = {
        "query":{
            "bool":{
                "must":[]
            }
        }
    }
    if item:
        query_body['query']['bool']['must'].extend(item)
    if query:
        query_body['query']['bool']['must'].append(query)
    query_body['query']['bool']['must'].append(timerange)
    return query_body