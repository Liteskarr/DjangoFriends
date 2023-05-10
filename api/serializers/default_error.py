from rest_framework import serializers


class DefaultError(serializers.Serializer):
    """
    Serializer of default error.
    """
    details = serializers.CharField()
