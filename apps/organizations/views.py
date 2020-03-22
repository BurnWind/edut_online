from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger,Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import CourseOrg,City,Teacher
from .forms import UserConsoleForm
from operation.models import UserCollect
from courses.models import Course


class OrgView(View):
    '''
    课程机构列表功能
    '''
    def get(self, request):
        all_citys = City.objects.all()
        all_orgs = CourseOrg.objects.all()
        hot_orgs = CourseOrg.objects.order_by('-click')[:3]

        # 机构全局搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = CourseOrg.objects.filter(Q(name__contains=search_keywords)|
                                                  Q(desc__contains=search_keywords))

        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        kind = request.GET.get('ct', '')
        if kind:
            all_orgs = all_orgs.filter(kind=kind)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)
        org_num = all_orgs.count()
        return render(request, 'org-list.html',
                      {
                          'all_city' : all_citys,
                          'all_org' : orgs,
                          'org_num' : org_num,
                          'city_id' : city_id,
                          'kind' : kind,
                          'sort' : sort,
                          'hot_orgs' : hot_orgs
                      })


class UserConsoleView(View):
    def post(self, request):
        console_form = UserConsoleForm(request.POST)
        if console_form.is_valid():
            console_form.save(commit=True)
            return JsonResponse({"status" : "success"})
        else:
            return JsonResponse({"status" : "fail", "msg" : "添加出错"})


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        current_page = 'home'
        org = CourseOrg.objects.get(id=org_id)
        org.click += 1
        org.save()
        has_Fav = False
        if request.user.is_authenticated:
            if UserCollect.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_Fav = True
        all_courses = org.courses.all()[:3]
        all_teachers = org.teachers.all()[:1]

        return render(request, 'org-detail-homepage.html',
                      {
                          'all_courses' : all_courses,
                          'all_teachers' : all_teachers,
                          'course_org' : org,
                          'current_page' : current_page,
                          'has_Fav' : has_Fav,
                      })


class OrgCourseView(View):
    '''
    机构课程页
    '''
    def get(self, request, org_id):
        current_page = 'course'
        org = CourseOrg.objects.get(id=org_id)
        all_courses = org.courses.all()
        has_Fav = False
        if request.user.is_authenticated:
            if UserCollect.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_Fav = True
        return render(request, 'org-detail-course.html',
                      {
                          'all_courses' : all_courses,
                          'course_org' : org,
                          'current_page' : current_page,
                          'has_Fav': has_Fav,
                      })


class OrgTeacherView(View):
    '''
    机构讲师页
    '''
    def get(self, request, org_id):
        current_page = 'teacher'
        org = CourseOrg.objects.get(id=org_id)
        all_teachers = org.teachers.all()
        has_Fav = False
        if request.user.is_authenticated:
            if UserCollect.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_Fav = True
        return render(request, 'org-detail-teachers.html',
                      {
                          'all_teachers' : all_teachers,
                          'course_org' : org,
                          'current_page' : current_page,
                          'has_Fav': has_Fav,
                      })


class OrgDescView(View):
    '''
    机构介绍页
    '''
    def get(self, request, org_id):
        current_page = 'desc'
        org = CourseOrg.objects.get(id=org_id)
        has_Fav = False
        if request.user.is_authenticated:
            if UserCollect.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_Fav = True
        return render(request, 'org-detail-desc.html',
                      {
                          'course_org' : org,
                          'current_page' : current_page,
                          'has_Fav': has_Fav,
                      })


class AddFavorView(View):
    '''
    用户收藏，取消收藏
    '''
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            return JsonResponse({"status": "fail", "msg": "用户未登录"})
        records = UserCollect.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if records:
            '''
            取消收藏
            '''
            records.delete()
            if fav_type == '1':
                course = Course.objects.get(id=fav_id)
                course.favor -= 1
                if course.favor <= 0:
                    course.favor = 0
                course.save()
            elif fav_type == '2':
                course_org = CourseOrg.objects.get(id=fav_id)
                course_org.favor -= 1
                if course_org.favor <= 0:
                    course_org.favor = 0
                course_org.save()
            elif fav_type == '3':
                teacher = Teacher.objects.get(id=fav_id)
                teacher.favor -= 1
                if teacher.favor <= 0:
                    teacher.favor = 0
                teacher.save()
            return JsonResponse({"status": "success", "msg": "收藏"})
        else:
            '''
            收藏
            '''
            if int(fav_id) > 0 and int(fav_type) in [1,2,3]:
                collect = UserCollect()
                collect.user = request.user
                collect.fav_type = int(fav_type)
                collect.fav_id = int(fav_id)
                collect.save()
                if fav_type == '1':
                    course = Course.objects.get(id=fav_id)
                    course.favor += 1
                    course.save()
                elif fav_type == '2':
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.favor += 1
                    course_org.save()
                elif fav_type == '3':
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.favor += 1
                    teacher.save()
                return JsonResponse({"status": "success", "msg": "已收藏"})
            else:
                return JsonResponse({"status": "fail", "msg": "收藏出错"})


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        hot_teachers = Teacher.objects.order_by('-click')[:5]

        # 讲师全局搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = Teacher.objects.filter(Q(name__contains=search_keywords)|
                                                  Q(work_company__contains=search_keywords)|
                                                  Q(work_position__contains=search_keywords))

        teachers_num = all_teachers.count()
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 2, request=request)
        all_teachers = p.page(page)
        return render(request, 'teachers-list.html',
                      {
                        "all_teachers" : all_teachers,
                        "hot_teachers" :  hot_teachers,
                        "sort" : sort,
                        "teachers_num" : teachers_num,
                      })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        courses = Course.objects.filter(teacher=teacher)
        hot_teachers = Teacher.objects.order_by('-click')[:5]

        hasFav_teacher = False
        hasFav_org = False
        if request.user.is_authenticated:
            if UserCollect.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3):
                hasFav_teacher = True
            elif UserCollect.objects.filter(user=request.user, fav_id=teacher.courseorg.id, fav_type=2):
                hasFav_org = True

        return render(request, 'teacher-detail.html', {
            "teacher" : teacher,
            "courses" : courses,
            "hot_teachers": hot_teachers,
            "hasFav_teacher" : hasFav_teacher,
            "hasFav_org" : hasFav_org,
        })
