from django.db import models
import uuid
from userprofile.models import Profile


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    featured_img = models.ImageField(upload_to='category/', default="default.png")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['created']


class Product(models.Model):
    prod_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(max_length=30)
    discount = models.FloatField(max_length=30, null=True, blank=True)
    featured_img = models.ImageField(upload_to='goods/', default="default.png")
    img1 = models.ImageField(upload_to='goods/', null=True, blank=True, default="default.png")
    img2 = models.ImageField(upload_to='goods/', blank=True, default="default.png")
    img3 = models.ImageField(upload_to='goods/',null=True, blank=True, default="default.png")
    tags = models.ManyToManyField('Tag', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['price']

    class NewMeta(Meta):
        def high_price(self):
            ordering = ['-price']


class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name


class OrderProduct(models.Model):
    STATUS_CHOICES = (
        ("PROCESSING", "В обробці"),
        ("DONE", "Готово"),

    )
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    # Bounding for non-authorized user
    session_id = models.ForeignKey('OrderCard', on_delete=models.CASCADE, null=True, blank=True)

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    count = models.SmallIntegerField(default=1, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="PROCESSING")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.product_id)

    @property
    def total_price(self):
        if self.product_id.discount:
            total_price_order = self.count * self.product_id.discount
        else:
            total_price_order = self.count * self.product_id.price
        return total_price_order


class OrderCard(models.Model):
    STATUS_CHOICES = (
        ("PROCESSING", "В обробці"),
        ("PREPARING", "Готується до відправки"),
        ("SENT", "Відправлено"),
        ("TAKEN", "Отримано"),
    )

    PAYMENT_CHOICES = (
        ("ON_MAIL", "Накладений платіж"),
        ("CARD", "Оплата на картку"),
    )

    client = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    goods = models.ManyToManyField(OrderProduct, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    mail_post = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    surname = models.CharField(max_length=200, null=True, blank=True)
    father_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    payment_way = models.CharField(max_length=25, choices=PAYMENT_CHOICES, default="Оберіть вид оплати")
    total = models.FloatField(max_length=30,null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="В обробці")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)



