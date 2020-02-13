from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from rest_app import throttles
from . import my_permissions
from rest_app.models import Student, Classes
from rest_app.serializers import StudentSerializer, ClassesSerializer, UserSerializer, StudentSerializerV2


# Create your views here.

# 高级优化
class StudentView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # 父类中包含get和post方法
    # 设置权限，在对应的view视图中增加属性
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # 限制节流
    throttle_classes = [throttles.AnonymousThrottle]
    # perform_create方法，在对应的serializer执行新增操作的时候，
    # 传入指定的owner=self.request.user
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.version == '2.0':
            return StudentSerializerV2
        return self.serializer_class


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    # serializer_class = StudentSerializer
    serializer_class = StudentSerializer
    # 使用内置节流类需要指定
    # throttle_scope = 'contacts'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,my_permissions.IsOwnerOrReadOnly]

    # 指定使用的节流类，标识匿名用户访问
    throttle_classes = [throttles.AnonymousThrottle]
    # throttle_classes = [UserRateThrottle]

    def get_serializer_class(self):
        if self.request.version == '2.0':
            return StudentSerializerV2
        return self.serializer_class

# 用户的创建
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



# 类视图的优化
# class StudentView(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
#
#
# class StudentDetailView(mixins.ListModelMixin,
#                         mixins.UpdateModelMixin,
#                         mixins.DestroyModelMixin,
#                         generics.GenericAPIView):
#
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
#
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
#
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)





# 基于类的视图
# class StudentView(APIView):
#     def get(self,request,format=None):
#         stu_li = Student.objects.all()
#         serializer = StudentSerializer(stu_li, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     def post(self,request,format=None):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

#
# class StudentDetailView(APIView):
#
#     def get_student(self,pk):
#         try:
#             return Student.objects.get(pk=pk)
#         except Student.DoesNotExist:
#             raise Http404
#
#     def get(self,pk):
#         student = self.get_student(pk)
#         serializer = StudentSerializer(student)
#         return Response(serializer.data)
#
#     def put(self,request,pk,format=None):
#         student = self.get_student(pk)
#         serializer = StudentSerializer(student, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self,pk,format=None):
#         student = self.get_student(pk)
#         student.delete()
#         # return JsonResponse(status=204)
#         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
# 基于函数的视图
# @csrf_exempt
def stduent(request, format=None):
    # get请求用于获取资源
    if request.method == "GET":
        students = Student.objects.all()
        serializer = StudentSerializer(students,many=True)
        return Response(serializer.data)
    # post请求用于新增资源
    elif request.method == "POST":
        # 利用 JSONParser 将request主体内容反序列化
        # data = JSONParser().parse(request)
        # 将上一步的字典数据，传入到 序列化类中
        # serializer_data = StudentSerializer(data=data)
        serializer = StudentSerializer(data=request.data)
        # 进行验证
        if serializer.is_valid():
            # 验证成功将数据保存到数据库中
            serializer.save()
            # 返回 201 状态码和刚刚新保存到数据库中的数据
            # return JsonResponse(serializer_data.data,status=201)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        # 验证失败，返回400错误
        # return JsonResponse(serializer_data.errors,status=400)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
@api_view(["GET","PUT","DELETE"])
def students_detail(request, pk, format=None):
    try:
        # 根据pk获取模型实例
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        # 如果pk指定的数据不存在返回404错误
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    # get请求
    if request.method == "GET":
        # 序列化
        serializer = StudentSerializer(student)
        # 返回Json数据
        # return JsonResponse(serializer.data)
        return Response(serializer.data)
    # put请求
    elif request.method == "PUT":
        # 使用JsonParser将request主体内容反序列化为字典
        # data = JSONParser().parse(request)
        # 将上一步的字典数据，传入到 序列化类中
        # serializer = StudentSerializer(student,data=data)
        serializer = StudentSerializer(student,data=request.data)
        # 验证
        if serializer.is_valid():
            # 保存数据到数据库
            serializer.save()
            # 默认状态码为200
            # return JsonResponse(serializer.data)
            return Response(serializer.data)
        # 验证失败,返回400错误
        # return JsonResponse(serializer.errors,status=400)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    # delete请求方式
    elif request.method == "DELETE":
        # 删除
        student.delete()
        # return JsonResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET","POST"])
def classes(request,format=None):
    if request.method == "GET":
        class_li = Classes.objects.all()
        serializer = ClassesSerializer(class_li,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # data = JSONParser().parse(request)
        serializer = ClassesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT","DELETE"])
def classes_detail(request,pk,format=None):
    try:
        classes_li = Classes.objects.get(pk=pk)
    except Student.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ClassesSerializer(classes_li)
        return Response(serializer.data)
    elif request.method == "PUT":
        # data = JSONParser().parse(request)
        serializer = StudentSerializer(classes_li,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        # 执行模型删除操作
        classes_li.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

