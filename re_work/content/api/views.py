from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import VideoContentSerializer, PreContentSerializer, ProductionContentSerializer, \
    PostContentSerializer, CommentSerializer
from ..models import Section, VideoContent, PreProductionContent, PostProductionContent, ProductionContent, FileContent, \
    CommonContent, Comments


class InsertVideoContent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            video_edit = self.request.user.is_video_editor
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            full_stack = self.request.user.is_full_stack
            if not (admin or video_edit or admin_staff or full_stack):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            products_id = self.kwargs['pk']
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
            products = section.video_content.all()
            serializer = VideoContentSerializer(products, many=True)
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
            serializer = PreContentSerializer(products, many=True)
            return Response({'contents': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'contents': 'No video present'}, status=status.HTTP_200_OK)


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
            return Response({'contents': 'No video present'}, status=status.HTTP_200_OK)


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
            return Response({'contents': 'No video present'}, status=status.HTTP_200_OK)


class AddPreContentsFile(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            script = self.request.user.is_script_writer
            admin = self.request.user.is_admin
            admin_staff = self.request.user.is_staff_admin
            full_stack = self.request.user.is_full_stack
            if not (admin or script or admin_staff or full_stack):
                return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
            products_id = self.kwargs['pk']
            section = Section.objects.get(product_id=products_id)
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
