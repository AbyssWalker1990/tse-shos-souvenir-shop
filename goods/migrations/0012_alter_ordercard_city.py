# Generated by Django 4.0.6 on 2022-08-13 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0011_alter_ordercard_email_alter_ordercard_father_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercard',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
