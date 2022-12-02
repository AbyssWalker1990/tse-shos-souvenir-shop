# Generated by Django 4.1.3 on 2022-12-02 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0014_ordercard_session_id_orderproduct_session_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='featured_img',
            field=models.ImageField(default='default.png', upload_to='category/'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='goods.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='featured_img',
            field=models.ImageField(default='default.png', upload_to='goods/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img1',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='goods/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img2',
            field=models.ImageField(blank=True, default='default.png', upload_to='goods/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img3',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='goods/'),
        ),
    ]