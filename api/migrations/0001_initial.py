# Generated by Django 3.1.1 on 2020-10-29 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=10)),
                ('number', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='StudyTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(choices=[('m', 'morning'), ('a', 'afternoon'), ('e', 'evening'), ('n', 'night')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studylocation', models.CharField(max_length=15)),
                ('courses', models.ManyToManyField(related_name='students', to='api.Course')),
                ('studytime', models.ManyToManyField(related_name='students', to='api.StudyTime')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(max_length=10)),
                ('content', models.CharField(max_length=140)),
                ('timestamp', models.DateTimeField()),
                ('receivers', models.ManyToManyField(related_name='received_message', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_message', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_organized', models.DateTimeField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('title', models.CharField(max_length=50)),
                ('size_limit', models.IntegerField()),
                ('link', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500)),
                ('status', models.IntegerField()),
                ('course_focus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='api.course')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organized_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='api.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]