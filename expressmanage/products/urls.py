from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    # PRODUCT
    # ------------------------------------------------------------------------------
    # ex: /products/
    path('', views.Product_IndexView.as_view(), name='product_index'),

    # ex: /products/5/
    path('<int:pk>/', views.Product_DetailView.as_view(), name='product_detail'),

    # ex: /products/new/
    path('new/', views.Product_CreateView.as_view(), name='product_create'),

    # ex: /products/e/5/
    path('e/<int:pk>/', views.Product_UpdateView.as_view(), name='product_update'),

    # ex: /products/d/5/
    path('d/<int:pk>/', views.Product_DeleteView.as_view(), name='product_delete'),


    # CONTAINER TYPE
    # ------------------------------------------------------------------------------
    # ex: /products/containers/
    path('containers/', views.ContainerType_IndexView.as_view(), name='container_index'),

    # ex: /products/containers/1/
    path('containers/<int:pk>/', views.ContainerType_DetailView.as_view(), name='container_detail'),

    # ex: /products/containers/new
    path('containers/new', views.ContainerType_CreateView.as_view(), name='container_create'),

    # ex: /products/containers/e/5/
    path('containers/e/<int:pk>/', views.ContainerType_UpdateView.as_view(), name='container_update'),

    # ex: /products/containers/d/5/
    path('containers/d/<int:pk>/', views.ContainerType_DeleteView.as_view(), name='container_delete'),
]