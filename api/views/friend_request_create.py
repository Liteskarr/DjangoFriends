from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import views

import api.models as models
import api.serializers as serializers


@extend_schema(
    tags=['FriendRequests'],
    request=serializers.FriendRequestAction,
    responses={
        status.HTTP_201_CREATED: None,
        status.HTTP_409_CONFLICT: serializers.DefaultError,
    },
    summary='Creates friend request from one user to other.'
)
class FriendRequestCreate(views.APIView):
    def post(self, request: views.Request, *args, **kwargs):
        action = serializers.FriendRequestAction(data=request.data)
        action.is_valid(raise_exception=True)
        initiator = models.User.get_by_id(action.data['initiator_id'])
        subject = models.User.get_by_id(action.data['subject_id'])
        if (req := models.FriendRequest.get_request(initiator, subject)) is not None:
            if req.status == models.Statuses.Friends:
                return views.Response({'details': 'Users already is friends!'}, status=status.HTTP_409_CONFLICT)
            else:
                return views.Response({'details': 'Request already exists!'}, status=status.HTTP_409_CONFLICT)
        req = models.FriendRequest(sender_id=initiator.pk, receiver_id=subject.pk)
        req.save()
        inv = models.FriendRequest.get_request(subject, initiator)
        if inv is not None:
            req.status = models.Statuses.Friends
            inv.status = models.Statuses.Friends
            req.save()
            inv.save()
        return views.Response(status=status.HTTP_201_CREATED)
