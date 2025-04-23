from django import forms
from .models import Habit
from goals.models import Goal

class HabitForm(forms.ModelForm):
    # ✅ 実行曜日（チェックボックス形式）
    DAYS_OF_WEEK = [
        ('月', '月'), ('火', '火'), ('水', '水'),
        ('木', '木'), ('金', '金'), ('土', '土'), ('日', '日'),
    ]

    schedule_days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        label="実施曜日"
    )

    # ✅ 目標値（1以上の整数）＋ min制約
    target_value = forms.IntegerField(
        min_value=1,
        initial=1,
        label="目標値",
        widget=forms.NumberInput(attrs={
            'min': '1',
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
            'step': '1',
            'oninput': "validity.valid||(value='');"
        })
    )

    # ✅ 単位の選択肢
    UNIT_CHOICES = [
        ('回', '回'), ('分', '分'), ('時間', '時間'),
        ('ml', 'ミリリットル'), ('l', 'リットル'),
        ('km', 'キロメートル'), ('mile', 'マイル'), ('㎎', 'グラム'),
    ]
    target_unit = forms.ChoiceField(choices=UNIT_CHOICES, label="単位")

    # ✅ 頻度の選択肢
    FREQ_CHOICES = [
        ('1日あたり', '1日あたり'),
        ('1週間あたり', '1週間あたり'),
        ('1ヶ月あたり', '1ヶ月あたり'),
    ]
    target_frequency = forms.ChoiceField(choices=FREQ_CHOICES, label="頻度")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['goal'].queryset = Goal.objects.filter(user=user)

        # 🔁 編集時の曜日処理
        if 'schedule_days' in self.initial and isinstance(self.initial['schedule_days'], str):
            self.initial['schedule_days'] = self.initial['schedule_days'].split(',')

    class Meta:
        model = Habit
        fields = [
            'goal',
            'habit_name',
            'schedule_days',
            'target_value',
            'target_unit',
            'target_frequency',
        ]
        labels = {
            'goal': '関連する目標',
            'habit_name': '習慣名',
            'target_value': '目標値',
            'target_unit': '単位',
            'target_frequency': '頻度',
        }

    def clean_target_value(self):
        value = self.cleaned_data['target_value']
        if value < 1:
            raise forms.ValidationError("1以上の数値を入力してください。")
        return value
