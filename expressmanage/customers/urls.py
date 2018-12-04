from django.urls import path

from . import views

app_name = 'customers'
urlpatterns = [
    # ex: /customers/
    path('', views.Customer_IndexView.as_view(), name='customer_index'),

    # ex: /customers/5/
    path('<int:pk>/', views.Customer_DetailView.as_view(), name='customer_detail'),

    # ex: /customers/new/
    path('new/', views.Customer_CreateView.as_view(), name='customer_create'),
]