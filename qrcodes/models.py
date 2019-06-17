from django.contrib.auth.models import User
from django.db import models


class QRCode_Web(models.Model):
    qr_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    url = models.CharField(max_length=500)

    def generate_QR(self):
        return self.url        
    def __str___(self):
        return self.name

class QRCode_Wifi(models.Model):
    qr_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    wifiname = models.CharField(max_length=500, null=True)
    wifipassword =  models.CharField(max_length=500, null=True)
    wifitype =  models.CharField(max_length=20, null=True)

    def generate_QR(self):
        return f"WIFI:T:{self.wifitype};S:{self.wifiname};P:{self.wifipassword};;"
    def __str___(self):
        return self.name 
   
class QRCode_VCard(models.Model):
    qr_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    firstname = models.CharField(max_length=500, null=True)
    lastname = models.CharField(max_length=500, null=True)
    email = models.CharField(max_length=500, null=True)
    phone = models.IntegerField(null=True)

    def generate_QR(self):
        return f"BEGIN:VCARD\r\nVERSION:3.0\r\nN:{self.lastname};{self.firstname}\r\nFN:{self.firstname} {self.lastname}\r\nEMAIL:{self.email}\r\nTEL:{self.phone}\r\nEND:VCARD\r\n"        
    def __str___(self):
        return self.name