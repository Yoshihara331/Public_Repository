from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import login_view, signup_view, logout_view, profile_edit_view, CustomPasswordChangeView, profile_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),  # 新規登録
    path('login/', login_view, name='login'),  # ログイン
    path('logout/', logout_view, name='logout'),  # ログアウト
    path('profile/edit/', profile_edit_view, name='profile_edit'),  # プロフィール編集
    path('profile/password/', CustomPasswordChangeView.as_view(), name='password_change'),  # パスワード変更
    path('profile/', profile_view, name='profile'),  # プロフィール表示

]
