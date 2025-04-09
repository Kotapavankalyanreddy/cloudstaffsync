from django.contrib import admin
from django.urls import path
from employees import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('staff_profile/', views.staff_profile, name='staff_profile'),
    path('leave_request/', views.leave_request, name='leave_request'),    
    path('staff_leave_request/', views.staff_leave_request, name='staff_leave_request'),
    path('manage_leave/<int:leave_id>/', views.manage_leave, name='manage_leave'),
    path('attendance/', views.attendance, name='attendance'),
    path('staff_attendance/', views.staff_attendance, name='staff_attendance'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),
    path('performance/', views.performance, name='performance'),
    path('staff_performance/', views.staff_performance, name='staff_performance'),
    path('performance/add/', views.add_performance, name='add_performance'),
    path('performance/edit/<int:performance_id>/', views.edit_performance, name='edit_performance'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('notifications/', views.notifications, name='notifications'),
    path('upload/', views.upload, name='upload'),
    path('payroll/', views.payroll, name='payroll'),
    path('staff_payroll/', views.staff_payroll, name='staff_payroll'),
    path('payroll/edit/<int:payroll_id>/', views.edit_payroll, name='edit_payroll'),

]
