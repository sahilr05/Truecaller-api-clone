# Generated by Django 3.0.6 on 2021-05-06 18:12
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("main_app", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="email",
            field=models.EmailField(default="test3@user.com", max_length=254),
            preserve_default=False,
        )
    ]
