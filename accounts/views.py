from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignupForm, ProfileEditForm, CustomPasswordChangeForm

# ユーザー登録
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "アカウントが作成されました！")
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

# ログイン処理
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # すでにログイン済みならホームへ

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "ログインしました！")
                return redirect('home')
            else:
                messages.error(request, "ユーザー名またはパスワードが間違っています。")
        else:
            messages.error(request, "入力内容に誤りがあります。")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# ログアウト処理
def logout_view(request):
    logout(request)
    messages.success(request, "ログアウトしました！")
    return redirect('login')  # ログアウト後はログイン画面へ

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


# プロフィール編集
@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "プロフィールが更新されました！")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})

# パスワード変更
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('home')
    form_class = CustomPasswordChangeForm
    def form_valid(self, form):
        messages.success(self.request, "パスワードが変更されました！")
        return super().form_valid(form)
