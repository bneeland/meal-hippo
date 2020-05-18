import sys
sys.path.append("..")

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from webplatform.models import UserDeliveryDetail, UserSubscription

@receiver(post_save, sender=CustomUser)
def create_user_delivery_detail(sender, instance, created, **kwargs):
    if created:
        UserDeliveryDetail.objects.create(user=instance)
        UserSubscription.objects.create(user=instance)
