# Generated by Django 4.0.6 on 2022-08-11 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0008_alter_orderproduct_product_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['price']},
        ),
        migrations.AlterField(
            model_name='product',
            name='img1',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='img2',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='img3',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
    ]
