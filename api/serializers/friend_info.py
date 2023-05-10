from rest_framework import serializers


class FriendsInfo(serializers.Serializer):
    friends = serializers.ListSerializer(child=serializers.IntegerField(), allow_empty=True, required=True)
    checked_inbox = serializers.ListSerializer(child=serializers.IntegerField(), allow_empty=True, required=True)
    unchecked_inbox = serializers.ListSerializer(child=serializers.IntegerField(), allow_empty=True, required=True)
    outbox = serializers.ListSerializer(child=serializers.IntegerField(), allow_empty=True, required=True)
