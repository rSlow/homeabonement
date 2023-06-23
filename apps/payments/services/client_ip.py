from django.conf import settings
import ipaddress


def get_client_ip(request):
    x_forwarded_for: str = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_ip_valid(ip_string: str):
    ip = ipaddress.ip_address(ip_string)

    valid_net_string_list: list[str] = settings.YOOKASSA_NETS
    for valid_net_string in valid_net_string_list:
        valid_net = ipaddress.ip_network(valid_net_string)
        if ip in valid_net:
            return True

    valid_ip_string_list: list[str] = settings.YOOKASSA_IPS
    for valid_ip_string in valid_ip_string_list:
        valid_ip = ipaddress.ip_address(valid_ip_string)
        if ip == valid_ip:
            return True

    return False
