__author__ = 'wzy'
__date__ = '2020/2/23 19:22'

import xadmin
from .models import UserMessage,UserCollect,UserConsole,UserCourse,CourseComment

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user__nick_name', 'message', 'has_read', 'add_time']


class UserCollectAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user__nick_name', 'fav_id', 'fav_type', 'add_time']


class UserConsoleAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course',]
    list_filter = ['user__nick_name', 'course__name', 'add_time']


class CourseCommentAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments',]
    list_filter = ['user__nick_name', 'course__name', 'comments', 'add_time']


xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserConsole, UserConsoleAdmin)
xadmin.site.register(UserCollect, UserCollectAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
