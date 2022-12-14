from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import OrderCard, OrderProduct, Product


def delete_bucket_item(sender, instance, created, **kwargs):
    if created:
        order_card = instance
        order_products = OrderProduct.objects.all().filter(client=order_card.client)
        for i in order_products:
            i.status = "DONE"
            i.save()


def send_order_info(sender, instance, created, **kwargs):
    if created:
        order_card = instance
        order_products = OrderProduct.objects.all().filter(client=order_card.client, status="PROCESSING")
        if not order_products:
            order_products = OrderProduct.objects.all().filter(session_id=order_card)

        print("ORDER: ", order_products)
        user_mail = order_card.email
        print(user_mail)

        product_list = ""
        for product in order_products:
            product_list += product.product_id.name + ", "
        product_list = product_list[0:-2]
        subject = "Дякуємо за покупку у нашому магазині 'Це Щось!'"
        message = f"Ваше замовлення: ({product_list}) прийнято. Незабаром з вами зв'яжуться для уточнення деталей. " \
                  f"Гарного дня!"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user_mail],
            fail_silently=False,
        )


post_save.connect(send_order_info, sender=OrderCard)
post_save.connect(delete_bucket_item, sender=OrderCard)
