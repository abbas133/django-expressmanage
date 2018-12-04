from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'firm', 'first_name', 'last_name'
            ),
        }),
        ('Contact Information', {
            "fields": (
                'mobile_number', 'address', 'city'
            ),
        })
    )

    # List view option on admin page
    list_display = ('firm', 'first_name', 'last_name', 'mobile_number')

    # List of filterable fields
    list_filter = ['firm', 'first_name']

    # Search box at the top
    search_fields = ['firm', 'first_name']


admin.site.register(Customer, CustomerAdmin)