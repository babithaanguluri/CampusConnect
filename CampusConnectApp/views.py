from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from .forms import RegistrationForm, TaskForm, TaskFileUploadForm
from .models import CustomUser, Task, TaskSubmission


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def redirect_dashboard(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'STAFF':
        return redirect('staff_dashboard')
    elif request.user.role == 'STUDENT':
        return redirect('student_dashboard')
    else:
        return redirect('login')


@login_required
def admin_dashboard(request):
    users = CustomUser.objects.all()
    tasks = Task.objects.all()
    return render(request, 'admin_dashboard.html', {
        'users': users,
        'tasks': tasks
    })


@staff_member_required
def admin_profile(request):
    return render(request, 'admin_profile.html', {'user': request.user})


@login_required
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html', {})


@login_required
def student_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    submissions = TaskSubmission.objects.filter(student=request.user)
    submitted_task_ids = [s.task.id for s in submissions]
    return render(request, 'student_dashboard.html', {
        'tasks': tasks,
        'submitted_task_ids': submitted_task_ids
    })


@login_required
def student_profile(request):
    return render(request, 'student_profile.html', {'user': request.user})


@login_required
def staff_profile(request):
    return render(request, 'staff_profile.html')


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            form.save_m2m()
            return redirect('view_tasks')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})


@login_required
def view_tasks(request):
    tasks = Task.objects.all()
    all_submissions = TaskSubmission.objects.select_related('student', 'task')
    submissions_by_task = {}
    for submission in all_submissions:
        if submission.task.id not in submissions_by_task:
            submissions_by_task[submission.task.id] = []
        submissions_by_task[submission.task.id].append(submission)

    return render(request, 'view_tasks.html', {
        'tasks': tasks,
        'user': request.user,
        'submissions_by_task': submissions_by_task
    })


@login_required
def mark_task_done(request, task_id):
    if request.user.role not in ['STAFF', 'ADMIN']:
        return redirect('view_tasks')

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST' and not task.is_completed:
        task.is_completed = True
        task.completed_by = request.user
        task.completed_at = timezone.now()
        task.save()
    return redirect('view_tasks')


def navbar(request):
    return render(request, 'navbar.html', {})


def home(request):
    return render(request, 'home.html', {})


def about(request):
    return render(request, 'about.html', {})


def email(request):
    return render(request, 'email.html', {})


def logout(request):
    return render(request, 'logout.html', {})


@login_required
def upload_file(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user not in task.assigned_to.all():
        return HttpResponseForbidden("You are not allowed to upload for this task.")

    if request.method == 'POST':
        form = TaskFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # ✅ Check if submission already exists
            existing_submission = TaskSubmission.objects.filter(task=task, student=request.user).first()

            if existing_submission:
                # ✅ Update file instead of creating new
                existing_submission.file = form.cleaned_data['file']
                existing_submission.uploaded_at = timezone.now()
                existing_submission.save()
            else:
                TaskSubmission.objects.create(
                    task=task,
                    student=request.user,
                    file=form.cleaned_data['file']
                )
            return redirect('student_dashboard')
    else:
        form = TaskFileUploadForm()

    return render(request, 'upload_file.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.role in ['ADMIN', 'STAFF']:
        task.delete()
    return redirect('view_tasks')

def mark_task_reviewed(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.user.role in ['STAFF', 'ADMIN']:
        task.is_marked = True
        task.marked_by = request.user
        task.marked_at = timezone.now()
        task.save()
        
    return redirect('view_tasks')