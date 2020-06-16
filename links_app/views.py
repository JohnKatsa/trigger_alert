from django.shortcuts import render
from rest_framework import viewsets
from .models import Link
from links_app.serializers import LinkSerializer

from datetime import datetime

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
        print(serializer.data)
        print("ok", serializer, Link.objects.filter(id=self.request.GET.get('id')))
        input()
        if(len(Link.objects.filter(id=self.request.GET.get('id'))) == 0):
            return super().perform_create(serializer)