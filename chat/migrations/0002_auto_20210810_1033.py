# Generated by Django 3.2.4 on 2021-08-10 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='friends',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_account', to=settings.AUTH_USER_MODEL)),
                ('sender_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]