from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework import views

import api.models as models
import api.serializers as serializers


@extend_schema(
    tags=['FriendRequests'],
    request=serializers.FriendRequestAction,
    responses={
        status.HTTP_200_OK: None,
        status.HTTP_404_NOT_FOUND: serializers.DefaultError,
    },
    parameters=[
        OpenApiParameter(
            name='initiator_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='Initiator of breaking.',
        ),
        OpenApiParameter(
            name='subject_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='Subject of breaking.'
        )
    ],
    summary='Breaks friend relations between two users. '
            'Saves friend request from subject to initiator with checked status.'
)
class FriendBreak(views.APIView):
    def delete(self, request: views.Request, *args, initiator_id: int, subject_id: int, **kwargs):
        initiator = models.User.get_by_id(initiator_id)
        subject = models.User.get_by_id(subject_id)
        if initiator is None or subject is None:
            return views.Response({'details': 'User with this ID does not exists!'}, status=status.HTTP_404_NOT_FOUND)
        req = models.FriendRequest.get_request(initiator, subject)
        if req is None or req.status != models.Statuses.Friends:
            return views.Response({'details': 'Friend requests between these users does not exists!'},
                                  status=status.HTTP_404_NOT_FOUND)
        req.delete()
        inv = models.FriendRequest.get_request(subject, initiator)
        inv.status = models.Statuses.Checked
        return views.Response(status=200)
