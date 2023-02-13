from datetime import datetime

from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import VideoContentSerializer, PreContentSerializer, ProductionContentSerializer, \
    PostContentSerializer, CommentSerializer, FileContentSerializer, FileContentSerializerAdmin, \
    VideoContentSerializerAdmin, CommonContentSerializer, FileContentUpdateSerializer, VideoContentUpdateSerializer
from ..models import Section, VideoContent, PreProductionContent, PostProductionContent, ProductionContent, FileContent, \
    CommonContent, Comments
from push_notifications.models import APNSDevice, GCMDevice

# device = GCMDevice.objects.get(registration_id=gcm_reg_id)
from ...core.permissions import IsAdminStaff
from ...notification.mixins import send_push_notification
from ...product.models import Product
from ...user.models import User


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
            video = VideoContent.objects.create(name=self.request.data['name'],
                                                          video_url=self.request.data['video_url'],
                                                          duration=self.request.data['duration'])
            section.video_content.add(video)
            section.save()
            messages = "New Video has been uploaded to {}! Approval is remaining".format(section.product__product_name)
            users = User.objects.filter(user_type__in=[2, 6])
            print(users)
            send_push_notification(message=messages, users=users, product_id=products_id, type="video")
            return Response({'details': 'Video added!'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'details': 'Error!'})


class GetProductVideoContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            products = section.video_content.all().filter(has_approved=True).order_by('created_at')
            serializer = VideoContentSerializer(products, many=True)
            return Response({'contents': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No video present'}, status=status.HTTP_200_OK)


class PatchPreContent(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminStaff]
    serializer_class = PreContentSerializer
    queryset = PreProductionContent.objects.all()
    lookup_url_kwarg = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'details': 'Updated!'}, status=status.HTTP_200_OK)


class PatchPostContent(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminStaff]
    serializer_class = PostContentSerializer
    queryset = PostProductionContent.objects.all()
    lookup_url_kwarg = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'details': 'Updated!'}, status=status.HTTP_200_OK)


class PatchProdContent(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminStaff]
    serializer_class = ProductionContentSerializer
    queryset = ProductionContent.objects.all()
    lookup_url_kwarg = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'details': 'Updated!'}, status=status.HTTP_200_OK)


class PatchCommonContent(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminStaff]
    serializer_class = CommonContentSerializer
    queryset = CommonContent.objects.all()
    lookup_url_kwarg = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'details': 'Updated!'}, status=status.HTTP_200_OK)


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


class GetAdminProductContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            products_id = self.kwargs['pk']
            prod = Product.objects.get(id=products_id)
            if not (self.request.user.is_admin or self.request.user.is_staff_admin):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            section = Section.objects.get(product_id=products_id)
            prodproducts = section.production_contents.all()
            prodserializer = ProductionContentSerializer(prodproducts, many=True)
            postproducts = section.post_contents.all()
            postserializer = PostContentSerializer(postproducts, many=True)
            products = section.pre_contents.all()
            file = section.pre_contents.all().first()
            f = file.file_contents.all()
            file_ser = FileContentSerializerAdmin(f, many=True)
            serializer = PreContentSerializer(products, many=True)
            return Response(
                {'precontents': serializer.data, 'files': file_ser.data, 'prodcontents': prodserializer.data,
                 'postcontents': postserializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No content present'}, status=status.HTTP_200_OK)


class GetDeveloperFileContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products_id = self.kwargs['pk']
        prod = Product.objects.get(id=products_id)
        if not (prod.script_writer == self.request.user and (
                self.request.user.is_script_writer or self.request.user.is_full_stack)):
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
        if not (prod.video_editor == self.request.user and (
                self.request.user.is_video_editor or self.request.user.is_full_stack)):
            return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        section = Section.objects.get(product_id=products_id)
        video = section.video_content.all()
        vid_ser = VideoContentSerializerAdmin(video, many=True)
        return Response({'details': vid_ser.data}, status=status.HTTP_200_OK)


class GetProductContent(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
            prodproducts = section.production_contents.all()
            prodserializer = ProductionContentSerializer(prodproducts, many=True)
            postproducts = section.post_contents.all()
            postserializer = PostContentSerializer(postproducts, many=True)
            preproducts = section.pre_contents.all()
            file = section.pre_contents.all().first()
            f = file.file_contents.all().filter(has_approved=True)
            file_ser = FileContentSerializer(f, many=True)
            preserializer = PreContentSerializer(preproducts, many=True)
            return Response(
                {'precontents': preserializer.data, 'files': file_ser.data, 'prodcontents': prodserializer.data,
                 'postcontents': postserializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No content present'}, status=status.HTTP_204_NO_CONTENT)


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
            file = FileContent.objects.create(name=self.request.data['name'],
                                                        files=self.request.data['files'])
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
            name = CommonContent.objects.create(name=self.request.data['name'])
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
            prop = CommonContent.objects.create(name=self.request.data['props'])
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
            models = CommonContent.objects.create(name=self.request.data['model'])
            pre = section.pre_contents.all().first()
            pre_model = pre.model.add(models)
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
            date = datetime.strptime(request.data['date'], '%Y-%m-%d %H:%M:%S')
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
            editings = CommonContent.objects.create(name=self.request.data['editing'])
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
            internals = CommonContent.objects.create(name=self.request.data['internal'])
            postp = section.post_contents.all().first()
            post_internal = postp.internal.add(internals)
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
            date = datetime.strptime(request.data['date'], '%Y-%m-%d %H:%M:%S')
            postp = section.post_contents.all().first()
            postp.delivery = date
            postp.save()
            return Response({'details': 'Created'}, status=status.HTTP_201_CREATED)

        except:
            return Response({'details': 'Error!'})


class getFileComment(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        com = self.kwargs['pk']
        commentss = FileContent.objects.get(id=com)
        c = commentss.comment.all()
        serializer = CommentSerializer(c, many=True)
        return Response({'details': serializer.data})


class getVideoComment(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        com = self.kwargs['pk']
        commentss = VideoContent.objects.get(id=com)
        c = commentss.comment.all()
        serializer = CommentSerializer(c, many=True)
        return Response({'details': serializer.data})


class getCommonComment(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        com = self.kwargs['pk']
        commentss = CommonContent.objects.get(id=com)
        c = commentss.comment.all()
        serializer = CommentSerializer(c, many=True)
        return Response({'details': serializer.data})


class CreateVideoComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        comment = request.data['comment']
        com = Comments.objects.create(comment=comment, user=self.request.user)
        video = VideoContent.objects.get(id=content_id)
        video.comment.add(com)
        video.save()
        sec = Section.objects.filter(video_content=content_id)
        sec = sec.first()
        pro = Product.objects.get(id=sec.product_id)
        users = [pro.video_editor_id, pro.client_id]
        for us in User.objects.filter(user_type__in=[2, 6]):
            users.append(us.id)
        users.remove(request.user.id)
        messages = "New comment has been added to Video!"
        send_push_notification(message=messages, users=users, product_id=sec.product_id, type="video")
        return Response({"details": "Comment Added!"})


class CreateVideoCommentReply(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        comment = request.data['comment']
        com = Comments.objects.create(comment=comment, user=self.request.user)
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
        com = Comments.objects.create(comment=comment, user=self.request.user)
        file = FileContent.objects.get(id=content_id)
        file.comment.add(com)
        file.save()
        sec = Section.objects.filter(video_content=content_id)
        sec = sec.first()
        pro = Product.objects.get(id=sec.product_id)
        users = [pro.script_writer_id, pro.client_id]
        for us in User.objects.filter(user_type__in=[2, 6]):
            users.append(us.id)
        users.remove(request.user.id)
        messages = "New comment has been added to File!"
        send_push_notification(message=messages, users=users, product_id=sec.product_id, type="file")
        return Response({"details": "Comment Added!"})


class CreateFileCommentReply(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content_id = self.kwargs['pk']
        comment = request.data['comment']
        com = Comments.objects.create(comment=comment, user=self.request.user)
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
        com = Comments.objects.create(comment=comment, user=self.request.user)
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
        com = Comments.objects.create(comment=comment, user=self.request.user)
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
        file.has_approved = request.data['has_approved']
        file.comment_time = datetime.strptime(request.data['comment_time'], '%Y-%m-%d %H:%M:%S')
        file.save()
        messages = "New Script has been uploaded! You can provide comment till {}".format(request.data['comment_time'])
        send_push_notification(message=messages, users=[], product_id=id, type="video")
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
        video.has_approved = request.data['has_approved']
        video.comment_time = datetime.strptime(request.data['comment_time'], '%Y-%m-%d %H:%M:%S')
        video.save()
        messages = "New Video has been uploaded! You can provide comment till {}".format(request.data['comment_time'])
        send_push_notification(message=messages, users=[], product_id=id, type="video")
        return Response({'details': 'Video has been Approved'}, status=status.HTTP_202_ACCEPTED)


class TurnoffFileComment(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminStaff]
    serializer_class = FileContentUpdateSerializer
    queryset = FileContent.objects.all()
    lookup_url_kwarg = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'details': 'Updated!'}, status=status.HTTP_200_OK)


class TurnoffVideoComment(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminStaff]
    serializer_class = VideoContentUpdateSerializer
    queryset = VideoContent.objects.all()
    lookup_url_kwarg = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'details': 'Updated!'}, status=status.HTTP_200_OK)
