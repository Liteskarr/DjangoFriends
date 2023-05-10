from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

import api.views

urlpatterns = [
    path('schema/', api.views.SchemaApiView.as_view(), name='schema'),
    path('users/all/', api.views.AllUsers.as_view()),
    path('users/get/<int:pk>/', api.views.GetUser.as_view()),
    path('users/register/', api.views.RegisterUser.as_view()),
    path('friends/info/<int:pk>/', api.views.FriendInfo.as_view()),
    path('friends/request/create/', api.views.FriendRequestCreate.as_view()),
    path('friends/status/<int:initiator_id>/<int:subject_id>', api.views.FriendStatus.as_view()),
    path('friends/break/<int:initiator_id>/<int:subject_id>', api.views.FriendBreak.as_view()),
    path('friends/request/deny/<int:initiator_id>/<int:subject_id>', api.views.FriendRequestDeny.as_view()),
    path('friends/request/apply/<int:initiator_id>/<int:subject_id>', api.views.FriendRequestApply.as_view()),
    path('friends/request/delete/<int:initiator_id>/<int:subject_id>', api.views.FriendRequestDelete.as_view()),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
