"""CampusConnectProject URL Configuration

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from CampusConnectApp import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view, name='logout'),

    path('dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    path('add-task/', views.add_task, name='add_task'),
    path('view-tasks/', views.view_tasks, name='view_tasks'),
    path('mark-task-done/<int:task_id>/', views.mark_task_done, name='mark_task_done'),

    path('navbar/',views.navbar,name='navbar'),
    path('home/',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('email/',views.email,name='email'),

    path('staff-profile/', views.staff_profile, name='staff_profile'),
    path('admin-profile/', views.admin_profile, name='admin_profile'),
    path('student-profile/', views.student_profile, name='student_profile'),
    path('upload/<int:task_id>/', views.upload_file, name='upload_file'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('mark-reviewed/<int:task_id>/', views.mark_task_reviewed, name='mark_task_reviewed'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
