from django.shortcuts import render
from rest_framework import viewsets

from models import Link
from links_app.serializers import LinkSerializer

class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)