from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    name_article = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    year_of_publication = models.CharField(max_length=10, default=datetime.date.today().strftime("%Y-%m-%d"))
    url_article = models.CharField(max_length=60)
    url_permission = models.CharField(max_length=60)