# Generated by Django 4.1.3 on 2022-12-02 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0015_alter_category_featured_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='product_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.product'),
        ),
    ]
