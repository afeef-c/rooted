# Generated by Django 5.0.1 on 2024-02-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_account_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000002B0C57A1C60>', max_length=200),
        ),
    ]
