from django.contrib import admin
from .models import Habit, DailyReport

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('habit_name', 'user', 'goal', 'target_value', 'target_unit', 'target_frequency', 'created_at')

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'habit', 'goal', 'date', 'status', 'created_at')
    list_filter = ('user', 'habit', 'status', 'date')
