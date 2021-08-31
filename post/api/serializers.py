from rest_framework import serializers
from post.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=[
            'author',
            'title',
            'content',
            'created_date',
            'slug',
            'image',
            'modified_by'
        ]

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=[
            'title',
            'content',
            'image'
        ]