# Generated by Django 4.2.7 on 2025-05-24 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name="Bo'lim nomi")),
                ('description', models.TextField(blank=True, verbose_name='Tavsif')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqti')),
            ],
            options={
                'verbose_name': "Bo'lim",
                'verbose_name_plural': "Bo'limlar",
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Mutaxassislik nomi')),
                ('description', models.TextField(blank=True, verbose_name='Tavsif')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialties', to='core.department', verbose_name="Bo'lim")),
            ],
            options={
                'verbose_name': 'Mutaxassislik',
                'verbose_name_plural': 'Mutaxassisliklar',
            },
        ),
    ]
