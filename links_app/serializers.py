from rest_framework import serializers
from models import Link, User

class LinkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Link
        fields = ['url', 'is_multi_page', 'page_id']