from django.contrib.auth.models import User
import json
from rest_framework.test import APITestCase
from django.urls import reverse
from post.models import Post


class PostCreateList(APITestCase):
    url_create = reverse("post:create")
    url_list = reverse("post:list")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "veli"
        self.password = "test1234"
        self.user = User.objects.create_user(username= self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data = {"username": self.username, "password": self.password} )
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)

    def test_add_new_post(self):
        data = {
            'content': 'test 1',
            'title' :'header 1'
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(201, response.status_code)

    def test_add_new_post_unauthorization(self):
        self.client.credentials()
        data = {
            'content': 'test 1',
            'title': 'header 1'
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(401, response.status_code)

    # post list
    def test_posts(self):
        self.test_add_new_post()
        response = self.client.get(self.url_list)
        self.assertTrue(len(json.loads(response.content)["results"]) == Post.objects.all().count())




class PostUpdateDelete(APITestCase):
    login_url = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "veli"
        self.password = "test1234"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="veli2", password=self.password)
        self.post = Post.objects.create(title="header", content="test")
        self.url = reverse("post:update", kwargs={"slug": self.post.slug})
        self.url_detail = reverse("post:detail", kwargs={"slug": self.post.slug})
        self.test_jwt_authentication()

    def test_jwt_authentication(self, username="veli", password="test1234"):
        response = self.client.post(self.login_url, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_post_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)


    def test_post_delete_different_user(self):
        self.test_jwt_authentication("veli2")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)


    def test_post_update(self):
        data = {
            'content':  'test',
            'title': 'test header'
        }

        response = self.client.put(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Post.objects.get(id=self.post.id).content == data["content"])



    def test_post_update_different_user(self):
        self.test_jwt_authentication("veli2")
        data = {
            'content':  'test',
            'title': 'test header'
        }

        response = self.client.put(self.url, data)
        self.assertEqual(403, response.status_code)



    def test_unauthorization(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)