from rest_framework import serializers

from favourite.models import Favourite


class FavouriteListCreateApiSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favourite
        fields='__all__'

    def validate(self, attrs):
        queryset=Favourite.objects.filter(post=attrs['post'],user=attrs['user'])
        if queryset.exists():
            raise serializers.ValidationError('Already added to Favourites')
        return attrs

class FavouriteApiSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favourite
        fields=('content',)
