from django.test import Client, TestCase
from django.urls import reverse

# Create your tests here.

class UserTestCase(TestCase):

    def setUp(self):
        self.c = Client()

    def test_login_page(self):
        response = self.c.get(reverse('login:login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')
        self.assertContains(response, "user")
        self.assertContains(response, "password")


    def test_signup_page(self):
        response = self.c.get(reverse('login:signup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/signup.html')
        self.assertContains(response, "username")
        self.assertContains(response, "password1")
        self.assertContains(response, "password2")


