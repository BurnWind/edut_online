from django.shortcuts import render
from django.views.generic import View
from pure_pagination import PageNotAnInteger,Paginator
from django.http import JsonResponse
from django.db.models import Q

from .models import Course
from operation.models import UserCollect,UserCourse,CourseComment
from organizations.models import CourseOrg,Teacher
from util.mixin_util import LoginRequiredMixin


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = Course.objects.order_by('-click')[:3]

        # 课程全局搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = Course.objects.filter(Q(name__contains=search_keywords)|
                                                  Q(desc__contains=search_keywords)|
                                                  Q(detail__contains=search_keywords))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students_num')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        all_courses = p.page(page)
        return render(request, 'course-list.html',
                      {
                        "all_courses" : all_courses,
                        "hot_courses" : hot_courses,
                        "sort" : sort,
                      })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click += 1
        course.save()
        hasfav_course = False
        hasfav_org = False
        if request.user.is_authenticated:
            if UserCollect.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                hasfav_course = True
            if UserCollect.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=2):
                hasfav_org = True
        tag =  course.tag
        if tag:
            related_courses = Course.objects.filter(~Q(id=int(course_id)), tag=tag)[:2]
        else:
            related_courses = []

        return render(request, 'course-detail.html',
                      {
                          "course" : course,
                          "related_courses" : related_courses,
                          "hasfav_course" : hasfav_course,
                          "hasfav_org" : hasfav_org,
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


class CourseVideoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        #
        # if not request.user.is_authenticated:
        #     return render(request, 'login.html')

        usercourse = UserCourse.objects.filter(user=request.user, course=course)
        if not usercourse:
            course.students_num += 1
            course.save()
            usercourse = UserCourse(user=request.user, course=course)
            usercourse.save()

        courseuser = UserCourse.objects.filter(course=course)
        #取出该课程所有用户id
        course_user_ids = [user.id for user in courseuser]
        #取出所有课程id
        all_usercourses = UserCourse.objects.filter(user_id__in=course_user_ids)
        all_courseid = [user_course.course.id for user_course in all_usercourses]
        #有关课程
        related_courses = Course.objects.filter(id__in=all_courseid).order_by("-click")[:5]
        if not related_courses:
            related_courses = []
        return render(request, 'course-video.html',
                      {
                          "course" : course,
                          "related_courses" : related_courses,
                      })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course_comment = course.coursecomments.all()
        return render(request, 'course-comment.html',
                      {
                          "course" : course,
                          "course_comment" : course_comment,
                      })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"status" : "fail", "msg" : "用户未登录"})

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course = Course.objects.get(id=course_id)
            course_comment = CourseComment(user=request.user, course=course, comments=comments)
            course_comment.save()
            return JsonResponse({"status": "success", "msg" : "添加失败"})
        else:
            return JsonResponse({"status": "success", "msg" : "添加失败"})