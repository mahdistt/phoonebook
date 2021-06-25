from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    """
    serializer for phonebook
    """

    class Meta:
        model = models.Entry
        fields = (
            'name',
            'created_at',
            'last_name',
            'phone_number',
            'creator',
        )
