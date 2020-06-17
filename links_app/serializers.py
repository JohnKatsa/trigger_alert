from rest_framework import serializers
from .models import Link, User

class LinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = ['id', 'url', 'content', 'is_multi_page', 'page_id', 'next_check', 'penalty']