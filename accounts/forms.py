from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "ユーザー名を入力"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "パスワードを入力"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "もう一度パスワードを入力"}),
        }
        labels = {
            "username": "ユーザー名",
            "password1": "パスワード",
            "password2": "パスワード（確認用）",
        }
        help_texts = {  # help_text を削除（黒字のメッセージを消す）
            "username": "",
            "password1": "",
            "password2": "",
        }
