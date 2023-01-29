from rest_framework import serializers, status
from rest_framework.response import Response

from re_work.content.models import Section, VideoContent, PreProductionContent, ProductionContent, PostProductionContent
from re_work.product.models import Product


class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'logo']


class ProductAdminDataSerializer(serializers.ModelSerializer):
    # video_editor = serializers.CharField(source="video_editor.name", read_only=True, allow_null=True)
    # script_writer = serializers.CharField(source="script_writer.name", read_only=True, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'logo', 'video_editor', 'script_writer']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'logo', 'client', 'video_editor', 'script_writer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, validated_data):
        product_name = validated_data.get('product_name')
        description = validated_data.get('description')
        client = validated_data.get('client')
        if not (product_name or description or client):
            raise serializers.ValidationError(
                " Missing mandatory fields data."
            )
        return validated_data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.save()
        ids = product.id
        # video_content = VideoContent.objects.create()
        pre_content = PreProductionContent.objects.create()
        production_content = ProductionContent.objects.create()
        post_content = PostProductionContent.objects.create()
        contents = Section.objects.create(product_id=ids)
        # contents.video_content.add(video_content.id)
        contents.pre_contents.add(pre_content.id)
        contents.production_contents.add(production_content.id)
        contents.post_contents.add(post_content.id)
        contents.save()
        return validated_data

    def update(self, instance, validated_data):
        product = super().update(instance, validated_data)
        return product
