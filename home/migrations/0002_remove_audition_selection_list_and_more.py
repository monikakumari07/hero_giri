# Generated by Django 4.2.3 on 2023-07-28 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audition',
            name='selection_list',
        ),
        migrations.AlterField(
            model_name='audition',
            name='add_audition_position',
            field=models.CharField(max_length=300),
        ),
        migrations.DeleteModel(
            name='SelectionList',
        ),
    ]
