from django.contrib import admin
from django.contrib import admin
from .models import Department, Role, Manager, Employee, PerformanceReview, Project, Task, LeaveRequest


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'title', 'phone_number', 'hire_date')
    list_filter = ('department', 'hire_date')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'manager', 'department', 'role', 'title', 'phone_number', 'hire_date')
    list_filter = ('department', 'role', 'hire_date')


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'review_date', 'rating')

    list_filter = ('review_date', 'rating')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'start_date', 'end_date')

    list_filter = ('department', 'start_date', 'end_date')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'assigned_to', 'due_date', 'completed')
    list_filter = ('project', 'due_date', 'completed')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'approved')

    list_filter = ('approved', 'start_date', 'end_date')
