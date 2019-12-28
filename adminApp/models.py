from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Business(models.Model):
    lifecycle = (
        (1,'测试'),
        (2,'上线'),
        (3,'下线')
        )
    name = models.CharField(max_length=32,verbose_name='业务名称')
    shortname = models.CharField(max_length=32,verbose_name='业务简称')
    # 表示外键关联到用户表,当用户表删除了该条数据,该表中不删除,仅仅是把外键置空
    users = models.ManyToManyField(to=User)
    components = models.ManyToManyField(to='Component',blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    life_cycle = models.IntegerField(choices=lifecycle)
    def __str__(self):
        return self.name

class Component(models.Model):
    name = models.CharField(max_length=32,unique=True,verbose_name='组件名称')
    hosts = models.ManyToManyField(to='Host',blank=True)
    def __str__(self):
        return self.name

class Host(models.Model):
    os_type = (
        (1,'Linux'),
        (2,'Windows'),
        (3,'Other')
        )
    ip = models.GenericIPAddressField(unique=True)
    hostname = models.CharField(max_length=64,null=True,blank=True)
    os = models.IntegerField(choices=os_type,default=3)
    create_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.ip
    
class EsHost(models.Model):
    host = models.GenericIPAddressField(unique=True)
    
class EsCluster(models.Model):
    health_option = (
        (1,'red'),
        (2,'yellow'),
        (3,'green')
        )
    name = models.CharField(max_length=64,verbose_name='集群名',blank=True)
    version = models.CharField(max_length=32,verbose_name='版本',blank=True)
    health = models.IntegerField(choices=health_option,default=3)
    master = models.GenericIPAddressField()
    hosts = models.ManyToManyField(to=EsHost,blank=True)
    is_enabled = models.BooleanField()
    
class IndexRule(models.Model):
    '''
    索引规则
    '''
    index_period_option=(
        (1,'daily'),
        (2,'monthly'),
        (3,'yearly')
        )
    one_to_one = models.BooleanField() #一个业务一个索引
    index_suffix = models.CharField(max_length=64,verbose_name='索引后缀')
    index_period = models.IntegerField(choices=index_period_option,default=2)

class GrafanaUser(models.Model):
    name = models.CharField(max_length=32,unique=True,verbose_name='用户名')
    password = models.CharField(max_length=64,verbose_name='密码')
    folder_title = models.CharField(max_length=32,verbose_name='文件夹名称')
    folder_id = models.IntegerField(verbose_name='文件夹id')
    folder_uid = models.CharField(max_length=32,verbose_name='文件夹uid')
    user = models.CharField(max_length=32,verbose_name='日志系统用户')
    
class GrafanaFavorite(models.Model):
    title = models.CharField(max_length=255,verbose_name='仪表盘名称')
    url = models.CharField(max_length=255,verbose_name='链接')

class LogStructure(models.Model):
    name_type = (
        (1,'Integer'),
        (2,'String')
        )
    business = models.ManyToManyField(to=Business)
    component = models.ManyToManyField(to=Component,blank=True)
    name = models.CharField(max_length=64,verbose_name='字段名称')
    type = models.IntegerField(choices=name_type)
    description = models.CharField(max_length=128,verbose_name='说明')
    enabled = models.BooleanField(verbose_name='已启用')
    default = models.BooleanField(verbose_name='默认字段')

class APINotifyWayColumn(models.Model):
    field = models.CharField(max_length=32,verbose_name='字段名')
    type = models.CharField(max_length=32,verbose_name='字段类型')
    description = models.CharField(max_length=64,verbose_name='说明') 

class APINotifyWay(models.Model):
    name = models.CharField(max_length=32,verbose_name='通知方式')
    field = models.ManyToManyField(to=APINotifyWayColumn,blank=True)
    enabled = models.BooleanField()

class LogAlarmRule(models.Model):
    depth_option = (
        (1,'业务级别'),
        (2,'组件级别')
        )
    level_option = (
        (1,'低'),
        (2,'中'),
        (3,'高')
        )
    date_option = (
        (1,'工作日'),
        (2,'全年')
        )
    time_type_option = (
        (1,'全天'),
        (2,'工作时段')
        )
    name = models.CharField(max_length=64,verbose_name='告警规则名')
    description = models.CharField(max_length=128,verbose_name='描述',blank=True,null=True)
    business = models.ForeignKey(to=Business,verbose_name='所属业务',on_delete=models.CASCADE)
    alarm_depth = models.IntegerField(choices=depth_option,verbose_name='告警深度')
    component = models.IntegerField(verbose_name='组件ID',blank=True,null=True)
    level = models.IntegerField(choices=level_option,verbose_name='告警级别')
    title = models.CharField(max_length=255,verbose_name='告警标题')
    message = models.TextField(verbose_name='告警内容')
    alarm_date = models.IntegerField(choices=date_option,verbose_name='告警周期')
    #告警时段
    time_type = models.IntegerField(choices=time_type_option,verbose_name='时段类型')
    start_time = models.TimeField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    #告警压缩
    compress_enabled = models.BooleanField(verbose_name='压缩启用')
    total_time = models.IntegerField(verbose_name='时间窗口',blank=True,null=True)
    interval_time = models.IntegerField(verbose_name='时间间隔',blank=True,null=True)
    total_number = models.IntegerField(verbose_name='告警总次数',blank=True,null=True)
    logic_expression = models.CharField(max_length=64,verbose_name='告警表达式')
    notifier = models.ManyToManyField(to=User,verbose_name='通知用户')
    notify_way = models.CharField(max_length=64,verbose_name='通知方式')# 1 邮件, 2 短信, 3 API
    enabled = models.BooleanField(default=False,verbose_name='生效')
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='owner')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('name','business')

class LogAlarmExpression(models.Model):
    '''
    大于(gt) , 小于(lt), 等于(eq), 大于等于(ge), 小于等于(le), 不等于(ne)
    告警模块在判断时根据 operator把value转换成整型 
    '''
    rule = models.ForeignKey(to=LogAlarmRule,on_delete=models.CASCADE)
    expression_id = models.CharField(max_length=2,verbose_name='表达式标识')
    field = models.CharField(max_length=64,verbose_name='字段名')
    operator = models.CharField(max_length=3,verbose_name='运算符')
    value = models.CharField(max_length=64,verbose_name='关键字或阀值')