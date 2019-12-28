"""logPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from adminApp import views
from dataApp.views import LogSearch,Dashboards

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'index', views.IndexRuleViewSet)
router.register(r'clusters', views.EsClusterViewSet)
router.register(r'structure', views.LogStructureViewSet)
router.register(r'alarmrule', views.LogAlarmRuleViewSet)
router.register(r'expression', views.LogAlarmExpressionViewSet)
router.register(r'business', views.BusinessViewSet)
router.register(r'admin/business', views.AdminBusinessViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('menus/',views.RoutersMenus.as_view()),
    path('login/',views.LoginView.as_view()),
    path('log/',LogSearch.as_view()),
    path('dashboards/',Dashboards.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
