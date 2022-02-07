# Generated by Django 3.2.11 on 2022-02-02 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topicblog', '0030_auto_20220127_1411'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topicblogitem',
            options={'permissions': (('tbi.may_view', 'May view unpublished TopicBlogItems'), ('tbi.may_edit', 'May create and modify TopicBlogItems'), ('tbi.may_publish', 'May publish TopicBlogItems'), ('tbi.may_publish_self', 'May publish own TopicBlogItems'))},
        ),
        migrations.AddField(
            model_name='topicblogemail',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topicblogitem',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='topicblogemail',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='topicblogitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]