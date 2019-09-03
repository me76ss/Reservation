# Generated by Django 2.2.4 on 2019-09-03 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextrainfo',
            name='admin_type',
            field=models.CharField(blank=True, choices=[('SUPER_ADMIN', 'SUPER_ADMIN'), ('ADMIN', 'ADMIN'), ('PROVIDER', 'PROVIDER')], max_length=50),
        ),
        migrations.AlterField(
            model_name='userextrainfo',
            name='user_type',
            field=models.CharField(blank=True, choices=[('STUDENT', 'STUDENT'), ('PERSONNEL', 'PERSONNEL'), ('GUEST', 'GUEST')], max_length=50),
        ),
    ]
