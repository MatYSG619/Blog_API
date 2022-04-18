from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from django.shortcuts import get_object_or_404

from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentSerializer, ReplyCommentSerializer, \
    ArticleWithCommentsSerializer


class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({"articles": serializer.data})

    def post(self, request):
        article = request.data.get('article')

        serializer = ArticleSerializer(data=article)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": "Article '{}' created successfully".format(article_saved.title)})


class ArticleDetail(APIView):
    def get(self, request, pk):
        article = Article.objects.filter(pk=pk)
        serializer = ArticleDetailSerializer(article, many=True)
        return Response({"article": serializer.data})

    def post(self, request, pk):
        comment = request.data.get('comment')
        comment.update({"article": pk, "level": "0"})
        serializer = CommentSerializer(data=comment)
        if serializer.is_valid(raise_exception=True):
            comment_saved = serializer.save()
        return Response({"success": "Comment '{}' create".format(comment_saved.id)})


class CommentDetail(APIView):
    def get(self, request, comment_id):
        comment = Comment.objects.filter(pk=comment_id)
        serializer = ReplyCommentSerializer(comment, many=True)
        return Response({"comment": serializer.data})

    def post(self, request, comment_id):
        # Данные о комментарии, на который оставляется ответ
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=comment_id)
        # Увеличение уровня комментария
        level = int(comment.level) + 1
        # Формирование формы
        comment_form = request.data.get('comment')
        comment_form.update({"article": int(comment.article.pk), "level": level, "parent": comment_id})
        serializer = ReplyCommentSerializer(data=comment_form)
        if serializer.is_valid(raise_exception=True):
            comment_saved = serializer.save()
        return Response({"success": "Reply '{}' on the comment '{}' create".format(comment_saved.id, comment.id)})


class ArticleWithComments(APIView):
    def get(self, request, pk):
        article = Article.objects.filter(pk=pk)
        serializer = ArticleWithCommentsSerializer(article, many=True)
        return Response({"article": serializer.data})
