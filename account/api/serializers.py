from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'note', 'twitter']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        profile_serializer = ProfileSerializer(instance=instance.profile, data=profile)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        return super(UserSerializer, self).update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

class RegisterUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['id','username','password','confirm_password']

    def validate(self,attrs):
        validate_password(attrs['password'])
        if attrs['confirm_password']!=attrs['password']:
            raise serializers.ValidationError('passwords must be same')
        return attrs

    def create(self, validated_data):
        username=validated_data.get('username')
        password=validated_data.get('password')
        user=User(username=username)
        user.set_password(password)
        user.save()
        return user




