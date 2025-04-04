from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

# ユーザー登録フォーム
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
            'password1': 'パスワード',
            'password2': 'パスワード（確認）',
        }

# プロフィール編集フォーム
class ProfileEditForm(UserChangeForm):
    password = None  # パスワードフィールドを削除
    
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
        }

# パスワード変更フォーム
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        labels = {
            'old_password': '現在のパスワード',
            'new_password1': '新しいパスワード',
            'new_password2': '新しいパスワード（確認）',
        }
