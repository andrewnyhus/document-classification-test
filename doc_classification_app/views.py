from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import json


def index(request):
    return render(request, 'home.html', {})


@api_view(["POST"])
@permission_classes((AllowAny, ))
def get_prediction(request):
    words = request.data['words'].split(" ")
    print("words: ", words)

    return HttpResponse("Here are the similar documents")
