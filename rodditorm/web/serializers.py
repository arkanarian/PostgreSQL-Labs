from rest_framework import serializers
from web.models import Queries

class ListQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Queries
        fields = ('type', 'topic', 'description', 'query')