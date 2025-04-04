from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('create/', views.habit_create, name='habit_create'),
    path('edit/<int:habit_id>/', views.habit_edit, name='habit_edit'),
    path('delete/<int:habit_id>/', views.habit_delete, name='habit_delete'),
    path('toggle/', views.toggle_habit_log, name='toggle_habit_log'),

    # 🔥 ここを追加
    path('save_note/', views.save_note, name='save_summary_note'),

    # 習慣別コメント用
    path('save_comment/', views.save_habit_comment, name='save_comment'),
]
