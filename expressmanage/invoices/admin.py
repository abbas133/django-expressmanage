from django.contrib import admin

from .models import Invoice, InvoiceLineItem, Payment, Receipt


class InvoiceLineItemInline(admin.TabularInline):
    model = InvoiceLineItem
    extra = 3


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 3


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceLineItemInline, PaymentInline]


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Payment)
admin.site.register(Receipt)