from django.db import models

from api.models.statuses import Statuses
from api.models.user import User
from api.models.user_relation import UsersRelation


class FriendRequest(models.Model):
    """
    Model of friend request.
    """
    sender = models.ForeignKey('User', unique=False, on_delete=models.CASCADE, related_name='sender_id')
    receiver = models.ForeignKey('User', unique=False, on_delete=models.CASCADE, related_name='receiver_id')
    status = models.CharField(default=Statuses.Unchecked, max_length=1, null=False)

    @staticmethod
    def make_request(sender: User, receiver: User) -> "FriendRequest":
        """
        Makes request from sender to receiver if it is not exists.
        """
        if (rq := FriendRequest.get_request(sender, receiver)) is None:
            rq = FriendRequest(sender_id=sender.pk, receiver_id=receiver.pk)
            rq.save()
        return rq

    @staticmethod
    def make_friends(x: User, y: User):
        """
        Makes friend between two users if it is not exists.
        """
        req = FriendRequest.make_request(x, y)
        inv = FriendRequest.make_request(y, x)
        req.status = Statuses.Friends
        inv.status = Statuses.Friends
        req.save()
        inv.save()

    @staticmethod
    def get_request(sender: User, receiver: User) -> "FriendRequest":
        """
        Returns request by sender and receiver if it exists else None.
        """
        return FriendRequest.objects.filter(sender=sender, receiver=receiver).first()

    @staticmethod
    def is_friends(x: User, y: User) -> bool:
        """
        Returns True if two users is friends else False.
        """
        req = FriendRequest.get_request(x, y)
        return req is not None and req.status == Statuses.Friends

    @staticmethod
    def get_relation_status(x: User, y: User) -> UsersRelation:
        """
        Returns relations status between two users.
        """
        if x.pk == y.pk:
            return UsersRelation.SameUser
        req = FriendRequest.get_request(x, y)
        inv = FriendRequest.get_request(y, x)
        if req is None and inv is None:
            return UsersRelation.Nothing
        elif req is None and inv is not None:
            return UsersRelation.RequestFrom
        elif req is not None and inv is None:
            return UsersRelation.RequestTo
        else:
            return UsersRelation.Friends

    def __repr__(self):
        return f'({self.status}) {self.sender} --> {self.receiver}'

    def __str__(self):
        return repr(self)
