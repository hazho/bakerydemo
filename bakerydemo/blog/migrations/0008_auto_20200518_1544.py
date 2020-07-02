# Generated by Django 2.1.15 on 2020-05-18 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20191004_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogindexpage',
            name='locale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_localize.Locale'),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='locale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_localize.Locale'),
        ),
        migrations.AlterField(
            model_name='blogpeoplerelationship',
            name='locale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_localize.Locale'),
        ),
    ]