from django.shortcuts import get_object_or_404

from .models import QRCode_VCard, QRCode_Web, QRCode_Wifi


def get_qr_object(type, qr_id):
    types = {
        "web": QRCode_Web,
        "vcard": QRCode_VCard,
        "wifi": QRCode_Wifi,
    }
    return get_object_or_404(types.get(type), pk=qr_id)