from django.contrib import admin

from .models import InwardOrder, InOli, OutwardOrder, OutOli


class InOli_Inline(admin.TabularInline):
    model = InOli

    fieldsets = (
        ('Order Details', {
            "fields": (
                'inward_order', 'product', 'container_type', 'quantity', 'stock',
            ),
        }),
    )

    extra = 2


class OutOli_Inline(admin.TabularInline):
    model = OutOli

    fieldsets = (
        ('Order Details', {
            "fields": (
                'outward_order', 'in_oli', 'quantity'
            ),
        }),
    )


class InwardOrderAdmin(admin.ModelAdmin):
    model = InwardOrder

    fieldsets = (
        ('Inward Order', {
            "fields": (
                'customer',
            ),
        }),
    )

    inlines = [InOli_Inline]


class OutwardOrderAdmin(admin.ModelAdmin):
    model = OutwardOrder

    fieldsets = (
        ('Outward Order', {
            "fields": (
                'customer', 'inward_order'
            ),
        }),
    )

    inlines = [OutOli_Inline]


admin.site.register(InwardOrder, InwardOrderAdmin)
admin.site.register(OutwardOrder, OutwardOrderAdmin)