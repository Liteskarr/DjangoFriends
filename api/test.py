from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.views import Response

import api.models as models
import api.views as views

FACTORY = APIRequestFactory()
ANY = ''


class AllUsersTestCase(TestCase):
    N = 16

    def setUp(self):
        self.users = [models.User(username=f'{i}') for i in range(AllUsersTestCase.N)]
        for user in self.users:
            user.save()

    def test(self):
        request = FACTORY.get(ANY, {})
        response: Response = views.AllUsers.as_view()(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(set(map(lambda x: x['pk'], response.data)), set(map(lambda x: x.pk, self.users)))
        self.assertEquals(set(map(lambda x: x['username'], response.data)), set(map(lambda x: x.username, self.users)))


class GetUserTestCase(TestCase):
    N = 16

    def setUp(self):
        self.users = [models.User(username=f'{i}') for i in range(AllUsersTestCase.N)]
        for user in self.users:
            user.save()

    def test(self):
        view = views.GetUser.as_view()
        for user in self.users:
            request = FACTORY.get(ANY)
            response: Response = view(request, pk=user.pk)
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            self.assertEquals(response.data['pk'], user.pk)
            self.assertEquals(response.data['username'], user.username)


class RegisterUserTestCase(TestCase):
    def test(self):
        username = 'BeautifulUser'
        request = FACTORY.post(ANY, {'username': username})
        response: Response = views.RegisterUser.as_view()(request)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        user = models.User.get_by_id(response.data['pk'])
        self.assertIsNotNone(user)
        self.assertEquals(username, user.username)


class FriendRequestCreateTestCase(TestCase):
    def setUp(self):
        self.user_x = models.User(username='UserX')
        self.user_y = models.User(username='UserY')
        self.user_x.save()
        self.user_y.save()

    def test_201(self):
        request = FACTORY.post(ANY, {
            'initiator_id': self.user_x.pk,
            'subject_id': self.user_y.pk
        })
        response: Response = views.FriendRequestCreate.as_view()(request)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(
            models.FriendRequest.get_relation_status(self.user_x, self.user_y),
            models.UsersRelation.RequestTo
        )
        self.assertEquals(
            models.FriendRequest.get_relation_status(self.user_y, self.user_x),
            models.UsersRelation.RequestFrom
        )
        req = models.FriendRequest.get_request(self.user_x, self.user_y)
        self.assertIsNotNone(req)

    def test_409(self):
        request = FACTORY.post(ANY, {
            'initiator_id': self.user_x.pk,
            'subject_id': self.user_y.pk
        })
        response: Response = views.FriendRequestCreate.as_view()(request)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        response: Response = views.FriendRequestCreate.as_view()(request)
        self.assertEquals(response.status_code, status.HTTP_409_CONFLICT)


class FriendRequestDeleteTestCase(TestCase):
    def setUp(self):
        self.user_x = models.User(username='UserX')
        self.user_y = models.User(username='UserY')
        self.user_x.save()
        self.user_y.save()
        models.FriendRequest.make_request(self.user_x, self.user_y)

    def test_200(self):
        request = FACTORY.delete(ANY)
        response: Response = views.FriendRequestDelete.as_view()(request,
                                                                 initiator_id=self.user_x.pk,
                                                                 subject_id=self.user_y.pk)
        self.assertEquals(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIsNone(models.FriendRequest.get_request(self.user_x, self.user_y))

    def test_404_user(self):
        request = FACTORY.delete(ANY)
        response: Response = views.FriendRequestDelete.as_view()(request,
                                                                 initiator_id=self.user_x.pk,
                                                                 subject_id=32)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND, response.data)

    def test_404_request(self):
        request = FACTORY.delete(ANY)
        response: Response = views.FriendRequestDelete.as_view()(request,
                                                                 initiator_id=self.user_y.pk,
                                                                 subject_id=self.user_x.pk)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND, response.data)


class FriendRequestApplyTestCase(TestCase):
    def setUp(self):
        self.user_x = models.User(username='UserX')
        self.user_y = models.User(username='UserY')
        self.user_x.save()
        self.user_y.save()
        models.FriendRequest.make_request(self.user_x, self.user_y)

    def test_200(self):
        request = FACTORY.put(ANY, {})
        response: Response = views.FriendRequestApply.as_view()(request,
                                                                initiator_id=self.user_y.pk,
                                                                subject_id=self.user_x.pk)
        self.assertEquals(response.status_code, status.HTTP_200_OK, response.data)
        self.assertTrue(models.FriendRequest.is_friends(self.user_x, self.user_y))


class FriendRequestDenyTestCase(TestCase):
    def setUp(self):
        self.user_x = models.User(username='UserX')
        self.user_y = models.User(username='UserY')
        self.user_x.save()
        self.user_y.save()
        models.FriendRequest.make_request(self.user_x, self.user_y)

    def test_200(self):
        request = FACTORY.put(ANY, {})
        response: Response = views.FriendRequestDeny.as_view()(request,
                                                               initiator_id=self.user_y.pk,
                                                               subject_id=self.user_x.pk)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertFalse(models.FriendRequest.is_friends(self.user_x, self.user_y))


class FriendInfoTestCase(TestCase):
    N = 5

    def setUp(self):
        self.users = [models.User(username=f'{i + 1}') for i in range(FriendInfoTestCase.N)]
        for user in self.users:
            user.save()
        models.FriendRequest.make_friends(self.users[0], self.users[1])
        models.FriendRequest.make_request(self.users[0], self.users[2])
        models.FriendRequest.make_request(self.users[3], self.users[0])
        r = models.FriendRequest.make_request(self.users[4], self.users[0])
        r.status = models.Statuses.Checked
        r.save()

    def test_200(self):
        request = FACTORY.get(ANY, {})
        response: Response = views.FriendInfo.as_view()(request, pk=self.users[0].pk)
        self.assertEquals([self.users[1].pk], response.data['friends'])
        self.assertEquals([self.users[3].pk], response.data['unchecked_inbox'])
        self.assertEquals([self.users[4].pk], response.data['checked_inbox'])
        self.assertEquals([self.users[2].pk], response.data['outbox'])


class FriendStatusTestCase(TestCase):
    N = 5

    def setUp(self):
        self.users = [models.User(username=f'{i + 1}') for i in range(FriendStatusTestCase.N)]
        for user in self.users:
            user.save()
        models.FriendRequest.make_friends(self.users[0], self.users[1])
        models.FriendRequest.make_request(self.users[0], self.users[2])
        models.FriendRequest.make_request(self.users[3], self.users[0])

    def test_200(self):
        request = FACTORY.get(ANY, {})
        view = views.FriendStatus.as_view()
        target = self.users[0]
        answers = [
            models.UsersRelation.Friends,
            models.UsersRelation.RequestTo,
            models.UsersRelation.RequestFrom,
            models.UsersRelation.Nothing
        ]
        for i, user in enumerate(self.users[1::]):
            response: Response = view(request, initiator_id=target.pk, subject_id=user.pk)
            self.assertEquals(response.data['status'], answers[i])


class FriendRequestBreakTestCase(TestCase):
    def setUp(self):
        self.user_x = models.User(username='UserX')
        self.user_y = models.User(username='UserY')
        self.user_x.save()
        self.user_y.save()
        models.FriendRequest.make_friends(self.user_x, self.user_y)

    def test_200(self):
        request = FACTORY.delete(ANY, {})
        response: Response = views.FriendRequestDelete.as_view()(request,
                                                                 initiator_id=self.user_x.pk,
                                                                 subject_id=self.user_y.pk)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(models.FriendRequest.get_request(self.user_x, self.user_y))
        self.assertEquals(models.FriendRequest.get_request(self.user_y, self.user_x).status,
                          models.Statuses.Checked)
