__author__ = 'wzy'
__date__ = '2020/2/26 15:01'

from django.urls import path

from .views import  OrgView,UserConsoleView,OrgHomeView,OrgCourseView,OrgTeacherView,OrgDescView,AddFavorView
from .views import TeacherListView, TeacherDetailView


urlpatterns = [
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_userconsole/', UserConsoleView.as_view(), name='add_userconsole'),
    path('home/<int:org_id>/', OrgHomeView.as_view(), name='org_home'),
    path('course/<int:org_id>/', OrgCourseView.as_view(), name='org_course'),
    path('org_teacher/<int:org_id>/', OrgTeacherView.as_view(), name='org_teacher'),
    path('desc/<int:org_id>/', OrgDescView.as_view(), name='org_desc'),
    path('add_fav/', AddFavorView.as_view(), name='add_fav'),
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/detail/<int:teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail'),
]