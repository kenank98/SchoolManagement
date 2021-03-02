# Generated by Django 3.1.4 on 2021-03-02 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_assistsin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateTimeField()),
                ('assignment_number', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.course')),
            ],
            options={
                'unique_together': {('course', 'assignment_number')},
            },
        ),
    ]
