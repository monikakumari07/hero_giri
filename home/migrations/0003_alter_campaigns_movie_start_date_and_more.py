# Generated by Django 4.2.3 on 2023-07-28 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_audition_selection_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaigns',
            name='movie_start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='campaigns',
            name='movie_start_end',
            field=models.DateField(),
        ),
    ]
