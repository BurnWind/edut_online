
from datetime import datetime

from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市名称")
    desc = models.CharField(max_length=200, verbose_name="城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class  CourseOrg(models.Model):
    city = models.ForeignKey(City, related_name="orgs", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    favor = models.IntegerField(default=0, verbose_name="收藏数")
    click = models.IntegerField(default=0, verbose_name="点击数")
    address = models.CharField(max_length=150, verbose_name="机构地址")
    image = models.ImageField(upload_to="orgs/%Y/%m", verbose_name="机构封面")
    kind = models.CharField(max_length=10, choices=(('per', '个人'),('school', '高校'),('pxjg', '培训机构')), default='pxjg', verbose_name='机构类别')
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")
    city = models.ForeignKey(City, verbose_name="所在城市", related_name='orgs', on_delete=models.CASCADE)
    students = models.IntegerField(default=0, verbose_name=u"学习人数")

    class Meta:
        verbose_name = "机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    #获取课程数
    def get_courses(self):
        return self.courses.all().count()

    #获取讲师数
    def get_teachers(self):
        return self.teachers.all().count()


class Teacher(models.Model):
    courseorg = models.ForeignKey(CourseOrg, related_name="teachers", on_delete=models.CASCADE)
    favor = models.IntegerField(default=0, verbose_name="收藏数")
    click = models.IntegerField(default=0, verbose_name="点击数")
    name = models.CharField(max_length=50, verbose_name="讲师姓名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="工作公司")
    work_position = models.CharField(max_length=50, verbose_name="工作职位")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(default='', upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    class Meta:
        verbose_name = "讲师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    #获取讲师课程数
    def get_courses_nums(self):
        return self.courses.all().count()

