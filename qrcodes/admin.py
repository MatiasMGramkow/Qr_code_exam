from django.contrib import admin

from .models import QRCode_Web, QRCode_VCard, QRCode_Wifi

# Register your models here.
admin.site.register(QRCode_Web)
admin.site.register(QRCode_VCard)
admin.site.register(QRCode_Wifi)