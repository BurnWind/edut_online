__author__ = 'wzy'
__date__ = '2020/2/23 18:30'

import xadmin
from .models import CourseOrg,City,Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['city', 'name', 'desc', 'add_time', 'favor', 'click', 'address', 'image']
    search_fields = ['city', 'name', 'desc', 'favor', 'click', 'address', 'image']
    list_filter = ['city__name', 'name', 'desc', 'add_time', 'favor', 'click', 'address', 'image']


class TeacherAdmin(object):
    list_display = ['courseorg', 'favor', 'click', 'name', 'work_years', 'work_company', 'work_position', 'points', 'add_time']
    search_fields = ['courseorg', 'favor', 'click', 'name', 'work_years', 'work_company', 'work_position', 'points']
    list_filter = ['courseorg__name', 'favor', 'click', 'name', 'work_years', 'work_company', 'work_position', 'points', 'add_time']

xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)