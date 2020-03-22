__author__ = 'wzy'
__date__ = '2020/2/26 15:01'

from django.urls import path

from .views import CourseView,CourseDetailView,AddFavorView,CourseVideoView,CourseCommentView,AddCommentView


urlpatterns = [
    path('list/', CourseView.as_view(), name='course_list'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('add_fav/', AddFavorView.as_view(), name='add_favor'),
    path('video/<int:course_id>/', CourseVideoView.as_view(), name='course_video'),
    path('comment/<int:course_id>/', CourseCommentView.as_view(), name='course_comment'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
]