from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import OrderCard, OrderProduct


def delete_bucket_item(sender, instance, created, **kwargs):
    if created:
        order_card = instance
        order_products = OrderProduct.objects.all().filter(client=order_card.client)
        for i in order_products:
            i.status = "DONE"
            i.save()



post_save.connect(delete_bucket_item, sender=OrderCard)