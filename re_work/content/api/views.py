from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import VideoContentSerializer, PreContentSerializer, ProductionContentSerializer, \
    PostContentSerializer, CommentSerializer, FileContentSerializer, FileContentSerializerAdmin, \
    VideoContentSerializerAdmin
from ..models import Section, VideoContent, PreProductionContent, PostProductionContent, ProductionContent, FileContent, \
    CommonContent, Comments
from push_notifications.models import APNSDevice, GCMDevice

# device = GCMDevice.objects.get(registration_id=gcm_reg_id)
from ...product.models import Product


class InsertVideoContent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            video_edit = self.request.user.is_video_editor
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            full_stack = self.request.user.is_full_stack
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            if not (
                    admin or video_edit or admin_staff or full_stack or section.product.video_editor == self.request.user):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

            section = Section.objects.get(product_id=products_id)
            video, _ = VideoContent.objects.get_or_create(video_url=self.request.data['video_url'],
                                                          duration=self.request.data['duration'])
            section.video_content.add(video)
            return Response({'details': 'Video added!'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'details': 'Error!'})


class GetProductVideoContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            products = section.video_content.all().filter(has_approved=True)
            serializer = VideoContentSerializer(products, many=True)
            return Response({'contents': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No video present'}, status=status.HTTP_200_OK)


class GetAdminProductVideoContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            products = section.video_content.all()
            serializer = VideoContentSerializerAdmin(products, many=True)
            return Response({'contents': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No video present'}, status=status.HTTP_200_OK)


class GetPreContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            products = section.pre_contents.all()
            file = section.pre_contents.all().first()
            f = file.file_contents.all().filter(has_approved=True)
            file_ser = FileContentSerializer(f, many=True)
            serializer = PreContentSerializer(products, many=True)
            return Response({'contents': serializer.data, 'file': file_ser.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No content present'}, status=status.HTTP_200_OK)


class GetAdminPreContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            products_id = self.kwargs['pk']
            prod = Product.objects.get(id=products_id)
            if not (self.request.user.is_admin or self.request.user.is_staff_admin):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            section = Section.objects.get(product_id=products_id)
            products = section.pre_contents.all()
            file = section.pre_contents.all().first()
            f = file.file_contents.all()
            file_ser = FileContentSerializerAdmin(f, many=True)
            serializer = PreContentSerializer(products, many=True)
            return Response({'contents': serializer.data, 'file': file_ser.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No content present'}, status=status.HTTP_200_OK)


class GetDeveloperFileContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products_id = self.kwargs['pk']
        prod = Product.objects.get(id=products_id)
        if prod.script_writer != self.request.user:
            return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        section = Section.objects.get(product_id=products_id)
        file = section.pre_contents.all().first().file_contents.all()
        file_ser = FileContentSerializerAdmin(file, many=True)
        return Response({'details': file_ser.data}, status=status.HTTP_200_OK)


class GetDeveloperVideoContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products_id = self.kwargs['pk']
        prod = Product.objects.get(id=products_id)
        if prod.video_editor != self.request.user:
            return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        section = Section.objects.get(product_id=products_id)
        video = section.video_content.all()
        vid_ser = VideoContentSerializerAdmin(video, many=True)
        return Response({'details': vid_ser.data}, status=status.HTTP_200_OK)


class GetProdContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            products = section.production_contents.all()
            serializer = ProductionContentSerializer(products, many=True)
            return Response({'contents': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No content present'}, status=status.HTTP_200_OK)


class GetPostContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            products = section.production_contents.all()
            serializer = PostContentSerializer(products, many=True)
            return Response({'contents': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No content present'}, status=status.HTTP_200_OK)


class AddPreContentsFile(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            script = self.request.user.is_script_writer
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            full_stack = self.request.user.is_full_stack
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            if not (admin or script or admin_staff or full_stack or section.product.script_writer == self.request.user):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            file, _ = FileContent.objects.get_or_create(files=self.request.data['files'])
            pre = section.pre_contents.all().first()
            pre_file = pre.file_contents.add(file)
            return Response({'details': 'File Added created'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'details': 'Error!'})


class AddLocationContents(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            if not (admin or admin_staff):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            name, _ = CommonContent.objects.get_or_create(name=self.request.data['name'])
            pre = section.pre_contents.all().first()
            pre_location = pre.location.add(name)
            return Response({'details': 'Location created'}, status=status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Error!'})


class AddPropsContents(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            if not (admin or admin_staff):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            prop, _ = CommonContent.objects.get_or_create(name=self.request.data['props'])
            pre = section.pre_contents.all().first()
            pre_prop = pre.props.add(prop)
            return Response({'details': 'Props created'}, status=status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Error!'})


class AddModelContents(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            if not (admin or admin_staff):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            models, _ = CommonContent.objects.get_or_create(name=self.request.data['model'])
            pre = section.pre_contents.all().first()
            pre_model = pre.location.add(models)
            return Response({'details': 'Models created'}, status=status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Error!'})


class AddProdContent(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            if not (admin or admin_staff):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            date = self.request.data['date']
            prod = section.production_contents.all().first()
            prod.video_completion = date
            prod.save()
            return Response({'details': 'Created'}, status=status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Error!'})


class AddPostProdContentEditing(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            if not (admin or admin_staff):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            editings, _ = CommonContent.objects.get_or_create(name=self.request.data['editing'])
            postp = section.post_contents.all().first()
            post_editing = postp.editing.add(editings)
            return Response({'details': 'Created'}, status=status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Error!'})


class AddPostProdContentInternal(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            if not (admin or admin_staff):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            internals, _ = CommonContent.objects.get_or_create(name=self.request.data['editing'])
            postp = section.post_contents.all().first()
            post_internal = postp.editing.add(internals)
            return Response({'details': 'Created'}, status=status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Error!'})


class AddPostProdContentDelivery(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            if not (admin or admin_staff):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            date = self.request.data['date']
            postp = section.post_contents.all().first()
            postp.delivery = date
            postp.save()
            return Response({'details': 'Created'}, status=status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Error!'})


class get_comment(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        com = self.kwargs['pk']
        commentss = Comments.objects.filter(id=com)
        serializer = CommentSerializer(commentss, many=True)
        return Response({'details': serializer.data})


class CreateVideoComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        comment = request.data['comment']
        com, _ = Comments.objects.get_or_create(comment=comment, user=self.request.user)
        video = VideoContent.objects.get(id=content_id)
        video.comment.add(com)
        video.save()
        return Response({"details": "Comment Added!"})


class CreateVideoCommentReply(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        comment = request.data['comment']
        com, _ = Comments.objects.get_or_create(comment=comment, user=self.request.user)
        video = VideoContent.objects.get(id=content_id)
        if video.comment is None:
            video.comment = com
            video.save()
            return Response({"details": "Comment Added!"})
        parent_id = video.comment
        com.parents = parent_id
        com.save()
        return Response({"details": "Comment Added!"})


class CreateFileComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        comment = request.data['comment']
        com, _ = Comments.objects.get_or_create(comment=comment, user=self.request.user)
        file = FileContent.objects.get(id=content_id)
        file.comment.add(com)
        file.save()
        return Response({"details": "Comment Added!"})


class CreateFileCommentReply(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        comment = request.data['comment']
        com, _ = Comments.objects.get_or_create(comment=comment, user=self.request.user)
        file = FileContent.objects.get(id=content_id)
        if file.comment is None:
            file.comment = com
            file.save()
            return Response({"details": "Comment Added!"})
        parent_id = file.comment
        com.parents = parent_id
        com.save()
        return Response({"details": "Comment Added!"})


class CreateCommonCommentReply(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        comment = request.data['comment']
        com, _ = Comments.objects.get_or_create(comment=comment, user=self.request.user)
        common = CommonContent.objects.get(id=content_id)
        if common.comment is None:
            common.comment = com
            common.save()
            return Response({"details": "Comment Added!"})
        parent_id = common.comment
        com.parents = parent_id
        com.save()
        return Response({"details": "Comment Added!"})


class CreateCommonComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        comment = request.data['comment']
        com, _ = Comments.objects.get_or_create(comment=comment, user=self.request.user)
        common = CommonContent.objects.get(id=content_id)
        common.comment.add(com)
        common.save()
        return Response({"details": "Comment Added!"})


class ApproveFileContent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_id = self.kwargs['pk']
        admin = self.request.user.is_admin
        admin_staff = self.request.user.is_staff_admin
        if not (admin or admin_staff):
            return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        file = FileContent.objects.get(id=file_id)
        file.has_approved = True
        file.save()
        return Response({'details': 'File has been Approved'}, status=status.HTTP_202_ACCEPTED)


class ApproveVideoContent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        video_id = self.kwargs['pk']
        admin = self.request.user.is_admin
        admin_staff = self.request.user.is_staff_admin
        if not (admin or admin_staff):
            return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        video = VideoContent.objects.get(id=video_id)
        video.has_approved = True
        video.save()
        return Response({'details': 'Video has been Approved'}, status=status.HTTP_202_ACCEPTED)


'''Total 6 Api'''
