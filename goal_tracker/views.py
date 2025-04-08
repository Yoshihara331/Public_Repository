from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from goals.models import Goal
from habits.models import Habit, HabitLog, DailyReport


@login_required
def home(request):
    date_str = request.GET.get('date')
    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        selected_date = timezone.localdate()

    weekday = selected_date.weekday()  # 0:月〜6:日
    weekday_ja = ['月', '火', '水', '木', '金', '土', '日'][weekday]

    goals = Goal.objects.filter(user=request.user)
    habits = Habit.objects.filter(user=request.user, schedule_days__contains=weekday_ja)

    logs = HabitLog.objects.filter(habit__in=habits, date=selected_date)
    log_map = {log.habit.id: log.completed for log in logs}

    goal_habit_map = {}
    for goal in goals:
        related_habits = habits.filter(goal=goal)
        goal_habit_map[goal] = related_habits

    # ✅ ここが重要：DailyReport（1日の振り返り）取得
    try:
        daily_report = DailyReport.objects.filter(
            user=request.user,
            created_at__date=selected_date
        ).first()
    except DailyReport.DoesNotExist:
        daily_report = None

    return render(request, 'home.html', {
        'goal_habit_map': goal_habit_map,
        'selected_date': selected_date,
        'weekday_ja': weekday_ja,
        'log_map': log_map,
        'daily_report': daily_report,
    })


@csrf_protect
@login_required
def save_summary_note(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        note_text = request.POST.get('note')

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return redirect('home')

        report, created = DailyReport.objects.get_or_create(
            user=request.user,
            created_at=datetime.combine(target_date, datetime.min.time()),
            defaults={'note': note_text}
        )

        if not created:
            report.note = note_text
            report.save()

        return redirect(f"/?date={target_date}")


@csrf_exempt
@login_required
def save_comment(request):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        comment_text = request.POST.get('comment')
        date_str = request.POST.get('date')

        if not (habit_id and comment_text and date_str):
            return JsonResponse({'success': False, 'message': 'データが不足しています。'}, status=400)

        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return JsonResponse({'success': False, 'message': 'データが不正です。'}, status=400)

        report, _ = DailyReport.objects.get_or_create(
            user=request.user,
            habit=habit,
            goal=habit.goal,
            created_at=datetime.combine(target_date, datetime.min.time())
        )

        report.comment = comment_text
        report.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'POSTメソッドのみ対応'}, status=405)

def custom_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)