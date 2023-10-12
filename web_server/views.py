from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ArticleSerializer
from django.shortcuts import get_object_or_404
from .models import Article
from rest_framework.permissions import IsAuthenticated, AllowAny
import io
import json
import grpc
import gRPS.client
import gRPS.grpc_server_pb2
import gRPS.grpc_server_pb2_grpc
from gRPS.client import stub
from gRPS import grpc_server_pb2
from .forms import UploadFileForm

# Create your views here.
# Получение списка статей из БД
@permission_classes ([AllowAny])
@api_view(['GET'])
def get_list(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

# Получение определенного файла
@api_view(['GET'])
@permission_classes ([IsAuthenticated])
def get_file(request, pk):
    article = get_object_or_404(Article, pk=pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)

# Добавление статьи, названия полей не изменять!
@permission_classes ([IsAuthenticated])
@api_view(['POST'])
def add_article(request):
    mbuffer = request.FILES['article']
    fileArticle = (mbuffer.file).read()
    status_article = stub.AddFile(grpc_server_pb2.FileRequest(bucketName = request.POST['bucketName_article'], title = request.POST['title_article'], content = fileArticle.decode('latin-1'), contentType = 'application/pdf'))
    url_article = stub.GetFile(grpc_server_pb2.FileName(bucketName = request.data['bucketName_article'], title = request.data['title_article'])).content
    mbuffer = request.FILES['permission']
    filePermission = (mbuffer.file).read()
    status_permission = stub.AddFile(grpc_server_pb2.FileRequest(bucketName = request.POST['bucketName_permission'], title = request.POST['title_permission'], content = filePermission.decode('latin-1'), contentType = 'application/pdf'))
    url_permission = stub.GetFile(grpc_server_pb2.FileName(bucketName = request.data['bucketName_permission'], title = request.data['title_permission'])).content
    data = {
        "name_article" : request.data['name_article'],
        "author" : request.user.id,
        "year_of_publication" : request.data['year_of_publication'],
        "url_article" : url_article,
        "url_permission" : url_permission
    }
    serializer = ArticleSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
    return Response({"status_article":status_article.status,"status_permission":status_permission.status,"status":serializer.error_messages})

# Изменение статьи, названия полей не изменять!
@permission_classes ([IsAuthenticated])
@api_view(['PUT'])
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.FILES:
        if request.FILES['article'] and request.POST['bucketName_article'] and request.POST['title_article']:
            myData = request.FILES['article']
            file = (myData.file).read()
            status = stub.EditFile(grpc_server_pb2.FileRequest(bucketName = request.POST['bucketName_article'], title = request.POST['title_article'], content = file.decode('latin-1'), contentType = 'application/pdf'))
            request.data['url_article'] = stub.GetFile(grpc_server_pb2.FileName(bucketName = request.data['bucketName_article'], title = request.data['title_article'])).content
            print(status.status)
        if request.FILES['permission'] and request.POST['bucketName_permission'] and request.POST['title_permission']:
            myData = request.FILES['permission']
            file = (myData.file).read()
            status = stub.EditFile(grpc_server_pb2.FileRequest(bucketName = request.POST['bucketName_permission'], title = request.POST['title_permission'], content = file.decode('latin-1'), contentType = 'application/pdf'))
            article.url_permission = stub.GetFile(grpc_server_pb2.FileName(bucketName = request.data['bucketName_permission'], title = request.data['title_permission'])).content
            print(status.status)
        
    print(request.data)
    serializer = ArticleSerializer(article, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

# Удаление определенной статьи
@permission_classes ([IsAuthenticated])
@api_view(['POST'])
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    status = stub.DeleteFile(grpc_server_pb2.FileName(bucketName = request.data['bucketName'], title = request.data['title']))
    return Response(status.status)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_author_files(request):
    articles = Article.objects.filter(author = request.user.id)
    serializer = ArticleSerializer(articles, many = True)
    return Response(serializer.data)
