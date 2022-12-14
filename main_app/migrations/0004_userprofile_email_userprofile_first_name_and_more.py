# Generated by Django 4.1.1 on 2022-10-08 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='first', max_length=100, verbose_name='Email'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='last', max_length=100, verbose_name='First Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='email@email.com', max_length=100, verbose_name='Last Name'),
            preserve_default=False,
        ),
    ]
