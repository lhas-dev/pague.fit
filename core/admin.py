from django.contrib import admin
from .models import Gym, Plan, Student, Subscription, Payment

admin.site.register(Gym)
admin.site.register(Plan)
admin.site.register(Student)
admin.site.register(Subscription)
admin.site.register(Payment)
