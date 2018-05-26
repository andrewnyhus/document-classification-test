from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'home.html', {})

def get_similar_documents(request):
    return HttpResponse("Here are the similar documents")
