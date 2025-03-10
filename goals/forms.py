from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'target_count']
        labels = {
            'title': '目標のタイトル',
            'description': '説明（任意）',
            'target_count': '目標達成回数',
        }
