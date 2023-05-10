from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework import views

import api.models as models
import api.serializers as serializers


@extend_schema(
    tags=['FriendRequests'],
    request=serializers.FriendRequestAction,
    parameters=[
        OpenApiParameter(
            name='id',
            type=int,
            location=OpenApiParameter.PATH,
            description='Checked user\'s ID'
        )
    ],
    responses={
        status.HTTP_200_OK: serializers.FriendsInfo,
        status.HTTP_404_NOT_FOUND: serializers.DefaultError,
    },
    summary='Returns info about all user\'s relations.'
)
class FriendInfo(views.APIView):
    def get(self, request: views.Request, *args, pk: int, **kwargs):
        user = models.User.get_by_id(pk)
        if user is None:
            return views.Response({'details': 'User with this ID does not exists!'}, status=status.HTTP_404_NOT_FOUND)
        friends = list(
            models.FriendRequest.objects
            .filter(sender_id=user.pk, status=models.Statuses.Friends)
            .values_list('receiver_id', flat=True)
            .distinct()
        )
        unchecked_inbox = list(
            models.FriendRequest.objects
            .filter(receiver=user, status=models.Statuses.Unchecked)
            .values_list('sender', flat=True)
        )
        checked_inbox = list(
            models.FriendRequest.objects
            .filter(receiver=user, status=models.Statuses.Checked)
            .values_list('sender', flat=True)
        )
        outbox = list(
            models.FriendRequest.objects
            .filter(sender=user)
            .exclude(status=models.Statuses.Friends)
            .values_list('receiver', flat=True)
        )
        return views.Response({
            'friends': friends,
            'unchecked_inbox': unchecked_inbox,
            'checked_inbox': checked_inbox,
            'outbox': outbox
        }, status=status.HTTP_200_OK)
