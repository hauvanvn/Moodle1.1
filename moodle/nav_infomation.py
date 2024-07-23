from courses.models import Notification

def getIn4(request):
    user = request.user
    notifications = []

    if Notification.objects.exists():
        notifications = Notification.objects.filter(ForClass__participants__exact=user.id).order_by('date_created')[:3]

    return user, notifications