from django.shortcuts import render
from goals.models import Goal  # 目標モデルをインポート
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # 現在ログインしているユーザーの目標を取得
    goals = Goal.objects.filter(user=request.user)

    return render(request, 'home.html', {'goals': goals})
