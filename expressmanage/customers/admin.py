from django.contrib import admin

from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'firm', 'name'
            ),
        }),
        ('Contact Information', {
            "fields": (
                'mobile_number', 'address', 'city'
            ),
        })
    )

    # List view option on admin page
    list_display = ('firm', 'name', 'mobile_number')

    # List of filterable fields
    list_filter = ['firm', 'name']

    # Search box at the top
    search_fields = ['firm', 'name']


admin.site.register(Customer, CustomerAdmin)