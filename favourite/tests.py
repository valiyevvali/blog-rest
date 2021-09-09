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





class FavouriteUpdateDelete(APITestCase):
    login_url = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "veli"
        self.password = "test1234"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="veli2", password=self.password)
        self.post = Post.objects.create(title="header", content="test content")
        self.favourite = Favourite.objects.create(content="test", post=self.post, user=self.user)
        self.url = reverse("favourite:update-delete", kwargs={"pk": self.favourite.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self, username="veli", password="test1234"):
        response = self.client.post(self.login_url, data = {"username": username, "password": password} )
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)

    # delete fav
    def test_fav_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
    # check anyone can't delete fav
    def test_fav_delete_different_user(self):
        self.test_jwt_authentication("veli2")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

     #update
    def test_fav_update(self):
        data = {
            "content": "içerik 123",
        }

        response = self.client.put(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Favourite.objects.get(id=self.favourite.id).content == data["content"])


    def test_fav_update_different_user(self):
        self.test_jwt_authentication("veli2")
        data = {
            "content": "isdfsdf",
            "user": self.user2.id
        }

        response = self.client.put(self.url, data)
        self.assertTrue(403, response.status_code)

    # login required
    def test_unautherazation(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)