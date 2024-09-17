from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from products.models import Product, Category


@receiver(pre_save, sender=Product)
def create_product_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        instance.save()


@receiver(pre_save, sender=Category)
def create_category_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        instance.save()