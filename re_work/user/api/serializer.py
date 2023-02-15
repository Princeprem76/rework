from rest_framework import serializers, status
from rest_framework.response import Response

from re_work.product.models import Product
from re_work.user.models import User


class UserData(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'get_image', 'phone', 'address']


class DeveloperData(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'get_image', 'phone', 'address', 'user_type']


class UserSelection(serializers.ModelSerializer):
    active_product = serializers.SerializerMethodField("get_active_project")
    completed_product = serializers.SerializerMethodField("get_completed_project")

    class Meta:
        model = User
        fields = ["id", "name", 'active_product', 'completed_product']

    def get_active_project(self, obj):
        counts = Product.objects.filter(client_id=obj.id, has_completed=False).count()
        return counts

    def get_completed_project(self, obj):
        counts = Product.objects.filter(client_id=obj.id, has_completed=True).count()
        return counts


class UserCreation(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'phone', 'address', 'user_image', 'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        name = validated_data.get('name')
        user_type = validated_data.get('user_type')
        if not (email or password or name or user_type):
            raise serializers.ValidationError(
                " Missing mandatory fields data."
            )
        return validated_data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        return user
