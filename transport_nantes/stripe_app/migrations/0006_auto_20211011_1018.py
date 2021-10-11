# Generated by Django 3.2.5 on 2021-10-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_app', '0005_trackingprogression_tn_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trackingprogression',
            name='user_agent',
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='browser',
            field=models.CharField(max_length=50, null=True, verbose_name='Navigateur'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='browser_version',
            field=models.CharField(max_length=50, null=True, verbose_name='Version du navigateur'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='device_brand',
            field=models.CharField(default='Unknown', max_length=50, null=True, verbose_name='Marque'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='device_family',
            field=models.CharField(max_length=50, null=True, verbose_name="Famille d'appareils"),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='device_model',
            field=models.CharField(default='Unknown', max_length=50, null=True, verbose_name='Modèle'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='is_bot',
            field=models.BooleanField(null=True, verbose_name='Est un bot'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='is_mobile',
            field=models.BooleanField(null=True, verbose_name='Est un mobile'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='is_pc',
            field=models.BooleanField(null=True, verbose_name='Est PC'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='is_tablet',
            field=models.BooleanField(null=True, verbose_name='Est une tablette'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='is_touch_capable',
            field=models.BooleanField(null=True, verbose_name='Est tactile'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='os',
            field=models.CharField(max_length=50, null=True, verbose_name='OS'),
        ),
        migrations.AddField(
            model_name='trackingprogression',
            name='os_version',
            field=models.CharField(max_length=50, null=True, verbose_name="Version de l'OS"),
        ),
    ]
