from django.urls import path, include


app_name = "api_v1"
urlpatterns = [
    path('user/', include("re_work.user.api.urls", namespace="user")),
    path('product/', include("re_work.product.api.urls", namespace="products")),
    path('contents/', include("re_work.content.api.urls", namespace="contents")),
]
