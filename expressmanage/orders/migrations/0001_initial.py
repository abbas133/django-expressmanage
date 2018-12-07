# Generated by Django 2.0.9 on 2018-12-07 09:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('customers', '0002_auto_20181205_1250'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InOli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('quantity', models.IntegerField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('container_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.ContainerType')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inoli_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InwardOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('lot_number', models.CharField(blank=True, max_length=10)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=50)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inwardorder_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customers.Customer')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inwardorder_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutOli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('quantity', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outoli_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('in_oli', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='orders.InOli')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outoli_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutwardOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('received_by', models.CharField(default='Self', max_length=50)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=50)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outwardorder_create', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customers.Customer')),
                ('inward_order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.InwardOrder')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outwardorder_update', to=settings.AUTH_USER_MODEL, verbose_name='last updated by')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='outoli',
            name='outward_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OutwardOrder'),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Product'),
        ),
    ]
