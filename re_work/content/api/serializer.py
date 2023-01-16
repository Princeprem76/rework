from rest_framework import serializers

from re_work.content.models import VideoContent, CommonContent, PreProductionContent, ProductionContent, \
    PostProductionContent, Comments, FileContent


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name", read_only=True)
    children_comment = serializers.SerializerMethodField("get_children_comment")

    class Meta:
        model = Comments
        fields = ['id', 'name', 'comment', 'children_comment']

    def get_children_comment(self, obj):
        child_comment = Comments.objects.filter(parents_id=obj.id)
        children_comments_detail = CommentSerializer(
            child_comment, many=True, read_only=True
        )
        return children_comments_detail.data


class VideoContentSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)

    class Meta:
        model = VideoContent
        fields = ['video_url', 'duration', 'name', 'comment']


class FileContentSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=False)

    class Meta:
        model = FileContent
        fields = ['files', 'name', 'comment']


class CommonContentSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = CommonContent
        fields = ['id', 'name', 'comment']


class PreContentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=False, read_only=True)
    file_contents = FileContentSerializer(many=True, read_only=True)
    location = CommonContentSerializer(many=True)
    props = CommonContentSerializer(many=True)
    model = CommonContentSerializer(many=True)

    class Meta:
        model = PreProductionContent
        fields = ['id', 'file_contents', 'location', 'props', 'model', 'has_video', 'has_location', 'has_props',
                  'has_file', 'has_model', 'complete_video', 'complete_location', 'complete_props', 'complete_file',
                  'complete_model', 'comments']


class ProductionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionContent
        fields = ['id', 'video_completion', 'complete_video']


class PostContentSerializer(serializers.ModelSerializer):
    editing = CommonContentSerializer(many=True)
    internal = CommonContentSerializer(many=True)

    class Meta:
        model = PostProductionContent
        fields = ['id', 'editing', 'internal', 'delivery', 'has_editing', 'has_internal', 'has_delivery',
                  'complete_delivery', 'complete_internal', 'complete_delivery']
