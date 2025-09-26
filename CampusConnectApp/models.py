from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

# Custom User model with role
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STAFF', 'Staff'),
        ('STUDENT', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    assigned_to = models.ManyToManyField(
        CustomUser,
        related_name='tasks_assigned_to',
        limit_choices_to={'role': 'STUDENT'}
    )

    assigned_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tasks_created'
    )

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        null=True
    )

    completed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='completed_tasks',
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(null=True, blank=True)
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submission_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class TaskSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    is_marked = models.BooleanField(default=False)
    marked_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_submissions'
    )
    marked_at = models.DateTimeField(null=True, blank=True)

    notify_admin = models.BooleanField(default=False)
    notify_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} - {self.student.username}"

    class Meta:
        unique_together = ('task', 'student')

