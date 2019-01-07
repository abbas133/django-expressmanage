# Generated by Django 2.0.9 on 2019-01-07 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
        ('products', '0001_initial'),
        ('customers', '0002_auto_20190107_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='outwardorder',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outwardorder_create', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='outwardorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer'),
        ),
        migrations.AddField(
            model_name='outwardorder',
            name='inward_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.InwardOrder'),
        ),
        migrations.AddField(
            model_name='outwardorder',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outwardorder_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
        migrations.AddField(
            model_name='outoli',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outoli_create', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='outoli',
            name='in_oli',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='orders.InOli'),
        ),
        migrations.AddField(
            model_name='outoli',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outoli_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
        migrations.AddField(
            model_name='outoli',
            name='outward_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OutwardOrder'),
        ),
        migrations.AddField(
            model_name='inwardorder',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inwardorder_create', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='inwardorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer'),
        ),
        migrations.AddField(
            model_name='inwardorder',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inwardorder_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
        migrations.AddField(
            model_name='inoli',
            name='container_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ContainerType'),
        ),
        migrations.AddField(
            model_name='inoli',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inoli_create', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='inoli',
            name='inward_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.InwardOrder'),
        ),
        migrations.AddField(
            model_name='inoli',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inoli_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by'),
        ),
        migrations.AddField(
            model_name='inoli',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]