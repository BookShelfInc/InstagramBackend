from rest_framework import serializers

from .models import User, Follows

from photo_app.serializers import PhotoAvatarSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

class FollowsSerializer(serializers.ModelSerializer):
    target_user = UserSerializer()
    following = UserSerializer(many=True)
    class Meta:
        model = Follows
        fields = (
            'target_user',
            'following'
        )

class UserPhotoSerializer(serializers.ModelSerializer):
    photo = PhotoAvatarSerializer
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'photo'
        )