__author__ = 'wzy'
__date__ = '2020/2/29 17:18'

from django.urls import path

from .views import UserListView,UploadImageView,UpdatePwdView,SendEmailcodeView,UpdateEmailView,UserCourseView,FavorCourseView,FavorOrgView,FavorTeacherView,MessageView


urlpatterns = [
    path('list/', UserListView.as_view(), name='user_list'),
    path('upload_image/', UploadImageView.as_view(), name='upload_image'),
    path('update_pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    path('sendemail_code/', SendEmailcodeView.as_view(), name='sendemail_code'),
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    path('mycourse/', UserCourseView.as_view(), name='mycourse'),
    path('fav_course/', FavorCourseView.as_view(), name='fav_course'),
    path('fav_teacher/', FavorTeacherView.as_view(), name='fav_teacher'),
    path('fav_org/', FavorOrgView.as_view(), name='fav_org'),
    path('mymessage/', MessageView.as_view(), name='mymessage'),
]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'