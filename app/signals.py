from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from .models import CustomUser
from django.dispatch import receiver
from .models import AuthenticationLog,EmailValidation
from datetime import datetime,date


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in, sender = CustomUser)
def login_success(sender,request,user,**kwargs):
    if request.user.is_superuser != True:
        user = request.user.email
        action = "Logged-In Successfully"
        ipaddress = get_client_ip(request)
        data = AuthenticationLog(user = user, action = action, ip_address = ipaddress)
        data.save()
    else:
        pass

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_out, sender = CustomUser)
def login_success(sender,request,user,**kwargs):
    if request.user.is_superuser != True:
        user = request.user.email
        action = "Logged-Out Successfully"
        ipaddress = get_client_ip(request)
        timestamp = datetime.now()
        data = AuthenticationLog(user = user, action = action, ip_address = ipaddress,timestamp=timestamp)
        data.save()
    else:
        pass




@receiver(user_logged_out, sender = CustomUser)
def log_out(sender, request, user, **kwargs):
    print("Logged-Out Successfully")


@receiver(user_login_failed)
def login_failed(sender,credentials, request, **kwargs):
    print("Login-Failed")
