from rest_framework import serializers


class DefaultError(serializers.Serializer):
    details = serializers.CharField()
