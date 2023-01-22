from django.urls import path
from .views import Create_User, Delete_User, Update_User, Login_User, Client_List, Developer_List, Login_Admin, \
    Login_Developer
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('createuser/', Create_User.as_view(), name="user_create"),
    path('delete/<int:pk>/', Delete_User.as_view(), name="delete_user"),
    path('update/<int:pk>/', Update_User.as_view(), name="update_user"),
    path('login-user/', Login_User.as_view(), name="client_login"),
    path('login-admin/', Login_Admin.as_view(), name="admin_login"),
    path('login-developer/', Login_Developer.as_view(), name="developer_login"),
    path('client-list/', Client_List.as_view(), name="client_list"),
    path('developer-list/', Developer_List.as_view(), name="developer_list"),
    path('refresh-token/', TokenRefreshView.as_view(), name="refresh_token"),
]
