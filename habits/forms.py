from django import forms
from .models import Habit
from goals.models import Goal
import json  # ← 追加

class HabitForm(forms.ModelForm):
    DAYS_OF_WEEK = [
        ('月', '月'), ('火', '火'), ('水', '水'),
        ('木', '木'), ('金', '金'), ('土', '土'), ('日', '日'),
    ]

    schedule_days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'schedule-day'}),
        label="実施曜日"
    )
    
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

    UNIT_CHOICES = [
        ('回', '回'), ('分', '分'), ('時間', '時間'),
        ('ml', 'ミリリットル'), ('l', 'リットル'),
        ('km', 'キロメートル'), ('mile', 'マイル'), ('㎎', 'グラム'),
    ]
    target_unit = forms.ChoiceField(choices=UNIT_CHOICES, label="単位")

    FREQ_CHOICES = [
        ('1日あたり', '1日あたり'),
        ('1週間あたり', '1週間あたり'),
        ('1ヶ月あたり', '1ヶ月あたり'),
    ]
    target_frequency = forms.ChoiceField(choices=FREQ_CHOICES, label="頻度")

    ICON_CHOICES = [
        ('fa-dumbbell', '🏋️'), ('fa-running', '🏃'), ('fa-biking', '🚴'), ('fa-swimmer', '🏊'),
        ('fa-walking', '🚶'), ('fa-book', '📘'), ('fa-graduation-cap', '🎓'), ('fa-pencil-alt', '✏️'),
        ('fa-laptop-code', '💻'), ('fa-lightbulb', '💡'), ('fa-apple-alt', '🍎'), ('fa-heartbeat', '❤️'),
        ('fa-notes-medical', '📋'), ('fa-weight', '⚖️'), ('fa-seedling', '🌱'), ('fa-bed', '🛏️'),
        ('fa-bath', '🛁'), ('fa-shower', '🚿'), ('fa-coffee', '☕'), ('fa-utensils', '🍽️'),
        ('fa-bullseye', '🎯'), ('fa-flag-checkered', '🏁'), ('fa-check-circle', '✅'), ('fa-calendar-check', '📅'),
        ('fa-tasks', '🗒️'), ('fa-music', '🎵'), ('fa-film', '🎬'), ('fa-camera', '📷'), ('fa-paint-brush', '🎨'),
        ('fa-gamepad', '🎮'), ('fa-wallet', '👛'), ('fa-coins', '🪙'), ('fa-piggy-bank', '🐷'), ('fa-credit-card', '💳'),
        ('fa-money-bill-wave', '💵'), ('fa-briefcase', '💼'), ('fa-chart-line', '📈'), ('fa-users', '👥'),
        ('fa-folder-open', '📂'), ('fa-clock', '⏰'), ('fa-mountain', '🏔️'), ('fa-rocket', '🚀'),
        ('fa-compass', '🧭'), ('fa-brain', '🧠'), ('fa-eye', '👁️'), ('fa-hiking', '🥾'), ('fa-leaf', '🍃'),
        ('fa-bolt', '⚡'), ('fa-wind', '🌬️'), ('fa-spa', '🧖'), ('fa-water', '💧'), ('fa-tree', '🌳'),
        ('fa-fire', '🔥'), ('fa-dog', '🐶'), ('fa-cat', '🐱'), ('fa-sun', '☀️'), ('fa-moon', '🌙'),
        ('fa-cloud', '☁️'), ('fa-smile', '😄'), ('fa-frown', '😞'), ('fa-meditation', '🧘'), ('fa-hot-tub', '🛀'),
        ('fa-om', '🕉️'), ('fa-peace', '☮️'), ('fa-campground', '🏕️'), ('fa-fish', '🐟'), ('fa-bread-slice', '🍞'),
        ('fa-egg', '🥚'), ('fa-carrot', '🥕'), ('fa-seedling-alt', '🌿'), ('fa-yoga', '🧘‍♂️'), ('fa-journal', '📓'),
        ('fa-headphones', '🎧'), ('fa-hourglass', '⏳'), ('fa-binoculars', '🔭'), ('fa-calendar-alt', '📆'),
        ('fa-smog', '🌫️'), ('fa-snowflake', '❄️'), ('fa-bug', '🐞'), ('fa-plane', '✈️'), ('fa-ship', '🚢'),
        ('fa-bus', '🚌'), ('fa-bicycle', '🚲'), ('fa-anchor', '⚓'), ('fa-camera-retro', '📸'), ('fa-microphone', '🎤'),
        ('fa-drum', '🥁'), ('fa-guitar', '🎸'), ('fa-star', '⭐'), ('fa-heart', '💖'), ('fa-handshake', '🤝'),
        ('fa-bell', '🔔'), ('fa-birthday-cake', '🎂'), ('fa-cookie', '🍪'), ('fa-lemon', '🍋'),
        ('fa-ice-cream', '🍨'), ('fa-hamburger', '🍔'), ('fa-bacon', '🥓'), ('fa-pizza-slice', '🍕'),
        ('fa-cocktail', '🍸'), ('fa-wine-glass', '🍷')
    ]

    icon = forms.ChoiceField(choices=ICON_CHOICES, label="アイコン", required=False)

    class Meta:
        model = Habit
        fields = [
            'goal',
            'habit_name',
            'schedule_days',
            'target_value',
            'target_unit',
            'target_frequency',
            'icon',
        ]
        labels = {
            'goal': '関連する目標（任意）',
            'habit_name': '習慣名',
            'target_value': '目標値',
            'target_unit': '単位',
            'target_frequency': '頻度',
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['goal'].queryset = Goal.objects.filter(user=user)
            self.fields['goal'].required = False

        # 編集モード用初期値設定
        if self.instance and self.instance.pk:
            if self.instance.goal:
                self.initial['goal'] = self.instance.goal.id

            if self.instance.schedule_days:
                # カンマ区切り→リストへ変換
                self.initial['schedule_days'] = self.instance.schedule_days.split(',')

            if self.instance.icon and not self.initial.get('icon'):
                self.initial['icon'] = self.instance.icon

        # 新規作成かつGET指定があるときにアイコン自動設定
        if self.initial.get('goal') and not self.initial.get('icon'):
            goal = Goal.objects.filter(id=self.initial['goal']).first()
            if goal:
                self.initial['icon'] = goal.icon


    def clean_schedule_days(self):
        days = self.cleaned_data['schedule_days']
        return ','.join(days)

    def clean_target_value(self):
        value = self.cleaned_data['target_value']
        if value < 1:
            raise forms.ValidationError("1以上の数値を入力してください。")
        return value

    def save(self, commit=True):
        instance = super().save(commit=False)

        if not instance.icon and instance.goal:
            instance.icon = instance.goal.icon

        if commit:
            instance.save()
        return instance
