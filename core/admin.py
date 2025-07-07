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

admin.site.register(Plan)
admin.site.register(Student)
admin.site.register(Subscription)
admin.site.register(Payment)
