from django.db.models.signals import post_save
from django.conf import settings
from .models import Notification, CourseClass as Class
from users.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
    receiver = [User.objects.get(username='admin1').email]
    send_mail(subject, message=message, from_email=sender, recipient_list=receiver, fail_silently=False, html_message=message)

def Create_Notification_Assignment(assignment):
    course = Class.objects.get(id=assignment.ForClass.id)
    students = User.objects.filter(id__in=course.participants.all()).exclude(is_staff=1).exclude(is_superuser=1).order_by('username')

    notification = Notification()
    notification.author = assignment.author
    notification.ForClass = assignment.ForClass
    notification.title = "Asignment: " + assignment.title
    notification.text = "<br>" + "A new assignment was added to " + "<p> <a href=" + "127.0.0.0" + course.course.name + " - " + course.className + "</a></p>"  + "."

    notification.save()
    sendNotification(notification)