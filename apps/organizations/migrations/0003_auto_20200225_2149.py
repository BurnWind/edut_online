# Generated by Django 2.2 on 2020-02-25 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_courseorg_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='desc',
            field=models.TextField(verbose_name='机构描述'),
        ),
    ]
