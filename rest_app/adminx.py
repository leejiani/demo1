
# 将现有模型纳入管理
import xadmin
from rest_app.models import Classes,Student

xadmin.site.register(Classes)

# 自定义管理类
# 利用装饰器注册Student类
@xadmin.sites.register(Student)
class StudentAdminx(object):
    list_display = ["name","age","sex"]


# xadmin.site.register(Student,StudentAdminx)