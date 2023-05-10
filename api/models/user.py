from django.db import models


class User(models.Model):
    """
    Model of user.
    """
    username = models.CharField(max_length=16, unique=True, null=False)

    @staticmethod
    def get_by_id(user_id: int) -> "User":
        """
        Returns user by ID if exists else None.
        """
        return User.objects.filter(pk=user_id).only('pk', 'username').first()

    def __repr__(self):
        return f'<{self.pk}>:{self.username}'

    def __str__(self):
        return repr(self)
