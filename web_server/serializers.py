from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class ArticleDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        depth = 1
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['pk', 'name_article', 'author', 'year_of_publication', 'url_article', 'url_permission']
