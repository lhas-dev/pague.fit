from django.contrib import admin
from .models import Gym, Plan, Student, Subscription, Payment

class StudentInline(admin.TabularInline):
    model = Student
    extra = 1  # Number of empty forms to display
    fields = ['full_name', 'email', 'phone_number']

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'city', 'state']
    search_fields = ['name', 'owner__username', 'city', 'state']
    inlines = [StudentInline]

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['student', 'plan', 'start_date', 'next_due_date', 'status', 'public_id']
    readonly_fields = ['public_id']
    list_filter = ['status', 'plan__gym']
    search_fields = ['student__full_name', 'student__email', 'plan__name']

admin.site.register(Plan)
admin.site.register(Student)
admin.site.register(Payment)
