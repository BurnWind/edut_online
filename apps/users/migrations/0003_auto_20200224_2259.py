# Generated by Django 2.2 on 2020-02-24 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_banner_emailverifyrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forgot', '找回密码')], max_length=10, verbose_name='验证码类型'),
        ),
    ]
