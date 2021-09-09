import json
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse

from favourite.models import Favourite
from post.models import Post


class FavouriteCreateList(APITestCase):
    url=reverse("favourite:list-create")
    url_login=reverse("token_obtain_pair")

    def setUp(self):
        self.username='veli'
        self.password='veli1234'
        self.user=User.objects.create_user(username=self.username,password=self.password)
        self.post=Post.objects.create(title='test',content='test')

    def test_jwt_authentication(self):
        data={
            'username':'veli',
            'password':'veli1234'
        }
        response=self.client.post(self.url_login,data)
        self.assertEqual(200,response.status_code)
        self.assertTrue('access' in json.loads(response.content))
        token=response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_add_favourite(self):
        self.test_jwt_authentication()
        data={
            'content':'for test',
            'post':self.post.id,
            'user':self.user.id
        }
        response=self.client.post(self.url,data)
        self.assertEqual(201,response.status_code)

    def test_user_favs(self):
        self.test_add_favourite()
        response=self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)["results"])== Favourite.objects.filter(user=self.user).count())
