# Generated by Django 3.1.4 on 2021-03-04 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='content',
            field=models.FileField(null=True, upload_to='submissions'),
        ),
    ]