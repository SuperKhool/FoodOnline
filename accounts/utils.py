from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail  import EmailMessage
from django.conf import settings

from accounts.models import User


def DetectUser(user):
    if user.role ==1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role ==2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role is None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    
    
#Daynamic Way To send mail for reset Password as well as Active The User! 
def send_verification_email(request,user,mail_subject,email_template):
    current_site = get_current_site(request)
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(email_template,{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
        
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message,from_email,to=[to_email])
    mail.send()
    
 
  
   
# This is None Dynamic Way
'''
def send_password_reset_email(request,user):
    current_site = get_current_site(request)
    mail_subject = "RESET YOUR PASSWORD "
    from_email = settings.DEFAULT_FORM_EMAIL
    message = render_to_string('accounts/emails/reset_password_email.html',{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : default_token_generator.make_token(user),
        
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message,from_email,to=[to_email])
    mail.send()
    
'''


# Decoding The User From The Email And If user Exist Returning The User To The 
def check_valid_user(user,uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
        
    return user,uid
    