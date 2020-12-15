# Generated by Django 3.1 on 2020-11-29 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='reports',
            field=models.FileField(blank=True, upload_to='students/reports'),
        ),
        migrations.AddField(
            model_name='student',
            name='results',
            field=models.FileField(blank=True, upload_to='students/results'),
        ),
        migrations.AlterField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.png', upload_to='profile_pics'),
        ),
    ]
