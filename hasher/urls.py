from django.urls import path, include

from .views import shortenedUrlOperation , originalUrlOperation

urlpatterns = [
    path('urlshortener', shortenedUrlOperation),
    path('<urlId>', originalUrlOperation),
    
]