"""edut_online URL Configuration

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
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from django.views.static import serve
from datetime import timedelta
from edut_online.settings import MEDIA_ROOT
import xadmin
from users.views import LoginView,RegisterView,ActiveView,ForgetPwdView,ResetPwdView,ModifyPwdView,LogoutView,IndexView


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('captcha/', include('captcha.urls')),
    path('active/<str:active_code>/', ActiveView.as_view(), name='user_active'),
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    path('reset/<str:reset_code>/', ResetPwdView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd' ),

    #课程机构url配置
    path('org/', include(('organizations.urls', 'organizations'), namespace="org")),
    #配置上传文件的访问处理函数
    re_path(r'media/(?P<path>.*)$', serve, {'document_root' : MEDIA_ROOT}),
    # re_path(r'static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    # 课程url配置
    path('course/', include(('courses.urls', 'courses'), namespace="course")),
    #个人中心url配置
    path('users/', include(('users.urls', 'users'), namespace="user")),
]
