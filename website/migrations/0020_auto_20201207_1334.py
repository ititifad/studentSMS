# Generated by Django 3.1 on 2020-12-07 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_result_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='score',
            field=models.IntegerField(null=True),
        ),
    ]
