from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Post

@receiver(pre_save, sender=Post)
def calculate_new_price(sender, instance, **kwargs):
    instance.new_price = instance.price - instance.off