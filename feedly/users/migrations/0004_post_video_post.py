# Generated by Django 2.1.1 on 2018-09-26 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180926_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video_post',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
