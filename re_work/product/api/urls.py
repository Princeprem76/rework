from django.urls import path
from .views import CreateProduct, UpdateProduct, ClientProductView, DeveloperProductView, ProductList

app_name = 'product'

urlpatterns = [
    path('create-product/', CreateProduct.as_view(), name="product_create"),
    path('update-product/<int:pk>/', UpdateProduct.as_view(), name="product_update"),
    path('client-product/', ClientProductView.as_view(), name="client_products"),
    path('developer-product/', DeveloperProductView.as_view(), name="developer_product"),
    path('product-list/', ProductList.as_view(), name="product_list"),
]
