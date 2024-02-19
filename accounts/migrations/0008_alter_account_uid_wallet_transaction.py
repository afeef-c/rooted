# Generated by Django 5.0.1 on 2024-02-19 13:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_account_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x0000027F8EBA1C60>', max_length=200),
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.wallet')),
            ],
        ),
    ]
