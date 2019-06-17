from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from rest_framework.response import Response
import base64
import segno
import io

from .models import QRCode_Web, QRCode_VCard, QRCode_Wifi
from .utils import get_qr_object
from QR_Business.settings import MEDIA_ROOT, MEDIA_URL


@login_required
def details(request, type, qr_id): 
    qr = get_qr_object(type, qr_id)
    context = {
        "qrcode": qr,
        "type": type
    }

    if request.method == "GET":
        buff = io.BytesIO()
        segno.make(qr.generate_QR(), error="H").save(buff, kind="png", scale=15)
        encoded = base64.b64encode(buff.getvalue()).decode()
        context.update({"qr_img": encoded})
        return render(request, f"qrcodes/qrdetails{type}.html", context)

    if request.method == "POST":
        qr.name = request.POST["name"]

        if type == "web":
            qr.url = request.POST["url"]
        elif type == "wifi":
            qr.wifiname = request.POST["wifiname"]
            qr.wifipassword = request.POST["password"]
            qr.wifitype = request.POST["type"]
        elif type == "vcard":
            qr.firstname = request.POST["firstname"]
            qr.lastname = request.POST["lastname"]
            qr.email = request.POST["email"]
            qr.phone = request.POST["phone"]

        qr.save()

        return redirect(request.get_full_path())

@login_required
def home(request):
    if request.method == "GET": 
        context = {
            "qrcodes_web": QRCode_Web.objects.filter(user=request.user),
            "qrcodes_wifi":QRCode_Wifi.objects.filter(user=request.user),
            "qrcodes_vcard":QRCode_VCard.objects.filter(user=request.user)
        }
        
        return render(request, "qrcodes/home.html", context)

    return HttpResponseBadRequest()

@login_required
def new_web_qr(request):
    if request.method == "GET":
        return render(request, "qrcodes/qrweb.html")

    if request.method == "POST":
        qr = QRCode_Web()
        qr.name = request.POST["name"]
        qr.url = request.POST["url"]
        qr.user = request.user
        qr.save()
    
        return redirect(f"/qr/details/web/{qr.qr_id}")   
    return HttpResponseBadRequest()

@login_required
def new_vcard_qr(request):
    if request.method == "GET":
        return render(request, "qrcodes/qrvcard.html")

    if request.method == "POST":
        qr = QRCode_VCard()
        qr.name = request.POST["name"]
        qr.user = request.user
        qr.firstname = request.POST["firstname"]
        qr.lastname = request.POST["lastname"]
        qr.email = request.POST["email"]
        qr.phone = request.POST["phone"]
        qr.save()

        return redirect(f"/qr/details/vcard/{qr.qr_id}")
    
    return HttpResponseBadRequest()

@login_required
def new_wifi_qr(request):
    if request.method == "GET":
        return render(request, "qrcodes/qrwifi.html")

    if request.method == "POST":
        qr = QRCode_Wifi()
        qr.name = request.POST["name"]
        qr.user = request.user
        qr.wifiname = request.POST["wifiname"]
        qr.wifipassword = request.POST["password"]
        qr.wifitype = request.POST["type"]
        qr.save()

        return redirect(f"/qr/details/wifi/{qr.qr_id}")
    
    return HttpResponseBadRequest()