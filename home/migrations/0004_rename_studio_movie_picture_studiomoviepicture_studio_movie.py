# Generated by Django 4.2.3 on 2023-07-28 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_campaigns_movie_start_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studiomoviepicture',
            old_name='studio_movie_picture',
            new_name='studio_movie',
        ),
    ]
