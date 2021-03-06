# Generated by Django 3.2.8 on 2022-01-26 07:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_rename_notes_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='folder',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['updated_at']},
        ),
        migrations.AddField(
            model_name='folder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='note',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
