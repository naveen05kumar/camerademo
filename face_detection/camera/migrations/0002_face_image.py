# Generated by Django 5.0.7 on 2024-07-23 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='face',
            name='image',
            field=models.ImageField(default='detected_faces/default.jpg', upload_to='detected_faces/'),
        ),
    ]