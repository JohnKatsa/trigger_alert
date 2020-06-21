from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from .models import Link, User as Suser
from links_app.serializers import LinkSerializer, UserSerializer, UserLoginSerializer, UserRegistrationSerializer
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponse
from rest_framework.decorators import api_view

from datetime import datetime
import json

@api_view(['POST'])
def validateUsername(request):
    username = request.data['username']
    if Suser.objects.filter(username=username).count() > 0:
        return HttpResponse(False)
    return HttpResponse(True)

class LinkProcessorViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer

    def get_queryset(self):
        shard = int(self.request.GET['page_checker_id'])
        total_shards = int(self.request.GET['page_checkers'])

        links = Link.objects.filter(next_check__lte=datetime.now().timestamp())

        return [link for link in links if (link.id % total_shards == shard)]

    def perform_create(self, serializer):
        try: 
            link = Link.objects.get(url=serializer.validated_data.get('url'))
            link.content = serializer.data.get('content')
            link.next_check = serializer.data.get('next_check')
            link.penalty = serializer.data.get('penalty')
            link.version = serializer.data.get('version')
            link.save()
        except:
            super().perform_create(serializer)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Suser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        for item in request.POST.items():
            print(item)
        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid(raise_exception=True))
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return request.user in obj.users

class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer

    def get_queryset(self):
        uId = int(self.request.GET['u_id'])
        user = Suser.objects.get(id=uId)
        return [link for link in Link.objects.all() if user in link.users.all()]

    def perform_create(self, serializer):
        u_id = self.request.GET['u_id']
        try: 
            link = Link.objects.get(url=serializer.validated_data.get('url'))
        except:
            link = Link(url=serializer.data.get('url'),
                        is_multi_page=serializer.data.get('is_multi_page'),
                        page_id=serializer.data.get('page_id'))
            link.save()
            user = Suser.objects.get(id=u_id)
            link.users.add(user)
            link.save()
            