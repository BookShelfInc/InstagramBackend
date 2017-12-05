from rest_framework import serializers

from auth_app.serializers import UserSerializer
from .models import Photo, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = (
            'comment',
            'author',
            'photo'
        )

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Like
        fields = (
            'photo',
            'user'
        )

class PhotoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    class Meta:
        model = Photo
        fields = (
            'id',
            'photo_path',
            'photo_small_path',
            'description',
            'publish_date',
            'user_id',
            'comments',
            'likes'
        )

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'comment',
            'author',
            'photo'
        )

class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'photo',
            'user'
        )