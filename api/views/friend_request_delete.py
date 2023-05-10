from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework import views

import api.models as models
import api.serializers as serializers


@extend_schema(
    tags=['FriendRequests'],
    parameters=[
        OpenApiParameter(
            name='initiator_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID of user who created friend request for deletion.'
        ),
        OpenApiParameter(
            name='subject_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID of user who received friend request for deletion.'
        )
    ],
    responses={
        status.HTTP_200_OK: None,
        status.HTTP_404_NOT_FOUND: serializers.DefaultError,
    },
    summary='Deletes sent friend request.'
)
class FriendRequestDelete(views.APIView):
    def delete(self, request: views.Request, *args, initiator_id: int, subject_id: int, **kwargs):
        initiator = models.User.get_by_id(initiator_id)
        subject = models.User.get_by_id(subject_id)
        if initiator is None or subject is None:
            return views.Response({'details': 'User with this ID does not exists!'}, status=status.HTTP_404_NOT_FOUND)
        req = models.FriendRequest.get_request(initiator, subject)
        if req is None:
            return views.Response({'details': 'Request already not exists!'}, status=status.HTTP_404_NOT_FOUND)
        req.delete()
        inv = models.FriendRequest.get_request(subject, initiator)
        if inv is not None:
            inv.status = models.Statuses.Checked
            inv.save()
        return views.Response(status=status.HTTP_200_OK)
