from rest_framework import serializers

from re_work.content.models import VideoContent, CommonContent, PreProductionContent, ProductionContent, \
    PostProductionContent, Comments, FileContent


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name", read_only=True)

    # children_comment = serializers.SerializerMethodField("get_children_comment")

    class Meta:
        model = Comments
        fields = ['name', 'comment']

    # def get_children_comment(self, obj):
    #     child_comment = Comments.objects.filter(parents_id=obj.id).order_by("created_at")
    #     children_comments_detail = CommentSerializer(
    #         child_comment, many=True, read_only=True
    #     )
    #     return children_comments_detail.data


class VideoContentSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField("get_count")

    class Meta:
        model = VideoContent
        fields = ['id', 'video_url', 'duration', 'name', 'comment_count', 'comment_off']

    def get_count(self, obj):
        counts = VideoContent.objects.get(id=obj.id).comment.all().count()
        return counts


class VideoContentSerializerAdmin(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField("get_count")

    class Meta:
        model = VideoContent
        fields = ['id', 'video_url', 'duration', 'name', 'has_approved', 'comment_count', 'comment_off']

    def get_count(self, obj):
        counts = VideoContent.objects.get(id=obj.id).comment.all().count()
        return counts


class FileContentSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField("get_count")

    class Meta:
        model = FileContent
        fields = ['id', 'files', 'name', "comment_count", 'comment_off']

    def get_count(self, obj):
        counts = FileContent.objects.get(id=obj.id).comment.all().count()
        return counts


class FileContentSerializerAdmin(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField("get_count")

    class Meta:
        model = FileContent
        fields = ['id', 'files', 'name', 'has_approved', 'comment_count', 'comment_off']

    def get_count(self, obj):
        counts = FileContent.objects.get(id=obj.id).comment.all().count()
        return counts


class CommonContentSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField("get_count")

    class Meta:
        model = CommonContent
        fields = ['id', 'name', 'comment_count', 'comment_off']

    def get_count(self, obj):
        counts = CommonContent.objects.get(id=obj.id).comment.all().count()
        return counts


class PreContentSerializer(serializers.ModelSerializer):
    location = CommonContentSerializer(many=True, read_only=True, allow_null=True)
    props = CommonContentSerializer(many=True, read_only=True, allow_null=True)
    model = CommonContentSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = PreProductionContent
        fields = ['id', 'location', 'props', 'model', 'has_location', 'has_props',
                  'has_file', 'has_model', 'complete_location', 'complete_props', 'complete_file',
                  'complete_model', ]



class ProductionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionContent
        fields = ['id', 'video_completion', 'complete_video']


class PostContentSerializer(serializers.ModelSerializer):
    editing = CommonContentSerializer(many=True, read_only=True, allow_null=True)
    internal = CommonContentSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = PostProductionContent
        fields = ['id', 'editing', 'internal', 'delivery', 'has_editing', 'has_internal', 'has_delivery',
                  'complete_editing', 'complete_internal', 'complete_delivery']

