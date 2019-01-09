from django.urls import path

from . import views

app_name = 'invoices'
urlpatterns = [
# Invoice
# -----------------------------------------------------------------------------
    # ex: /invoices/
    path('', views.Invoice_IndexView.as_view(), name='invoice_index'),

    # ex: /invoices/5/
    path('<int:pk>/', views.Invoice_DetailView.as_view(), name='invoice_detail'),


# Payment
# -----------------------------------------------------------------------------
    # ex: /invoices/payments/
    path('payments/', views.Payment_IndexView.as_view(), name='payment_index'),

    # ex: /invoices/payment/new
    path('payment/new', views.Payment_CreateView.as_view(), name='payment_create'),

    # ex: /invoices/payment/bulk/new
    path('payment/bulk/new', views.LotPayment_CreateView.as_view(), name='payment_bulk_create'),


# Receipt
# -----------------------------------------------------------------------------
    # ex: /invoices/receipts/
    path('receipts/', views.Receipt_IndexView.as_view(), name='receipt_index'),

    # ex: /invoices/receipts/1/
    path('receipts/<int:pk>/', views.Receipt_DetailView.as_view(), name='receipt_detail'),


# AJAX HELPER URLS
# ------------------------------------------------------------------------------
    path('ajax/load-customer-invoices/', views.load_customer_invoices, name='load_customer_invoices'),
    path('ajax/fetch-invoice-details/', views.fetch_invoice_details, name='fetch_invoice_details'),
    path('ajax/load-customer-inward-orders/', views.load_customer_inward_orders, name='load_customer_inward_orders'),
    path('ajax/load-order-amount-pending/', views.load_order_amount_pending, name='load_order_amount_pending'),
]