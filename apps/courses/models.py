
from datetime import datetime

from django.db import models

from organizations.models import CourseOrg,Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="课程名称")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(max_length=2, choices=(("cj","初级"),("zj","中级"),("gj","高级")), verbose_name="难度")
    learn_time = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    favor = models.IntegerField(default=0, verbose_name="收藏数")
    click = models.IntegerField(default=0, verbose_name="点击量")
    students_num = models.IntegerField(default=0, verbose_name="学习人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面")
    category = models.CharField(default="后端开发", max_length=20, verbose_name="课程类别")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)
    you_need_know = models.CharField(default="", max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师告诉你")
    teacher = models.ForeignKey(Teacher, null=True, blank=True, related_name='courses', on_delete=models.CASCADE)
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    #获取章节数
    def get_lesson_num(self):
        return self.lessons.all().count()

    #获取学习用户
    def get_learn_user(self):
        return self.usercourses.all()[:5]

    #获取章节
    def get_lessons(self):
        return self.lessons.all()

    #获取资源
    def get_resources(self):
        return self.resources.all()


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="章节名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    #获取视频
    def get_videos(self):
        return self.videos.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="videos", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="课程名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    url = models.URLField(max_length=200, default="", verbose_name="访问地址")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Resource(models.Model):
    course = models.ForeignKey(Course, related_name="resources", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="资源名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    download = models.FileField(max_length=100, upload_to="course/resource/%Y%m", verbose_name="资源文件")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name