# dashboard_app/utils.py
import ipaddress
import json
import os

from django.conf import settings

def get_client_ip(request):
    # prefer X-Forwarded-For if behind proxy (ensure your proxy sets this)
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # X-Forwarded-For: client, proxy1, proxy2
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

def validate_ip_in_ranges(client_ip, ip_ranges):
    """
    ip_ranges: list of CIDR strings, e.g. ["192.168.1.0/24"]
    returns: True if client_ip is in any provided range.
    """
    if not ip_ranges:
        return True  # treat empty list as allow-all (configurable)
    try:
        addr = ipaddress.ip_address(client_ip)
    except ValueError:
        return False
    for rng in ip_ranges:
        try:
            net = ipaddress.ip_network(rng, strict=False)
        except ValueError:
            continue
        if addr in net:
            return True
    return False

def get_allowed_ip_ranges_for_class(class_obj):
    # class_obj.allowed_ip_ranges may be None or list
    if getattr(class_obj, "allowed_ip_ranges", None):
        return class_obj.allowed_ip_ranges
    # fallback to global default in settings
    return getattr(settings, "ALLOWED_IP_RANGES_DEFAULT", [])