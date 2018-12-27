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


    # Receipt
    # -----------------------------------------------------------------------------
    # ex: /invoices/receipts/
    path('receipts/', views.Receipt_IndexView.as_view(), name='receipt_index'),

    # ex: /invoices/receipts/1/
    path('receipts/<int:pk>/', views.Receipt_DetailView.as_view(), name='receipt_detail'),
]