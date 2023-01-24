from rest_framework.urls import path
from .views import (InsertVideoContent, GetProductVideoContent, GetProductContent, \
                    AddProdContent, AddPreContentsFile, AddLocationContents, AddPropsContents, AddModelContents, \
                    AddPostProdContentDelivery, AddPostProdContentEditing, AddPostProdContentInternal,
                    CreateFileComment, CreateVideoComment, CreateCommonComment, getFileComment, getCommonComment,
                    getVideoComment, GetAdminProductContent, GetDeveloperFileContent, GetDeveloperVideoContent,
                    ApproveFileContent, ApproveVideoContent, GetAdminProductVideoContent)

app_name = 'contents'

urlpatterns = [
    path('insert-video/<int:pk>/', InsertVideoContent.as_view(), name="Insert_Video"),
    path('product-video/<int:pk>/', GetProductVideoContent.as_view(), name="Product_Video"),
    path('adminproduct-video/<int:pk>/', GetAdminProductVideoContent.as_view(), name="Admin_Product_Video"),
    path('product-contents/<int:pk>/', GetProductContent.as_view(), name="Prod_Contents"),
    path('admin-product-contents/<int:pk>/', GetAdminProductContent.as_view(), name="Admin_Prod_Contents"),
    path('dev-filecontent/<int:pk>/', GetDeveloperFileContent.as_view(), name="Developer_file"),
    path('dev-videocontent/<int:pk>/', GetDeveloperVideoContent.as_view(), name="Developer_video"),
    path('addlocation/<int:pk>/', AddLocationContents.as_view(), name="Add_Location"),
    path('addprops/<int:pk>/', AddPropsContents.as_view(), name="Add_props"),
    path('addmodel/<int:pk>/', AddModelContents.as_view(), name="Add_model"),
    path('addprod-contents/<int:pk>/', AddProdContent.as_view(), name="Add_Production_content"),
    path('addpost-editing/<int:pk>/', AddPostProdContentEditing.as_view(), name="Add_Post_Editing"),
    path('addpost-internal/<int:pk>/', AddPostProdContentInternal.as_view(), name="Add_Post_Internal"),
    path('addpost-delivery/<int:pk>/', AddPostProdContentDelivery.as_view(), name="Add_Post_Delivery"),
    path('filecomments/<int:pk>/', getFileComment.as_view(), name="fileComments"),
    path('videocomments/<int:pk>/', getVideoComment.as_view(), name="videoComments"),
    path('commoncomments/<int:pk>/', getCommonComment.as_view(), name="commonComments"),
    path('addfile-comment/<int:pk>/', CreateFileComment.as_view(), name="File_Comment"),
    path('addvideo-comment/<int:pk>/', CreateVideoComment.as_view(), name="Video_Comment"),
    path('addcommon-comment/<int:pk>/', CreateCommonComment.as_view(), name="Common_Comment"),
    path('add-file/<int:pk>/', AddPreContentsFile.as_view(), name="Add_File"),
    path('approvefile/<int:pk>/', ApproveFileContent.as_view(), name="ApproveFile"),
    path('approvevideo/<int:pk>/', ApproveVideoContent.as_view(), name="ApproveVideo"),
]
