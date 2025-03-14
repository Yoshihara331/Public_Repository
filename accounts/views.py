from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # すでにログインしている場合はトップページへ

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        username = form.data.get('username')
        password1 = form.data.get('password1')
        password2 = form.data.get('password2')

        # パスワードの一致チェック
        if password1 != password2:
            messages.error(request, "パスワードが一致しません。")
        
        # ユーザー名の重複チェック
        elif User.objects.filter(username=username).exists():
            messages.error(request, "このユーザー名は既に使われています。")

        elif form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, str(error))  # エラーメッセージを追加

    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = AuthenticationForm(data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')  # ログアウト後はログイン画面へ
