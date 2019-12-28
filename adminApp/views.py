
# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from adminApp.serializers import UserSerializer, GroupSerializer,BusinessSerializer
from adminApp.serializers import EsClusterSerializer,IndexRuleSerializer,LogStructureSerializer,\
LogAlarmRuleSerializer,LogAlarmExpressionSerializer

from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from adminApp.menus import get_menus
from adminApp.models import Business,IndexRule,EsCluster,LogStructure,LogAlarmRule,LogAlarmExpression
from adminApp.grafana_api import create_grafana_info

from rest_framework import status

class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    
    def post(self,request):
        tokenobj = Token.objects.filter(user_id=request.user.id).first()
        if not tokenobj:
            tokenobj = Token.objects.create(user=request.user)
        token = tokenobj.key
        if request.user.is_superuser:
            rolename = '管理员'
        else:
            rolename = '普通用户'
        return Response({'token':token,'role':rolename})

class AdminBusinessViewSet(viewsets.ModelViewSet):
    '''
    管理部分业务数据格式, 不需要host
    '''
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = self.format_data([serializer.data])
        return Response(data)
    
    def format_data(self,data):
        treelist = []
        for d in data:
            rootTree = {
                "text": d['name'],
                "node": "business",
                "icon": "fa fa-skyatlas red",
                "opened": True,
                "children": []
            }
            
            for component in d['components']:
                componentTree = {
                    "text": component['name'],
                    "node": "component",
                    "id": component['id'],
                    "icon": "fa fa-sitemap yellow",
                    "opened": False,
                    "children": []
                }
                rootTree['children'].append(componentTree)
            treelist.append(rootTree)
                
        return treelist

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = Business.objects.filter(users__in=[request.user])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = self.format_data([serializer.data])
        return Response(data)
    
    def format_data(self,data):
        treelist = []
        for d in data:
            rootTree = {
                "text": "",
                "node": "business",
                "icon": "fa fa-skyatlas red",
                "opened": True,
                "children": []
            }
            roottextstr = d['name']+' ({})'.format(len(d['components']))
            rootTree['text'] = roottextstr
            for component in d['components']:
                componentTree = {
                    "text": "",
                    "node": "component",
                    "icon": "fa fa-sitemap yellow",
                    "opened": False,
                    "children": []
                }
                componenttextstr = component['name']+' ({})'.format(len(component['hosts']))
                componentTree['text'] = componenttextstr
                idnum = 1
                for host in component['hosts']:
                    hostdict = {'icon':'fa fa-television blue','node':'host'}
                    hostdict['id'] = idnum
                    hostdict['text'] = host['ip']
                    componentTree['children'].append(hostdict)
                rootTree['children'].append(componentTree)
            treelist.append(rootTree)
                
        return treelist

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        '''
        用户创建时，先调用grafana api, 创建 grafana user, folder, 成功后再创建用户, 如果失败就返回error
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class IndexRuleViewSet(viewsets.ModelViewSet):
    queryset = IndexRule.objects.all()
    serializer_class = IndexRuleSerializer
    
class EsClusterViewSet(viewsets.ModelViewSet):
    queryset = EsCluster.objects.all()
    serializer_class = EsClusterSerializer
    
class LogStructureViewSet(viewsets.ModelViewSet):
    queryset = LogStructure.objects.all()
    serializer_class = LogStructureSerializer
    
    def get_queryset(self):
        '''
        重写get_queryset方法, 支持接收get 参数,过滤queryset
        '''
        queryset = LogStructure.objects.all()
        query_dict = {}
        for key in self.request.query_params.keys():
            value=self.request.query_params.get(key,None)
            if value is not None:
                query_dict[key]=value

        queryset = queryset.filter(**query_dict)
        return queryset


class LogAlarmRuleViewSet(viewsets.ModelViewSet):
    queryset = LogAlarmRule.objects.all()
    serializer_class = LogAlarmRuleSerializer
    
    def perform_update(self, serializer):
        '''
        重写更新, 如果request.method = PATCH and request.data.has_key('enabled'), 通知关键字告警程序,删除或推送告警规则
        '''
        print(self.request.method,self.request.data)
        serializer.save()
    
    def get_queryset(self):
        '''
        重写get_queryset方法, 支持接收get 参数,过滤queryset
        '''
        if self.request.user.is_superuser:
            queryset = LogAlarmRule.objects.filter()
        else:
            queryset = LogAlarmRule.objects.filter(owner=self.request.user)
        query_dict = {}
        for key in self.request.query_params.keys():
            value=self.request.query_params.get(key,None)
            if value is not None:
                query_dict[key]=value

        queryset = queryset.filter(**query_dict)
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        '''
        重写retrieve, 对部分返回数据格式化, 符合前端渲染
        1 通知方式变成 list
        2 通知用户 'notifier': [2] => 'notifier':[{id:2,name:'yangxu'}]
        3 格式化expressions
        '''
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['notify_way'] = data['notify_way'].split(',')
        data['notifier'] = [{'id':1,'name':'admin'}]
        data['expressions'] = []
        expression_queryset = LogAlarmExpression.objects.filter(rule=data['id'])
        for tmp_queryset in expression_queryset:
            tmp_id = tmp_queryset.expression_id
            tmp_expression = {}
            tmp_expression['expression_id'] = tmp_id
            tmp_expression['field'+tmp_id] = tmp_queryset.field
            tmp_expression['operator'+tmp_id] = tmp_queryset.operator
            tmp_expression['value'+tmp_id] = tmp_queryset.value
            data['expressions'].append(tmp_expression)
            
        return Response(data)
    
    def create(self, request, *args, **kwargs):
        """
        重写create, 对post data进行部分格式调整
        """
        data = request.data
        data['notifier'] = [user['id'] for user in data['notifier']]
        data['notify_way'] = ','.join(data['notify_way'])
        data['owner'] = request.user.id
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid()
            self.perform_create(serializer)
        except:
            status = False
            message = serializer.errors
        else:
            status = True
            message = None
            self.save_expression(data) #告警规则保存成功再保存表达式, 表达式依赖 规则ID
        return Response({'status':status,'message':message})
    
    def save_expression(self,data):
        rule_instance = LogAlarmRule.objects.get(name=data['name'])
        expression_list = []
        for expression in data['expressions']:
            expression_id = expression['expression_id']
            obj = LogAlarmExpression(
                rule = rule_instance,
                expression_id = expression_id,
                field = expression['field'+expression_id],
                operator = expression['operator'+expression_id],
                value = expression['value'+expression_id]
                )
            expression_list.append(obj)
        LogAlarmExpression.objects.bulk_create(expression_list)
        
class LogAlarmExpressionViewSet(viewsets.ModelViewSet):
    queryset = LogAlarmExpression.objects.all()
    serializer_class = LogAlarmExpressionSerializer
    
    def get_queryset(self):
        '''
        重写get_queryset方法, 支持接收get 参数,过滤queryset
        '''
        queryset = LogAlarmExpression.objects.all()
        query_dict = {}
        for key in self.request.query_params.keys():
            value=self.request.query_params.get(key,None)
            if value is not None:
                query_dict[key]=value

        queryset = queryset.filter(**query_dict)
        return queryset

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

RoutersTable = [
    {'name':'admin', 'path': '/admin', 'children':[
        {'name':'business','path': 'business'},
        {'name':'host','path': 'host'},
        {'name':'structure','path': 'structure'},
        {'name':'user','path': 'user'},
        {'name':'system','path': 'system'},
        {'name':'newDatasource','path': 'newDatasource'}
        ]
    },
    {'name':'log', 'path': '/log', 'redirect':{ 'name': 'search' }, 'children':[
        {'name':'search','path': 'search'},
        {'name':'analysis','path': 'analysis'},
        {'name':'newDashboard','path':'analysis/new'},
        {'name':'viewDashboard','path':'analysis/view'},
        {'name':'importDashboard','path':'analysis/import'},
        {'name':'join','path':'join'},
        {'name':'transmit','path':'transmit'},
        {'name':'alarmset','path':'alarmset'},
        {'name':'alarmcreate','path':'alarmset/create'},
        {'name':'alarmedit','path':'alarmset/edit'},
        {'name':'alarmlist','path':'alarmlist'}
        ]
    }
]

class RoutersMenus(APIView):
    def get(self,request):
        menus = get_menus(request.user.is_superuser)
        return Response({'routers':RoutersTable,'menus':menus})
        