# core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Gym, Plan

@receiver(post_save, sender=Gym)
def create_default_plan(sender, instance, created, **kwargs):
    """
    Create a default plan for a gym when it is created.

    'sender' is the model (Gym).
    'instance' is the Gym object that was saved.
    'created' is a boolean that is True if the object was created now
    (and False if it was just an update).
    """
    if created:  # Only execute if the Gym was just created
        Plan.objects.create(
            gym=instance,
            name="Plano Mensal (Jiu-Jitsu)",
            monthly_fee=201.90,
            fee_after_due_date=25.90
        )
        print(f"Default plan created for gym: {instance.name}")
