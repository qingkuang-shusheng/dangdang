# Generated by Django 2.0.6 on 2020-09-16 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taddress',
            name='telephone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]