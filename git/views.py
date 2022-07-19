from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .models import User
import jwt
import urllib.request
from bs4 import BeautifulSoup
from .serializer import UserSerializer




@api_view(['GET'])
def getGit(request):
    token = request.GET['token']
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user = User.objects.get(id=payload['id'])
    serializer = UserSerializer(user)

    gitName = serializer.data['gitName']

    url = "https://github.com/" + gitName
    html = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html, 'html.parser')

    line = str(soup.find_all(class_="f4 text-normal mb-2"))

    commit = line.split()[4]

    return Response(commit)

@api_view(['POST'])
def signup(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    else:
        return Response("실패")

@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    if not username and not password:
        return Response("부족한 데이터")
    user = authenticate(username=username, password=password)
    if user is not None:
        encode_jwt = jwt.encode({"id": user.pk}, settings.SECRET_KEY, algorithm="HS256")
        response = Response()
        response.data = {"token": encode_jwt}
        return response
    else:
        return Response("부적절한 데이터")


@api_view(['GET'])
def userview(request):
    token = request.GET['token']
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user = User.objects.get(id=payload['id'])
    serializer = UserSerializer(user)
    print(serializer.data)
    return Response(serializer.data)