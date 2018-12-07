from django.contrib import admin

from .models import Product, ContainerType, RateSlab


class RateSlabInline(admin.TabularInline):
    model = RateSlab
    extra = 3


class ContainerTypeAdmin(admin.ModelAdmin):
    inlines = [RateSlabInline]


# Register your models here.
admin.site.register(Product)
admin.site.register(ContainerType, ContainerTypeAdmin)

