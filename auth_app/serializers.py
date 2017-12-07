from rest_framework import serializers

from .models import User, Follows

from photo_app.models import Photo

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

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'id',
            'photo_path',
            'photo_small_path',
        )

class UserPhotoSerializer(serializers.ModelSerializer):
    photo = AvatarSerializer()
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'photo'
        )