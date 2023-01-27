from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from re_work.core.permissions import IsAdminStaff
from re_work.product.api.serializer import ProductCreateSerializer, ProductDataSerializer, ProductAdminDataSerializer
from re_work.product.models import Product


class CreateProduct(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]


class UpdateProduct(UpdateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminStaff]
    queryset = Product.objects.all()
    lookup_url_kwarg = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'details': 'Updated!'}, status=status.HTTP_200_OK)


class ProductList(APIView):
    serializer_class = ProductAdminDataSerializer
    permission_classes = [IsAuthenticated, IsAdminStaff]

    def get(self, request, *args, **kwargs):
        # admin = self.request.user.is_admin
        # admin_staff = self.request.user.is_staff_admin
        # if not (admin or admin_staff):
        #     return Response({'details': 'User not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        product = Product.objects.filter(client_id=self.kwargs["pk"], has_completed=False)
        serializer = self.serializer_class(product, many=True)
        return Response({"product_details": serializer.data}, status=status.HTTP_200_OK)


class ProductComplete(APIView):
    permission_classes = [IsAuthenticated, IsAdminStaff]

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['pk'])
        product.has_completed = True
        product.save()
        return Response({"details": "Project Completed!"}, status=status.HTTP_202_ACCEPTED)


class ClientProductView(APIView):
    serializer_class = ProductDataSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, *args, **kwargs):
        product = Product.objects.filter(client_id=self.request.user.id, has_completed=False)
        serializer = self.serializer_class(product, many=True)
        return Response({"product_details": serializer.data}, status=status.HTTP_200_OK)


class ClientArchieveProductView(APIView):
    serializer_class = ProductDataSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, *args, **kwargs):
        product = Product.objects.filter(client_id=self.request.user.id, has_completed=True)
        serializer = self.serializer_class(product, many=True)
        return Response({"product_details": serializer.data}, status=status.HTTP_200_OK)


class DeveloperProductView(APIView):
    serializer_class = ProductDataSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, *args, **kwargs):
        product = Product.objects.filter(
            (Q(video_editor=self.request.user) | Q(script_writer=self.request.user)) and Q(has_completed=False))
        serializer = self.serializer_class(product, many=True)
        return Response({"product_details": serializer.data}, status=status.HTTP_200_OK)


class DeveloperArchieveProductView(APIView):
    serializer_class = ProductDataSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, *args, **kwargs):
        product = Product.objects.filter(
            (Q(video_editor=self.request.user) | Q(script_writer=self.request.user)) and Q(has_completed=True))
        serializer = self.serializer_class(product, many=True)
        return Response({"product_details": serializer.data}, status=status.HTTP_200_OK)
