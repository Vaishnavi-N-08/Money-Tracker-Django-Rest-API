# Generated by Django 4.1.4 on 2022-12-31 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Split', '0004_delete_entity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('title', models.CharField(max_length=100)),
                ('paid_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paid_by', to=settings.AUTH_USER_MODEL)),
                ('split_between_users', models.ManyToManyField(related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
