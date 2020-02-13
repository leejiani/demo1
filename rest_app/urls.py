from django.urls import path
from . import views

app_name = "rest_app"

urlpatterns = [
    path('students/',views.StudentView.as_view(),name='student'),
    path('students/<int:pk>/',views.StudentDetailView.as_view(),name='students_detail'),
    # path('students/<str:version>/<int:pk>/',views.StudentDetailView.as_view(),name='students_detail'),

    path('classes/',views.classes,name='classes'),
    path('classes/<int:pk>/',views.classes_detail,name='classes_detail'),

    path('user/',views.UserView.as_view(),name="user_view"),
    path('user/<int:pk>/',views.UserDetailView.as_view(),name="user_detail_view")
]

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns(urlpatterns)