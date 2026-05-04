from django.core.mail import send_mail
from django.conf import settings

def send_signup_email(user):
    subject = "Welcome to Our Platform!"
    message = f"Hello {user.username},\n\nThank you for signing up!\n\nYour credentials are as follows:\nUsername: {user.username}\n\nBest regards,\nYour Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)