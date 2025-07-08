# core/models.py

import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class Gym(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the gym")
    # OneToOneField ensures each user can own only one gym.
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Address fields
    street_name = models.CharField(max_length=200, blank=True, null=True, help_text="Street name")
    street_number = models.CharField(max_length=20, blank=True, null=True, help_text="Building/location number")
    complement = models.CharField(max_length=100, blank=True, null=True, help_text="Additional address information (apt, suite, etc)")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="City name")
    state = models.CharField(max_length=100, blank=True, null=True, help_text="State/province name")
    country = models.CharField(max_length=100, blank=True, null=True, help_text="Country name")
    postal_code = models.CharField(max_length=20, blank=True, null=True, help_text="ZIP/Postal code")

    class Meta:
        verbose_name_plural = "Gyms"

    def __str__(self):
        return self.name

class Plan(models.Model):
    # A gym can have multiple plans.
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="e.g., Monthly Plan - Jiu-Jitsu")
    monthly_fee = models.DecimalField(max_digits=7, decimal_places=2)
    # Optional field for late fees.
    fee_after_due_date = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.gym.name})"

class Student(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, help_text="Número de telefone obrigatório para contato.")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        unique_together = ('gym', 'phone_number')

    def __str__(self):
        return f"{self.full_name} ({self.gym.name})"

class Subscription(models.Model):
    """
    Connects a Student to a Plan. This is the core of the system.
    """
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('OVERDUE', 'Overdue'),
        ('CANCELED', 'Canceled'),
    )

    def get_first_day_next_month():
        """Returns the first day of next month"""
        today = date.today()
        first_next_month = today + relativedelta(months=1, day=1)
        return first_next_month

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    next_due_date = models.DateField(default=get_first_day_next_month)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    # Public ID for payment links, to avoid exposing database IDs.
    public_id = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.plan.name} Plan"

    def is_overdue(self):
        return date.today() > self.next_due_date

    def is_active(self):
        return self.status == 'ACTIVE'
    
    def is_canceled(self):
        return self.status == 'CANCELED'
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True) # Sets the timestamp when the object is created.
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    # To store the ID from the payment gateway (e.g., Mercado Pago).
    external_payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment from {self.subscription.student.full_name} - {self.status}"