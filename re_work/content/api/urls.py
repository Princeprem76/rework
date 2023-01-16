from rest_framework.urls import path
from .views import (InsertVideoContent, GetProductVideoContent, GetPostContent, GetProdContent, GetPreContent, \
                    AddProdContent, AddPreContentsFile, AddLocationContents, AddPropsContents, AddModelContents, \
                    AddPostProdContentDelivery, AddPostProdContentEditing, AddPostProdContentInternal, get_comment, )

app_name = 'contents'

urlpatterns = [
    path('insert-video/<int:pk>/', InsertVideoContent.as_view(), name="Insert_Video"),
    path('product-video/<int:pk>/', GetProductVideoContent.as_view(), name="Product_Video"),
    path('pre-contents/<int:pk>/', GetPreContent.as_view(), name="Pre_Contents"),
    path('prod-contents/<int:pk>/', GetProdContent.as_view(), name="Prod_Contents"),
    path('post-contents/<int:pk>/', GetPostContent.as_view(), name="Post_Contents"),
    path('addlocation/<int:pk>/', AddLocationContents.as_view(), name="Add_Location"),
    path('addprops/<int:pk>/', AddPropsContents.as_view(), name="Add_props"),
    path('addmodel/<int:pk>/', AddModelContents.as_view(), name="Add_model"),
    path('addprod-contents/<int:pk>/', AddProdContent.as_view(), name="Add_Production_content"),
    path('addpost-editing/<int:pk>/', AddPostProdContentEditing.as_view(), name="Add_Post_Editing"),
    path('addpost-internal/<int:pk>/', AddPostProdContentInternal.as_view(), name="Add_Post_Internal"),
    path('addpost-delivery/<int:pk>/', AddPostProdContentDelivery.as_view(), name="Add_Post_Delivery"),
    path('comments/<int:pk>/', get_comment.as_view(), name="Comments"),
]
