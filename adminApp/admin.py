from django.contrib import admin

# Register your models here.

from adminApp.models import Business,Component,Host,GrafanaUser,GrafanaFavorite,EsCluster
from adminApp.models import IndexRule,LogStructure
from adminApp.models import LogAlarmExpression,LogAlarmRule

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id','name','life_cycle')
    
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    
class HostAdmin(admin.ModelAdmin):
    list_display = ('id','ip','hostname','os')
    
class GrafanaUserAdmin(admin.ModelAdmin):
    list_display = ('id','name','password','user','folder_title','folder_id','folder_uid')

class GrafanaFavoriteAdmin(admin.ModelAdmin):
    list_display = ('id','title','url')
    
class EsClusterAdmin(admin.ModelAdmin):
    list_display = ('id','name','version','health','master','is_enabled')

class IndexRuleAdmin(admin.ModelAdmin):
    list_display = ('id','one_to_one','index_suffix','index_period')
    
class LogStructureAdmin(admin.ModelAdmin):
    list_display = ('id','name','type','enabled','default')

class LogAlarmRuleAdmin(admin.ModelAdmin):
    list_display = ('id','name','enabled')
    
admin.site.register(Business,BusinessAdmin)
admin.site.register(Component,ComponentAdmin)
admin.site.register(Host,HostAdmin)
admin.site.register(GrafanaUser,GrafanaUserAdmin)
admin.site.register(GrafanaFavorite,GrafanaFavoriteAdmin)
admin.site.register(EsCluster,EsClusterAdmin)
admin.site.register(IndexRule,IndexRuleAdmin)
admin.site.register(LogAlarmExpression)
admin.site.register(LogAlarmRule,LogAlarmRuleAdmin)
admin.site.register(LogStructure,LogStructureAdmin)