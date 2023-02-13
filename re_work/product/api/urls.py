from django.urls import path
from .views import CreateProduct, UpdateProduct, ClientProductView, DeveloperProductView, ProductList, \
    ClientArchieveProductView, ProductComplete, CompletedProductList

app_name = 'product'

urlpatterns = [
    path('create-product/', CreateProduct.as_view(), name="product_create"),
    path('update-product/<int:pk>/', UpdateProduct.as_view(), name="product_update"),
    path('client-product/', ClientProductView.as_view(), name="client_products"),
    path('developer-product/', DeveloperProductView.as_view(), name="developer_product"),
    path('product-list/<int:pk>/', ProductList.as_view(), name="product_list"),
    path('completed-product-list/<int:pk>/', CompletedProductList.as_view(), name="product_list"),
    path('client-archievelist/', ClientArchieveProductView.as_view(), name="Archieve_Project"),
    path('complete-product/<int:pk>/', ProductComplete.as_view(), name="Complete_Product"),
]
