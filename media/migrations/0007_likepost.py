# Generated by Django 3.2.15 on 2022-08-23 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0006_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]