from django.shortcuts import render
from rest_framework import viewsets
from .models import Link
from links_app.serializers import LinkSerializer

from datetime import datetime
import json

class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def post(self, request):
        print("ok")

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
            link.save()
        except:
            super().perform_create(serializer)