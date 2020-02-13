from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student, Classes

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']


class ClassesRelateField(serializers.RelatedField):
        def to_representation(self, value):
            return {'id':value.id,'name':value.name}


class StudentSerializer(serializers.ModelSerializer):
    # 新增所述 班级属性，通过第三方类实现
    classes = ClassesRelateField(read_only=True)
    # 增加只读功能
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Student
        # 指明要序列化的字段
        fields = ['id','name','age','sex','classes','owner']
        # fields = '__all__'
        # exclude 指明要排除的字段


class StudentSerializerV2(serializers.ModelSerializer):
    # 新增所述 班级属性，通过第三方类实现
    classes = ClassesRelateField(read_only=True)
    # 增加只读功能
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Student
        # 指明要序列化的字段
        fields = ['id','name','age','sex','classes','owner','phone']
        # fields = '__all__'
        # exclude 指明要排除的字段


class ClassesSerializer(serializers.ModelSerializer):
    # 新增所述 学生属性
    students = StudentSerializer(many=True,read_only=True)
    class Meta:
        model = Classes
        fields = ['id','name','students']