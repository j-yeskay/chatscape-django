# Generated by Django 3.2.4 on 2022-05-15 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account1', to=settings.AUTH_USER_MODEL)),
                ('account2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
