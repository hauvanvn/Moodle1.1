from courses.models import Notification, Assignment, CourseClass

def getIn4(request):
    user = request.user
    notifications = []
    events = []

    if Notification.objects.exists():
        notifications = Notification.objects.filter(ForClass__participants__exact=user.id).order_by('-date_created')[:5]

    if Assignment.objects.exists():
        courses = []
        courses_list = CourseClass.objects.all()
        for course in courses_list:
            if user in course.participants.all():
                courses.append(course)

        events = Assignment.objects.filter(ForClass__in=courses).order_by('date_opened', 'date_opened')

    return user, notifications, events