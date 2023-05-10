from rest_framework import serializers, status

import api.models as models


class FriendRequestAction(serializers.Serializer):
    """
    Serializer of friend reqeust action.
    """
    initiator_id = serializers.IntegerField(required=True, help_text='Initiator of action.')
    subject_id = serializers.IntegerField(required=True, help_text='Subject of action.')

    def validate(self, data: dict):
        """
        Checks what users with sent IDs is not same.
        """
        if data['initiator_id'] == data['subject_id']:
            raise serializers.ValidationError('IDs must be not same!')
        return data

    @staticmethod
    def _validate_user_ref(value: int, name: str):
        """
        Validates user's ID field.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError(f'Field "{name}" is not int!')
        if models.User.get_by_id(value) is None:
            raise serializers.ValidationError('No user with this ID!')
        return value

    def validate_initiator_id(self, value: int):
        return self._validate_user_ref(value, 'initiator_id')

    def validate_subject_id(self, value: int):
        return self._validate_user_ref(value, 'subject_id')
