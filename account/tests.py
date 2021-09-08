from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse

# Create your tests here.
from rest_framework.utils import json


class UserRegistrationTest(APITestCase):
    url=reverse("account:register")
    url_login=reverse("token_obtain_pair")

    #test for using right data set
    def test_user_registration(self):
        data={
            'username':'veli',
            'password':'veli1234',
            'confirm_password': 'veli1234'
        }

        response=self.client.post(self.url,data)
        self.assertEqual(201,response.status_code)


    def test_user_invalid_password(self):
        # data = {
        #     'username': 'veli',
        #     'password': 'veli123',
        #     'confirm_password': 'veli1234'
        # }
        data = {
            'username': 'veli',
            'password': 'veli1234',
            'confirm_password': 'veli12345'
        }

        response=self.client.post(self.url,data)
        self.assertEqual(400,response.status_code)


    def test_unique_name(self):
        self.test_user_registration()
        # data = {
        #     'username': 'veli',
        #     'password': 'veli1234',
        #     'confirm_password': 'veli1234'
        # }
        data = {
            'username': 'veli1',
            'password': 'veli1234',
            'confirm_password': 'veli12345'
        }

        response=self.client.post(self.url,data)
        self.assertEqual(400,response.status_code)


    # if user logined,can's see this page
    def test_user_authenticated_registration(self):
        self.test_user_registration()
        self.client.login(username='veli',password='veli1234')

        response=self.client.get(self.url)
        self.assertEqual(403,response.status_code)



    def test_user_authenticated_token_registration(self):
        self.test_user_registration()
        data={
            'username':'veli',
            'password':'veli1234'
        }
        print(self.url_login)
        response=self.client.post(self.url_login,data)
        self.assertEqual(200,response.status_code)
        token=response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        response_2=self.client.get(self.url)
        self.assertEqual(403,response_2.status_code)


class UserLogin(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username='veli'
        self.password='veli1234'
        self.user=User.objects.create_user(username=self.username,password=self.password)

    def test_user_token(self):
        response=self.client.post(self.url_login,{'username':'veli','password':'veli1234'})
        self.assertEqual(200,response.status_code)
        self.assertTrue('access' in json.loads(response.content))

    def test_user_invalid_data(self):
        response=self.client.post(self.url_login,{'username':'veli1','password':'veli1234'})
        self.assertEqual(401,response.status_code)

    def test_user_empty_data(self):
        response=self.client.post(self.url_login,{'username':'','password':''})
        self.assertEqual(400,response.status_code)




class UserChangePassword(APITestCase):
    url=reverse('account:change_password')
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username='veli'
        self.password='veli1234'
        self.user=User.objects.create_user(username=self.username,password=self.password)

    def test_login_with_token(self):
        response=self.client.post(self.url_login,{'username':'veli','password':'veli1234'})
        self.assertEqual(200,response.status_code)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_is_authenticated_user(self):
        response=self.client.get(self.url)
        self.assertEqual(401,response.status_code)


    def test_with_valid_data(self):
        self.test_login_with_token()
        data={
            'old_password':'veli1234',
            'new_password':'veli4321'
        }
        response=self.client.put(self.url,data)
        self.assertEqual(204,response.status_code)






