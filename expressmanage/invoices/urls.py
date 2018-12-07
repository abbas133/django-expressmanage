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
    # ex: /invoices/payment/new
    path('payment/new', views.Payment_CreateView.as_view(), name='payment_create'),

    # # ex: /invoices/new/
    # path('new/', views.Product_CreateView.as_view(), name='product_create'),

    # # CONTAINER TYPE
    # # ex: /invoices/ct/
    # path('ct/', views.Ct_IndexView.as_view(), name='ct_index'),

    # # ex: /invoices/ct/1/
    # path('ct/<int:pk>/', views.Ct_DetailView.as_view(), name='ct_detail'),

    # # ex: /invoices/ct/new
    # path('ct/new', views.Ct_CreateView.as_view(), name='ct_create'),

    # # RATE SLAB
    # # ex: /invoices/rs/
    # path('rs/', views.Rate_IndexView.as_view(), name='rate_index'),

    # # ex: /invoices/rs/1/
    # path('rs/<int:pk>/', views.Rate_DetailView.as_view(), name='rate_detail'),

    # # ex: /invoices/rs/new
    # path('rs/new', views.Rate_CreateView.as_view(), name='rate_create'),
]