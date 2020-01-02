#!/usr/bin/env python

from django.contrib.auth.models import User,Group
from adminApp.models import Business,Component,Host,EsCluster,IndexRule,LogStructure,\
LogAlarmRule,LogAlarmExpression
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    class Meta:
        model = User
        #fields = ['id','url', 'username', 'email', 'groups']
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        
class ComponentHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['ip']

class BusinessUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        
class BusinessComponentSerializer(serializers.ModelSerializer):
    hosts = ComponentHostSerializer(many=True)
    class Meta:
        model = Component
        fields = ['id','name','hosts']
        depth = 1

class BusinessSerializer(serializers.ModelSerializer):
    users = BusinessUserSerializer(many=True)
    components = BusinessComponentSerializer(many=True)
    class Meta:
        model = Business
        fields = ['id','name','shortname','life_cycle','create_time','components','users']
        depth = 2

class IndexRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexRule
        fields = '__all__'

class EsClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EsCluster
        fields = '__all__'
        depth = 1
        
class LogStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogStructure
        fields = '__all__'
        
class LogAlarmRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAlarmRule
        fields = '__all__'

class LogAlarmExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAlarmExpression
        fields = '__all__'