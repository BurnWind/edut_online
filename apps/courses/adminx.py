__author__ = 'wzy'
__date__ = '2020/2/23 19:34'

import xadmin
from .models import Course,Lesson,Video,Resource,BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ['course_org', 'name', 'desc', 'detail', 'degree', 'learn_time', 'click', 'favor', 'students_num', 'image', 'add_time']
    search_fields = ['course_org', 'name', 'desc', 'detail', 'degree', 'learn_time', 'click', 'favor', 'students_num', 'image']
    list_filter = ['course_org__name', 'name', 'desc', 'detail', 'degree', 'learn_time', 'click', 'favor', 'students_num', 'image', 'add_time']
    inlines = [LessonInline]

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    list_display = ['course_org', 'name', 'desc', 'detail', 'degree', 'learn_time', 'click', 'favor', 'students_num', 'image', 'add_time']
    search_fields = ['course_org', 'name', 'desc', 'detail', 'degree', 'learn_time', 'click', 'favor', 'students_num', 'image']
    list_filter = ['course_org__name', 'name', 'desc', 'detail', 'degree', 'learn_time', 'click', 'favor', 'students_num', 'image', 'add_time']

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'learn_times', 'add_time']
    search_fields = ['course', 'name', 'learn_times']
    list_filter = ['course__name', 'name', 'learn_times', 'add_time']


class VideoAdmin(object):
    ist_display = ['lesson', 'name', 'url', 'learn_times', 'add_time']
    search_fields = ['lesson', 'name', 'url', 'learn_times']
    list_filter = ['lesson__name', 'name', 'url', 'learn_times', 'add_time']


class ResourceAdmin(object):
    ist_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(Resource, ResourceAdmin)


