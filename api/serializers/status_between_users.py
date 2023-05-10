from rest_framework import serializers


class StatusBetweenUsers(serializers.Serializer):
    """
    Serializer of status between two users.
    """
    status = serializers.CharField()
