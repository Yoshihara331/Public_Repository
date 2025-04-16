from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザーごとの目標
    title = models.CharField(max_length=255)  # 目標のタイトル
    icon = models.CharField(max_length=50, default='fa-star')  # FontAwesome アイコン
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
