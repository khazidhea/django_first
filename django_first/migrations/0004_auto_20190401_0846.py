# Generated by Django 2.1.7 on 2019-04-01 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_first', '0003_auto_20190401_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='django_first.Product'),
        ),
    ]
