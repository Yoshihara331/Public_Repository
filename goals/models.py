# models.py
from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザーごとの目標
    title = models.CharField(max_length=255)  # 目標のタイトル
    description = models.TextField(blank=True, null=True)  # 目標の詳細
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時
    target_count = models.IntegerField(default=0)  # 達成回数

    def __str__(self):
        return self.title

    # 達成率を算出するプロパティ（フォーム入力には使用しない）
    @property
    def progress_percent(self):
        return 0  # 将来的に習慣の実績数と連携させて実装
