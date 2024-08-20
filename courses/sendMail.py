from django.db.models.signals import post_save
from django.conf import settings
from .models import Notification, CourseClass as Class
from users.models import User
from django.core.mail import send_mail
import string

def sendNotification(notification):
    course = Class.objects.get(id=notification.ForClass.id)
    students = User.objects.filter(id__in=course.participants.all()).exclude(is_staff=1).exclude(is_superuser=1).order_by('username')

    subject = notification.title
    message = f"""by {notification.author.first_name} {notification.author.last_name} - {notification.date_created.strftime('%A, %d %B %Y, %I:%M %p')}
        {notification.text}
    """
    
    sender = settings.EMAIL_HOST_USER
    receiver = [User.objects.get(username='admin1').email]
    #receiver = [st.email for st in students]
    send_mail(subject, message=message, from_email=sender, recipient_list=receiver, fail_silently=False, html_message=message)

def Create_Notification_Assignment(assignment):
    course = Class.objects.get(id=assignment.ForClass.id)
    students = User.objects.filter(id__in=course.participants.all()).exclude(is_staff=1).exclude(is_superuser=1).order_by('username')

    notification = Notification()
    notification.author = assignment.author
    notification.ForClass = assignment.ForClass
    notification.title = "Asignment: " + assignment.title
    # Replace 127.0.0.0 with link you want to redirect to.
    notification.text = "<br>" + "A new assignment was added to " + "<a href=" + string.punctuation[1] + settings.ALLOWED_HOSTS[0] + string.punctuation[1] + ">" + course.course.name + " - " + course.className + "." + "</a>"

    notification.save()
    sendNotification(notification)