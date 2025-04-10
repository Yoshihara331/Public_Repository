# Generated by Django 5.1.6 on 2025-03-31 12:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goals', '0002_remove_goal_actual_count'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habit_name', models.CharField(max_length=255)),
                ('schedule_days', models.CharField(help_text='例: 月,水,金', max_length=50)),
                ('streak_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goals.goal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HabitLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('completed', models.BooleanField(default=False)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='habits.habit')),
            ],
        ),
    ]
