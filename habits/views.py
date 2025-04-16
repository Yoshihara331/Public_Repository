from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Habit, DailyReport
from .forms import HabitForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from datetime import datetime


@login_required
def habit_list(request):
    habit_queryset = Habit.objects.filter(user=request.user, deleted_at__isnull=True).order_by('-created_at')
    paginator = Paginator(habit_queryset, 5)  # 👈 1ページに5件ずつ表示
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # 👈 変数名を page_obj にする！

    return render(request, 'habits/habit_list.html', {
        'page_obj': page_obj,
        'habits': page_obj.object_list,  # 👈 forループでは habits を使えるようにしておくとベター
    })


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST, user=request.user)
        if form.is_valid():
            print("✅ cleaned_data:", form.cleaned_data)  # ← 追加
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_list')
        else:
            print("❌ form.errors:", form.errors)
    else:
        form = HabitForm(user=request.user)
    return render(request, 'habits/habit_form.html', {'form': form})



@login_required
def habit_edit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('habit_list')
    else:
        # カンマ区切りの曜日 → リストに変換して初期値として渡す
        initial_data = {
            'schedule_days': habit.schedule_days.split(','),
        }
        form = HabitForm(instance=habit, initial=initial_data, user=request.user)

    return render(request, 'habits/habit_form.html', {'form': form})



@login_required
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.deleted_at = timezone.now()
    habit.save()
    return redirect('habit_list')


@csrf_exempt
@login_required
def toggle_habit_log(request):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        date_str = request.POST.get('date')

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return JsonResponse({'success': False, 'message': 'Invalid date'}, status=400)

        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
        except Habit.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Habit not found'}, status=404)

        # ✅ created_at__date で既存レコードを探す
        report = DailyReport.objects.filter(
            user=request.user,
            goal=habit.goal,
            habit=habit,
            date=target_date
        ).first()

        if not report:
            # ✅ 新規作成時には date と created_at の両方をセット
            report = DailyReport(
                user=request.user,
                goal=habit.goal,
                habit=habit,
                date=target_date,
                created_at=datetime.combine(target_date, datetime.min.time())
            )

        # ✅ ステータス切り替えて保存
        report.status = not report.status
        report.save()
        print("✅ 保存完了:", report)

        return JsonResponse({'success': True, 'completed': report.status})

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)




@csrf_protect
@login_required
def save_note(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        note_text = request.POST.get('note')

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return redirect('home')

        DailyReport.objects.update_or_create(
            user=request.user,
            created_at=datetime.combine(target_date, datetime.min.time()),
            goal=None,
            habit=None,
            defaults={'note': note_text}
        )

        return redirect(f"/?date={target_date}")


@csrf_exempt
@login_required
def save_habit_comment(request):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        comment_text = request.POST.get('comment')
        date_str = request.POST.get('date')

        if not (habit_id and date_str):
            return JsonResponse({'success': False, 'message': '必要な情報が不足しています。'}, status=400)

        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return JsonResponse({'success': False, 'message': 'データが不正です。'}, status=400)

        report, _ = DailyReport.objects.get_or_create(
            user=request.user,
            goal=habit.goal,
            habit=habit,
            created_at=datetime.combine(target_date, datetime.min.time())
        )

        report.comment = comment_text
        report.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'POSTメソッドのみ対応'}, status=405)
