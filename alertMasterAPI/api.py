import requests
import json
from django.contrib.auth.models import User
from adminApp.models import AlertHost,LogAlarmRule,LogAlarmExpression,Business,Component,LogStructure
from adminApp.serializers import LogAlarmRuleSerializer,LogAlarmExpressionSerializer


def generate_rule_data(rule_id):
    '''
    1 表达式 expressions 需要生成
    2 notifier 需要生成 1 代表邮件, 2 代表短信
    3 把 business id 换成 business shortname, 把component(如果有) id 换成 component name
    '''
    
    rule_queryset = LogAlarmRule.objects.get(id=rule_id)
    rule_serializer = LogAlarmRuleSerializer(rule_queryset)
    rule_data = rule_serializer.data
    for key in ['create_time','update_time','description']:
        del rule_data[key]
    
    notify_way = rule_data['notify_way'].split(',')
    notifiers = rule_data['notifier']
    rule_data['notifier'] = []
    for way in notify_way:
        notifier = {}
        for user_id in notifiers:
            user_queryset = User.objects.get(id=user_id)
            if way == '1':
                notifier[1] = []
                notifier[1].append(user_queryset.email)
            else:
                notifier[2] = []
        rule_data['notifier'].append(notifier)
    
    business_id = rule_data['business']
    business_queryset = Business.objects.get(id=business_id)
    rule_data['business'] = business_queryset.shortname
    
    if rule_data['alarm_depth'] == 2 and rule_data['component']:
        component_id = rule_data['component']
        component_queryset = Component.objects.get(id=component_id)
        rule_data['component'] = component_queryset.name
    
    rule_data['expressions'] = []
    expression_query_set = LogAlarmExpression.objects.filter(rule=rule_queryset)
    for expression in expression_query_set:
        expression_dict = {}
        expression_dict['expression_id'] = expression.expression_id
        expression_dict['field'] = expression.field
        expression_dict['operator'] = expression.operator
        expression_dict['value'] = expression.value
        logstructure_queryset = LogStructure.objects.get(business__in=[business_id],name=expression.field)
        expression_dict['type'] = logstructure_queryset.type
        rule_data['expressions'].append(expression_dict)
    
    return rule_data    

def add_rule(rule_id):
    queryset = AlertHost.objects.get(enabled=True)
    host = queryset.host
    port = queryset.port
    url = 'http://'+host+':'+str(port)+'/rule/add'
    rule_data = generate_rule_data(rule_id)
    
    res = requests.post(url, data=json.dumps(rule_data))
    print(res.text)
    
def delete_rule(rule_id):
    queryset = AlertHost.objects.get(enabled=True)
    host = queryset.host
    port = queryset.port
    url = 'http://'+host+':'+str(port)+'/rule/delete'
    
    res = requests.post(url, data=json.dumps({"ruleid":rule_id}))
    print(res.text)
    
    
   
