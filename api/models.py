from enum import Enum, auto

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=16, unique=True, null=False)

    @staticmethod
    def get_by_id(user_id: int):
        return User.objects.filter(pk=user_id).only('pk', 'username').first()

    def __repr__(self):
        return f'<{self.pk}>:{self.username}'

    def __str__(self):
        return repr(self)


class UsersRelation(Enum):
    Nothing = auto()
    Incoming = auto()
    Outcoming = auto()
    Friends = auto()


class Statuses(models.TextChoices):
    Unchecked = 'U'
    Checked = 'C'
    Friends = 'F'


class FriendRequest(models.Model):
    sender = models.ForeignKey('User', unique=False, on_delete=models.CASCADE, related_name='sender_id')
    receiver = models.ForeignKey('User', unique=False, on_delete=models.CASCADE, related_name='receiver_id')
    status = models.CharField(default=Statuses.Unchecked, max_length=1, null=False)

    @staticmethod
    def make_request(sender: User, receiver: User) -> "FriendRequest":
        if (rq := FriendRequest.get_request(sender, receiver)) is None:
            rq = FriendRequest(sender_id=sender.pk, receiver_id=receiver.pk)
            rq.save()
        return rq

    @staticmethod
    def make_friends(x: User, y: User):
        req = FriendRequest.make_request(x, y)
        inv = FriendRequest.make_request(y, x)
        req.status = Statuses.Friends
        inv.status = Statuses.Friends
        req.save()
        inv.save()

    @staticmethod
    def get_request(sender: User, receiver: User) -> "FriendRequest":
        return FriendRequest.objects.filter(sender=sender, receiver=receiver).first()

    @staticmethod
    def is_friends(x: User, y: User) -> bool:
        return FriendRequest.get_request(x, y) is not None and FriendRequest.get_request(y, x) is not None

    @staticmethod
    def get_relation_status(x: User, y: User) -> UsersRelation:
        if x.pk == y.pk:
            return UsersRelation.Nothing
        req = FriendRequest.get_request(x, y)
        inv = FriendRequest.get_request(y, x)
        if req is None and inv is None:
            return UsersRelation.Nothing
        elif req is None and inv is not None:
            return UsersRelation.Outcoming
        elif req is not None and inv is None:
            return UsersRelation.Incoming
        else:
            return UsersRelation.Friends

    def __repr__(self):
        return f'({self.status}) {self.sender} --> {self.receiver}'

    def __str__(self):
        return repr(self)
