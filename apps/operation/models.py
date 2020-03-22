
from datetime import  datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course

# Create your models here.


class UserConsole(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name


class CourseComment(models.Model):
    user = models.ForeignKey(UserProfile, related_name="coursecomments", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="coursecomments", on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name="评论内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name


class UserCollect(models.Model):
    user = models.ForeignKey(UserProfile, related_name="coursecollects", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name="数据id")
    fav_type = models.IntegerField(default=1, choices=((1, "课程"),(2, "课程机构"),(3, "讲师")), verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.ForeignKey(UserProfile, related_name="usermessages", on_delete=models.CASCADE)
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, related_name="usercourses", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="usercourses", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name