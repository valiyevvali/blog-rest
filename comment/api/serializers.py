from django.contrib.auth.models import User
from rest_framework import serializers

from comment.models import Comment
from post.models import Post


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude=['created_date','author']


    def validate(self, attrs):
        print(attrs)
        if attrs['parent']:
            if attrs['parent'].post != attrs['post']:
                raise serializers.ValidationError('Something went wrong')
        return attrs

#Alternative is depth
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','first_name')


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=('id','title','slug')

class CommentListSerializer(serializers.ModelSerializer):
    replies=serializers.SerializerMethodField()
    author=UserSerializer()
    post=PostCommentSerializer()
    class Meta:
        model = Comment
        fields='__all__'


    def get_replies(self,obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(),many=True).data


class CommentDeleteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields=['text',]







