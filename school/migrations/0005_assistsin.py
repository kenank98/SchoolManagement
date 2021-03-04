# Generated by Django 3.1.4 on 2021-03-02 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_extracurricular'),
        ('school', '0004_enrolledin'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssistsIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'unique_together': {('student', 'course')},
            },
        ),
    ]