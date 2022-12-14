# Generated by Django 4.0.6 on 2022-08-13 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_profile_phone'),
        ('goods', '0009_alter_product_options_alter_product_img1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=200)),
                ('mail_post', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('father_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('PROCESSING', 'В обробці'), ('SENT', 'Відправлено'), ('TAKEN', 'Отримано')], default='PROCESSING', max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.profile')),
                ('goods', models.ManyToManyField(blank=True, to='goods.orderproduct')),
            ],
        ),
    ]
