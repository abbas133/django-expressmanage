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

    # ex: /customers/e/5/
    path('e/<int:pk>/', views.Customer_UpdateView.as_view(), name='customer_update'),

    # ex: /customers/d/5/
    path('d/<int:pk>/', views.Customer_DeleteView.as_view(), name='customer_delete'),

]