from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'product', 'rating', 'title', 'body', 'verified_purchase', 'moderated', 'created_at')
