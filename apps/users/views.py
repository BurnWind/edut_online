from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from pure_pagination import Paginator,PageNotAnInteger
from django.urls import reverse

from users.models import UserProfile,EmailVerifyRecord,Banner
from users.forms import  LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,UploadImageForm,updateUserForm
from util.email_send import send_email_code
from util.mixin_util import LoginRequiredMixin
from operation.models import UserCourse,UserCollect,UserMessage
from courses.models import Course
from organizations.models import CourseOrg,Teacher

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveView(View):
    def get(self, request, active_code):
        email_record = EmailVerifyRecord.objects.filter(code=active_code)
        if email_record:
            for record in email_record:
                user = UserProfile.objects.get(email=record.email)
                user.is_active = True
                user.save()
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form' : register_form})
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form' : register_form, 'msg': '用户已存在'})
            pass_word = request.POST.get('password', '')
            re_user = UserProfile()
            re_user.username = user_name
            re_user.email = user_name
            re_user.password = make_password(pass_word)
            re_user.is_active = False
            re_user.save()

            usermessage = UserMessage()
            usermessage.message = "欢迎注册慕学在线网"
            usermessage.user = re_user
            usermessage.save()

            send_email_code.delay(user_name)
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form' : register_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if not user.is_active:
                    return render(request, 'login.html', {'msg': '用户名未激活'})
                login(request, user)
                return redirect(reverse('index'))
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ForgetPwdView(View):
    '''
    找回密码
    '''
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form' : forgetpwd_form})
    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            user_name = request.POST.get('email', '')
            user = UserProfile.objects.filter(email=user_name)
            if not user:
                return render(request, 'forgetpwd.html', {'msg' : '用户不存在'})
            send_email_code(user_name, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


class ResetPwdView(View):
    def get(self, request, reset_code):
        records = EmailVerifyRecord.objects.filter(code=reset_code)
        if records:
            for r in records:
                email = r.email
            return render(request, 'password_reset.html', {'email' : email})


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg' : '密码输入不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'modify_form' : modify_form})


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'mylist'
        return render(request, 'usercenter-info.html', {
            "user" : request.user,
            "current_page": current_page,
        })
    def post(self, request):
        up_userForm = updateUserForm(request.POST, instance=request.user)
        if up_userForm.is_valid():
            up_userForm.save()
            return JsonResponse({"status" : "success"})
        else:
            return JsonResponse(up_userForm.errors)



class UploadImageView(LoginRequiredMixin, View):
    '''
    修改头像
    '''
    def post(self, request):
        imageForm = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if imageForm.is_valid():
            imageForm.save(commit=True)
            return JsonResponse({"status" : "success"})
        else:
            return JsonResponse({"status" : "fail"})


class UpdatePwdView(LoginRequiredMixin, View):
    '''
    修改密码
    '''
    def post(self, request):
        UpPwdForm = ModifyPwdForm(request.POST)
        if UpPwdForm.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1!=pwd2:
                return JsonResponse({"status" : "fail", "msg" : "密码不一致"})
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return JsonResponse({"status" : "success"})
        else:
            return JsonResponse(UpPwdForm.errors)


class SendEmailcodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return JsonResponse({"email" : "邮箱已存在"})
        send_email_code(email, 'get_code')
        return JsonResponse({"status": "success"})


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type='get_code'):
            user = request.user
            user.email = email
            user.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"email": "验证码出错"})


class UserCourseView(LoginRequiredMixin, View):
    '''
    我的课程
    '''
    def get(self, request):
        current_page = 'mycourse'
        user_courses = UserCourse.objects.filter(user=request.user)
        courses = [user_course.course for user_course in user_courses]
        return render(request, 'usercenter-mycourse.html', {
            "courses" : courses,
            "current_page": current_page,
        })


class FavorCourseView(LoginRequiredMixin, View):
    '''
    我收藏的课程
    '''
    def get(self, request):
        current_page = 'myfav'
        user_collects = UserCollect.objects.filter(user=request.user, fav_type=1)
        course_ids = [user_collect.fav_id for user_collect in user_collects]
        courses = Course.objects.filter(id__in=course_ids)
        return render(request, 'usercenter-fav-course.html',{
            "courses" : courses ,
            "current_page": current_page,
        })


class FavorTeacherView(LoginRequiredMixin, View):
    '''
    我收藏的讲师
    '''

    def get(self, request):
        current_page = 'myfav'
        user_collects = UserCollect.objects.filter(user=request.user, fav_type=3)
        teacher_ids = [user_collect.fav_id for user_collect in user_collects]
        teachers = Teacher.objects.filter(id__in=teacher_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            "teachers" : teachers,
            "current_page" : current_page,
        })


class FavorOrgView(LoginRequiredMixin, View):
    '''
    我收藏的机构
    '''

    def get(self, request):
        current_page = 'myfav'
        user_collects = UserCollect.objects.filter(user=request.user, fav_type=2)
        org_ids = [user_collect.fav_id for user_collect in user_collects]
        orgs = CourseOrg.objects.filter(id__in=org_ids)
        return render(request, 'usercenter-fav-org.html', {
            "orgs" : orgs,
            "current_page": current_page,
        })


class MessageView(LoginRequiredMixin, View):
    '''
    我的消息
    '''
    def get(self, request):
        current_page = 'mymessage'
        messages = UserMessage.objects.filter(user=request.user)

        #清空未读消息为已读
        all_messages = UserMessage.objects.filter(user=request.user, has_read=False)
        for message in all_messages:
            message.has_read = True
            message.save()

        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, 3, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            "messages" : messages,
            "current_page" : current_page,
        })


class IndexView(View):
    '''
    首页
    '''
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "all_banners" : all_banners,
            "courses" : courses,
            "banner_courses" : banner_courses,
            "orgs" : orgs,
        })


def page_not_found(request, exception):
    '''
    全局处理404函数
    '''
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def page_error(request):
    '''
    全局处理500函数
    '''
    response =render_to_response('500.html')
    response.status_code = 500
    return response