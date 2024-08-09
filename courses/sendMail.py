from django.db.models.signals import post_save
from django.conf import settings
from .models import Notification, CourseClass as Class
from users.models import User
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse

def sendNotification(notification):
    course = Class.objects.get(id=notification.ForClass.id)
    students = User.objects.filter(id__in=course.participants.all()).exclude(is_staff=1).exclude(is_superuser=1).order_by('username')

    subject = notification.title
    message = f"""by {notification.author} - {notification.date_created}
        {notification.text}
    """
    
    sender = settings.EMAIL_HOST_USER
    #receiver = [st.email for st in students]
    receiver = [User.objects.get(username='admin').email]
    send_mail(subject, message, sender, receiver, fail_silently=False)