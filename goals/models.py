from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザーごとの目標
    title = models.CharField(max_length=255)  # 目標のタイトル
    description = models.TextField(blank=True, null=True)  # 目標の詳細
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時
    target_count = models.IntegerField(default=0)  # 達成目標回数
    actual_count = models.IntegerField(default=0)  # 実際の達成回数

    def __str__(self):
        return self.title
