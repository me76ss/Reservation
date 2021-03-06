# Generated by Django 2.2.4 on 2019-08-28 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import programs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('starts_at', models.DateTimeField()),
                ('ends_at', models.DateTimeField()),
                ('notify_at', models.TimeField()),
                ('queueable', models.BooleanField()),
                ('cancel_threshold', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ProgramSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts_at', models.DateTimeField()),
                ('ends_at', models.DateTimeField()),
                ('capacity', models.IntegerField()),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='programs.Program')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramWhitList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='white_list', to='programs.Program')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramSlotRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(programs.models.ProgramSlotType('RESERVE'), 'RESERVE'), (programs.models.ProgramSlotType('WAITING'), 'WAITING')], max_length=50)),
                ('participated', models.BooleanField(default=False)),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='programs.ProgramSlot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
