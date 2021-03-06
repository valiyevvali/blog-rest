from rest_framework import serializers
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    url=serializers.HyperlinkedIdentityField(
        view_name="post:detail",
        lookup_field='slug'
    )
    username=serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'username',
            'title',
            'content',
            'created_date',
            'url',
            'slug',
            'image',
            'modified_by'
        ]
    def get_username(self,obj):
        return str(obj.author.username)





class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image'
        ]
    '''override methods'''
    # def save(self, **kwargs):
    #     print(type(kwargs))
    #     for i in kwargs:
    #         print(i)
    #     return True

    # def create(self, validated_data):
    #     print(self.context)
    #     return Post.objects.create(author=self.context['request'].user, **validated_data)

    # def update(self, instance, validated_data):
    #     instance.title=validated_data.get('title',instance.title)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.save()
    #     return instance

    # def validate_image(self, value):
    #     if not value:
    #         raise serializers.ValidationError('content must be entered. 4')
    #     return value


    # def validate_title(self,value):
    #     if len(value) < 8:
    #         raise serializers.ValidationError('Title must be entered. 8')
    #     return value

