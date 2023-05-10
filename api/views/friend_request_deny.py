from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import views

import api.models as models
import api.serializers as serializers


@extend_schema(
    tags=['FriendRequests'],
    request=serializers.FriendRequestAction,
    responses={
        status.HTTP_200_OK: serializers.User,
        status.HTTP_404_NOT_FOUND: serializers.DefaultError,
    },
)
class FriendRequestDeny(views.APIView):
    def put(self, request: views.Request, *args, initiator_id: int, subject_id: int, **kwargs):
        initiator = models.User.get_by_id(initiator_id)
        subject = models.User.get_by_id(subject_id)
        if initiator is None or subject is None:
            return views.Response({'details': 'User with this ID does not exists!'}, status=status.HTTP_404_NOT_FOUND)
        req = models.FriendRequest.get_request(subject, initiator)
        if req is None:
            return views.Response({'details': 'Request for denying does not exists!'}, status=status.HTTP_404_NOT_FOUND)
        req.status = models.Statuses.Checked
        req.save()
        return views.Response(status=status.HTTP_200_OK)
