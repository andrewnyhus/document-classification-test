from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('get_similar_documents', views.get_similar_documents),
]