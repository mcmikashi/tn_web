# Generated by Django 3.2.11 on 2022-02-16 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PressMention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newspaper_name', models.CharField(max_length=200)),
                ('article_link', models.URLField(max_length=255)),
                ('article_title', models.CharField(max_length=200)),
                ('article_summary', models.TextField()),
                ('article_publication_date', models.DateField()),
            ],
            options={
                'permissions': (('press-editor', 'May create and see list view Article'),),
            },
        ),
    ]
