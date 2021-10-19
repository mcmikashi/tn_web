# Generated by Django 3.2.5 on 2021-10-19 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicblog', '0014_auto_20211017_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicblogitem',
            name='body_image',
            field=models.ImageField(blank=True, upload_to='body/'),
        ),
        migrations.AlterField(
            model_name='topicblogitem',
            name='header_image',
            field=models.ImageField(blank=True, upload_to='header/'),
        ),
        migrations.AlterField(
            model_name='topicblogitem',
            name='og_image',
            field=models.ImageField(blank=True, upload_to='opengraph/'),
        ),
        migrations.AlterField(
            model_name='topicblogitem',
            name='twitter_image',
            field=models.ImageField(blank=True, upload_to='twitter/'),
        ),
    ]
