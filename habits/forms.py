from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    DAYS_OF_WEEK = [
        ('月', '月曜日'),
        ('火', '火曜日'),
        ('水', '水曜日'),
        ('木', '木曜日'),
        ('金', '金曜日'),
        ('土', '土曜日'),
        ('日', '日曜日'),
    ]

    schedule_days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        label="実施曜日"
    )

    class Meta:
        model = Habit
        fields = ['goal', 'habit_name', 'schedule_days']
        labels = {
            'goal': '関連する目標',
            'habit_name': '習慣名',
        }

    def clean_schedule_days(self):
        data = self.cleaned_data['schedule_days']
        return ','.join(data)  # DBにはカンマ区切りで保存
