from django.db import models
from django.contrib.auth.models import User
from goals.models import Goal

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    habit_name = models.CharField(max_length=100)
    
    # 実施曜日（カンマ区切りで保存）
    schedule_days = models.CharField(max_length=50)

    # 習慣に対する目標値
    target_value = models.PositiveIntegerField(default=1)
    
    # 頻度の選択肢
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

    # 単位の選択肢
    UNIT_CHOICES = [
        ('回', '回'),
        ('分', '分'),
        ('時間', '時間'),
        ('ml', 'ミリリットル'),
        ('l', 'リットル'),
        ('km', 'キロメートル'),
        ('mile', 'マイル'),
        ('㎎', 'グラム'),
    ]
    target_unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='回')

    # ⬇️ 追加：FontAwesomeアイコン選択（Goalと同じスタイル）
    icon = models.CharField(max_length=50, default='fa-star')

    # タイムスタンプ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # ✅ フォームから来たときに schedule_days がリストだったら、文字列に変換
        if isinstance(self.schedule_days, list):
            self.schedule_days = ','.join(self.schedule_days)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.habit_name}（{self.target_value}{self.target_unit}）"

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
