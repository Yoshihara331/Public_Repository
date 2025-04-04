from django.db import models
from django.contrib.auth.models import User
from goals.models import Goal  # 既存目標モデル

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=255)
    schedule_days = models.CharField(max_length=50, help_text="例: 月,水,金")
    streak_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.habit_name} ({self.user.username})"

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habit.habit_name} - {self.date} - {'✅' if self.completed else '❌'}"

class DailyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey("goals.Goal", on_delete=models.CASCADE, null=True, blank=True)
    habit = models.ForeignKey("habits.Habit", on_delete=models.CASCADE, null=True, blank=True)
    
    # ✅ 日全体用（home画面の「今日の振り返りメモ」）
    note = models.TextField(null=True, blank=True)
    
    # ✅ 習慣別コメント用（「コメントを書く」ボタンで出てくるやつ）
    comment = models.TextField(null=True, blank=True)

    # ✅ 達成状況（toggleで記録される）
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField()  # ← auto_now_add=False にして意図的にdatetime指定
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        habit_name = self.habit.habit_name if self.habit else "日報"
        return f"{self.user.username} - {habit_name} ({self.created_at.strftime('%Y-%m-%d')})"
