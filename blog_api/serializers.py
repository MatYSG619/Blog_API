from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Article, Comment


class ArticleSerializer(serializers.Serializer):
    """Создание статей"""
    title = serializers.CharField(max_length=150)
    description = serializers.CharField()
    created = serializers.CharField()

    def create(self, validated_data):
        return Article.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Комментарий к статье"""

    class Meta:
        model = Comment
        fields = ['article', 'text', 'level']


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'description', 'created']


class ReplyCommentSerializer(serializers.ModelSerializer):
    """Ответ на комментарий"""

    class Meta:
        model = Comment
        fields = ['article', 'text', 'level', 'parent']


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None, level=0)
        return super().to_representation(data)


class CommentsSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Comment
        list_serializer_class = FilterReviewListSerializer
        fields = ['article', 'text', 'level', 'children']

    def to_representation(self, instance):
        # Очищаем словарь с уровнем комментирования 3 и выше
        representation = super().to_representation(instance)
        if representation['level'] >= 3:
            representation.clear()
        return representation


class ArticleWithCommentsSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True)

    class Meta:
        model = Article
        fields = ['title', 'description', 'created', 'comments']
