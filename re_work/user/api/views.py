from django.contrib.auth import login, authenticate
from django.db.models import Q

from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from re_work.user.api.serializer import UserData, UserCreation, UserSelection
from re_work.user.models import User

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        "password", "old_password", "new_password1", "new_password2"
    )
)


class Create_User(CreateAPIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = UserCreation

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": _("User Created!")},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class Update_User(UpdateAPIView):
    serializer_class = UserCreation
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(id=self.kwargs["pk"])
        serializer = UserData(user, many=False)
        return Response({"user_profile": serializer.data}, status=status.HTTP_200_OK)


class Delete_User(DestroyAPIView):
    serializer_class = UserCreation
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()


class User_List(RetrieveAPIView):
    serializer_class = UserCreation
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class Client_List(APIView):
    serializer_class = UserSelection
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, *args, **kwargs):
        queryset = User.objects.filter(user_type=1)
        serializer = self.serializer_class(queryset, many=True)
        return Response({"details": serializer.data}, status=status.HTTP_200_OK)


class Developer_List(APIView):
    serializer_class = UserSelection
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, *args, **kwargs):
        scripter = User.objects.filter(Q(user_type=3) | Q(user_type=5))
        video_editor = User.objects.filter(Q(user_type=4) | Q(user_type=5))
        serializer_script = self.serializer_class(scripter, many=True)
        serializer_video = self.serializer_class(video_editor, many=True)
        return Response({"script": serializer_script.data, "video": serializer_video.data}, status=status.HTTP_200_OK)


class Login_User(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        try:
            user = authenticate(username=email, password=password)
            if user is not None:
                user_details = User.objects.get(email=email)
                if user_details.is_client:
                    refresh = RefreshToken.for_user(user)
                    login(request, user)
                    ser = UserData(user_details, many=False)
                    response = {
                        "user_profile": ser.data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "The user is not a client!",
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "message": "Email or password doesn't match!",
                }, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


class Login_Admin(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        try:
            user = authenticate(username=email, password=password)
            if user is not None:
                user_details = User.objects.get(email=email)
                if user_details.is_admin:
                    refresh = RefreshToken.for_user(user)
                    login(request, user)
                    ser = UserData(user_details, many=False)
                    response = {
                        "user_profile": ser.data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "The user is not a Admin!",
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "message": "Email or password doesn't match!",
                }, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


class Login_Developer(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        try:
            user = authenticate(username=email, password=password)
            if user is not None:
                user_details = User.objects.get(email=email)
                if user_details.is_full_stack or user_details.is_script_writer or user_details.is_video_editor:
                    refresh = RefreshToken.for_user(user)
                    login(request, user)
                    ser = UserData(user_details, many=False)
                    response = {
                        "user_profile": ser.data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "The user is not a developer!",
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "message": "Email or password doesn't match!",
                }, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
