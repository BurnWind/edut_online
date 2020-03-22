# Generated by Django 2.2 on 2020-02-29 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200229_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forgot', '找回密码'), ('get_code', '获取验证码')], max_length=10, verbose_name='验证码类型'),
        ),
    ]