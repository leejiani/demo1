from django.db import models

# Create your models here.

class Classes(models.Model):
    name = models.CharField(max_length=20,verbose_name='班级')
    class Meta:
        verbose_name_plural = verbose_name = "班级"

class Student(models.Model):
    SEX_CHOICES = (('1','男'),('2','女'))
    name = models.CharField(max_length=20,verbose_name="姓名")
    age = models.IntegerField(null=False,blank=True,verbose_name="年龄")
    sex = models.IntegerField(choices=SEX_CHOICES,default=1,verbose_name="性别")
    classes = models.ForeignKey(Classes,related_name='students',
                                null=True,on_delete=models.SET_NULL,verbose_name="班级")
    phone = models.CharField(max_length=11,null=True)
    owner = models.ForeignKey('auth.User',related_name='students',null=True,on_delete=models.SET_NULL)
    class Meta:
        verbose_name_plural = verbose_name = "学生"

    def __str__(self):
        return f"{self.name}({self.pk})"


class Students(models.Model):
    sname = models.CharField(max_length=100)

    def __str__(self):
        return self.sname
