# Generated by Django 3.2.15 on 2022-08-22 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileimg',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_images'),
        ),
    ]