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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    remember_me = serializers.BooleanField()
