from django.contrib.auth import authenticate
from django.shortcuts import render
import random
from django.conf import settings
from django.views.decorators.vary import vary_on_headers
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Newsfeed, CustomUser


# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    @classmethod
    def get_token(cls, user: CustomUser):
        token = super().get_token(CustomUser)
        token['raw'] = "development"
        token['user_id'] = user.id
        return token


@api_view(['POST'])
def login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if username is None or password is None:
        return Response({"message": "username or password is missing"}, status=status.HTTP_400_BAD_REQUEST)
    if user is not None:
        token = MyTokenObtainPairSerializer.get_token(user)
        access_token = token.access_token
        context = {
            'message': 'successfully logged in',
            'data': {
                'user_id': user.id,
                'username': user.username,
                'access_token': str(access_token),
                'refresh_token': str(token),
            }
        }
        return Response(context, status=status.HTTP_200_OK, content_type='application/json')
    else:
        context = {
            'message': 'Invalid username or password',
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


@api_view(['GET'])
@authentication_classes([JWTTokenUserAuthentication])
@permission_classes([IsAuthenticated])
@cache_page(settings.CACHE_TTL)
@vary_on_headers('Authorization', )
def list_newsfeed(request):
    all_newsfeed = Newsfeed.objects.filter(user_id=request.user.id)
    data = []
    for item in all_newsfeed:
        temp = {
            'news_id': item.id,
            'user_id': item.user_id,
            'news': item.news
        }
        data.append(temp)
    context = {
        'test': random.randint(100, 999),
        'news': data
    }
    return Response(context, status=status.HTTP_200_OK)
