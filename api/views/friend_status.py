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
            name='initiator_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='Initiator of status checking.'
        ),
        OpenApiParameter(
            name='subject_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='Subject of status checking.'
        )
    ],
    responses={
        status.HTTP_200_OK: serializers.StatusBetweenUsers,
        status.HTTP_404_NOT_FOUND: serializers.DefaultError,
    },
    summary='Returns status of relation between two users.'
)
class FriendStatus(views.APIView):
    def get(self, request: views.Request, *args, initiator_id: int, subject_id: int, **kwargs):
        initiator = models.User.get_by_id(initiator_id)
        subject = models.User.get_by_id(subject_id)
        if initiator is None or subject is None:
            return views.Response({'details': 'User with this ID does not exists!'}, status=status.HTTP_404_NOT_FOUND)
        return views.Response(
            {'status': models.FriendRequest.get_relation_status(initiator, subject)},
            status=status.HTTP_200_OK
        )
