from django.db import models
from django.contrib.auth.models import User
from goals.models import Goal

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
    habit_name = models.CharField(max_length=100)

    schedule_days = models.CharField(max_length=50)  # ← カンマ区切りで保存（例: "月,火,水"）
    target_value = models.PositiveIntegerField(default=1)

    FREQ_CHOICES = [
        ('1日あたり', '1日あたり'),
        ('1週間あたり', '1週間あたり'),
        ('1ヶ月あたり', '1ヶ月あたり'),
    ]
    target_frequency = models.CharField(
        max_length=20,
        choices=FREQ_CHOICES,
        default='1日あたり'
    )

    UNIT_CHOICES = [
        ('回', '回'), ('分', '分'), ('時間', '時間'),
        ('ml', 'ミリリットル'), ('l', 'リットル'),
        ('km', 'キロメートル'), ('mile', 'マイル'), ('㎎', 'グラム'),
    ]
    target_unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='回')

    icon = models.CharField(max_length=50, default='fa-star')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        goal_name = self.goal.goal_title if self.goal else "未分類"
        return f"{goal_name} - {self.habit_name}（{self.target_value}{self.target_unit}）"


class DailyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey("goals.Goal", on_delete=models.CASCADE, null=True, blank=True)
    habit = models.ForeignKey("habits.Habit", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=False)
    status = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        habit_name = self.habit.habit_name if self.habit else "日報"
        return f"{self.user.username} - {habit_name} ({self.created_at.strftime('%Y-%m-%d')})"
