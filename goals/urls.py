from django.urls import path
from . import views

urlpatterns = [
    path('', views.goal_list, name='goal_list'),  # 目標一覧
    path('add/', views.goal_create, name='goal_create'),  # 目標追加
    path('<int:goal_id>/edit/', views.goal_edit, name='goal_edit'),  # 目標編集
    path('<int:goal_id>/delete/', views.goal_delete, name='goal_delete'),  # 目標削除
]
