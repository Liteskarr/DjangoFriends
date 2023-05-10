from rest_framework import serializers

import api.models as models


class User(serializers.ModelSerializer):
    """
    Serializer of user.
    """
    MIN_USERNAME_LENGTH = 6
    MAX_USERNAME_LENGTH = 16

    class Meta:
        model = models.User
        fields = ('pk', 'username',)

    def validate_username(self, value: str):
        if not isinstance(value, str):
            raise serializers.ValidationError('Field "username" is not str!')
        if not (User.MIN_USERNAME_LENGTH <= len(value) <= User.MAX_USERNAME_LENGTH):
            raise serializers.ValidationError(
                f'Field "username" length must be between {User.MIN_USERNAME_LENGTH} '
                f'and {User.MAX_USERNAME_LENGTH} symbols!'
            )
        return value
