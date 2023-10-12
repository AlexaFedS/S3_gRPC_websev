"""
URL configuration for file_transfer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from web_server import views as files_views
from rest_framework import routers

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'articles', files_views.get_list, name='get_articles'), # просто список файлов
    path(r'add_article', files_views.add_article, name='add_article'), 
        #добавление файлов, на вход: bucketName_article = articles !всегда!
                                    #title_article - название файла, !вводить исключительно английскими буквами/цифрами и в конце всегда добавлять '.pdf'!
                                    #article - сам пдф файл статьи
                                    #bucketName_permission = permissions !всегда!
                                    #title_permission - название файла, тоже !вводить исключительно английскими буквами/цифрами и в конце всегда добавлять '.pdf'!
                                    #permission - сам пдф файл разрешения
                                    #name_article - название статьи
                                    #author - автор статьи (указывается id пользователя, отправляющего реквест на добавление файла, автоматически)
                                    #year_of_publication - год публикации
    
    path(r'articles/<int:pk>', files_views.get_file, name='get_article'), # вернет данные определенной статьи
    path(r'articles/<int:pk>/edit', files_views.edit_article, name='edit_article'), # редактирование определенного файла, !поля url_... не редактируются!
                                    # на вход: если файл не прикрепляется - все поля как в модели
                                    # если файл прикрепляется, то прикреплять оба файла и вводить поля:
                                    # bucketName_article = articles !всегда!
                                    # title_article - название файла, !вводить исключительно английскими буквами/цифрами и в конце всегда добавлять '.pdf'!
                                    # article - сам пдф файл статьи
                                    # bucketName_permission = permissions !всегда!
                                    # title_permission - название файла, тоже !вводить исключительно английскими буквами/цифрами и в конце всегда добавлять '.pdf'!
                                    # permission - сам пдф файл разрешения
    path(r'articles/<int:pk>/delete', files_views.delete_article, name='remove_article'), # удаление определенного файла
    path(r'myarticles', files_views.get_author_files, name="author's_articles"), # вывод статей определенного автора

    # auth/users - регистрация
    # auth/token/login - вход и получение токена
    # auth/token/logout - выход из системы
    path(r'auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]
