from courses.models import Notification, Assignment, CourseClass

from datetime import timezone

def getIn4(request):
    user = request.user
    notifications = []
    events = []
    event_list = []

    if Notification.objects.exists():
        notifications = Notification.objects.filter(ForClass__participants__exact=user.id).order_by('-date_created')[:5]

    if Assignment.objects.exists():
        courses = []
        courses_list = CourseClass.objects.all()
        for course in courses_list:
            if user in course.participants.all():
                courses.append(course)

        events = Assignment.objects.filter(ForClass__in=courses).order_by('date_opened', 'date_opened')

        for event in events:
            datetime = event.date_closed
            datetime = datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)

            event_list.append(event.title)
            event_list.append(datetime.strftime("%Y"))
            event_list.append(datetime.strftime("%m"))
            event_list.append(datetime.strftime("%d"))
            
    return user, notifications, event_list