from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login as dj_login

from .models import QRCode_VCard, QRCode_Web, QRCode_Wifi


# Create your tests here.
class QRCodeTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.myuser = User.objects.create_user(username="testuser", password="matias12345")
        self.web = QRCode_Web.objects.create(qr_id=1, user=self.myuser, name="name", url="www.test.dk")
        self.vcard = QRCode_VCard.objects.create(qr_id=1, user=self.myuser, name="name", firstname="hans", lastname="eriksen", email="test@test.dk", phone="12345678")
        self.wifi = QRCode_Wifi.objects.create(qr_id=1, user=self.myuser, name="name", wifiname="WifiName", wifipassword="1234", wifitype="WPA")

    def test_access_restriction(self):
        self.assertEquals(self.c.get(reverse('qrcodes:home')).status_code, 302)
        self.assertEquals(self.c.get(reverse('qrcodes:new_web_qr')).status_code, 302)
        self.assertEquals(self.c.get(reverse('qrcodes:new_vcard_qr')).status_code, 302)
        self.assertEquals(self.c.get(reverse('qrcodes:new_wifi_qr')).status_code, 302)
    
    def test_home(self):
        self.c.login(username="testuser", password="matias12345")
        response = self.c.get(reverse('qrcodes:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'qrcodes/home.html')
        self.assertContains(response, "Create new Web QR-Code")
        self.assertContains(response, "Create new Vcard QR-Code")
        self.assertContains(response, "Create new WiFi QR-Code")
        self.assertContains(response, "logout")

    def test_new_web_qr(self):
        self.c.login(username="testuser", password="matias12345")
        response = self.c.get(reverse('qrcodes:new_web_qr'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'qrcodes/qrweb.html')
        self.assertContains(response, "Enter QR Name")
        self.assertContains(response, "Enter Url")
        self.assertContains(response, "Create QR")

    def test_new_vcard_qr(self):
        self.c.login(username="testuser", password="matias12345")
        response = self.c.get(reverse('qrcodes:new_vcard_qr'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'qrcodes/qrvcard.html')
        self.assertContains(response, "Enter QR Name")
        self.assertContains(response, "Enter First Name here")
        self.assertContains(response, "Enter Last Name here")
        self.assertContains(response, "Enter Number here")
        self.assertContains(response, "Enter Email here")
        self.assertContains(response, "Create QR")

    def test_new_wifi_qr(self):
        self.c.login(username="testuser", password="matias12345")
        response = self.c.get(reverse('qrcodes:new_wifi_qr'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'qrcodes/qrwifi.html')
        self.assertContains(response, "Enter QR Name")
        self.assertContains(response, "Enter Wifi SSID")
        self.assertContains(response, "Enter Password")
        self.assertContains(response, "Enter Type")
        self.assertContains(response, "Create QR")

    def test_qr_models(self):
        self.assertTrue(isinstance(self.web, QRCode_Web))
        self.assertTrue(isinstance(self.vcard, QRCode_VCard))
        self.assertTrue(isinstance(self.wifi, QRCode_Wifi))

    def test_vcard_wrong_phone(self):
        try:
            QRCode_VCard.objects.create(qr_id=1, user=self.myuser, name="name", firstname="hans", lastname="eriksen", email="test@test.dk", phone="onetwothree")
            self.assertTrue(False)
        except(ValueError):
            pass
