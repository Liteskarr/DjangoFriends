from rest_framework import serializers

import api.models as models


class FriendRequestAction(serializers.Serializer):
    initiator_id = serializers.IntegerField(required=True)
    subject_id = serializers.IntegerField(required=True)

    def validate(self, data: dict):
        if data['initiator_id'] == data['subject_id']:
            raise serializers.ValidationError('IDs must be not same!')
        return data

    @staticmethod
    def _validate_user_ref(value: int, name: str):
        if not isinstance(value, int):
            raise serializers.ValidationError(f'Field "{name}" is not int!')
        if models.User.get_by_id(value) is None:
            raise serializers.ValidationError('No user with this ID!')
        return value

    def validate_initiator_id(self, value: int):
        return self._validate_user_ref(value, 'initiator_id')

    def validate_subject_id(self, value: int):
        return self._validate_user_ref(value, 'subject_id')
