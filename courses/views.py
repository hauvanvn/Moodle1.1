from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CourseClass as Class, FileUpload, Notification, Comment, Assignment, Submission
from .forms import FileUploadForm, AnnouncementForm, AssignmentForm, GradingForm
from users.models import User

from moodle.nav_infomation import getIn4
from moodle.views import Http404NotFound
from django.http import HttpResponse

from .sendMail import sendNotification, Create_Notification_Assignment
import datetime

# Create your views here.
@login_required(login_url='users:login')
def view_class_list(request):
    user, notifications, events = getIn4(request)

    courses = []

    if Class.objects.exists():
        cur_date = datetime.date.today()
        open_date = datetime.date(cur_date.year - 3, cur_date.month, cur_date.day)

        courses = Class.objects.filter(participants=user.id).order_by('-date_created')

    return render(request, 'courses/View_courses_list.html', {'user': user, 'notifies': notifications, 'events': events, 'courses': courses})

@login_required(login_url='users:login')
def view_class_page(request, slug):
    course = Class.objects.get(slug=slug)
    user, notifications, events = getIn4(request)
    if user not in course.participants.all():
        return Http404NotFound(request)

    files = FileUpload.objects.filter(inClass=course.id)
    assignments = Assignment.objects.filter(ForClass=course.id)
    
    if request.method == "POST":
        if 'delete_material' in request.POST:
            # Delete material
            file_delete = FileUpload.objects.get(id=request.POST.get('delete_material'))
            file_delete.delete()
            messages.success(request, "Delete successful!")
            return redirect('courses:class_page', slug=slug)
        elif 'delete_assignment' in request.POST:
            # Delete assignment
            assignment = Assignment.objects.get(id=request.POST.get('delete_assignment'))
            assignment.delete()
            messages.success(request, "Delete successful!")
            return redirect('courses:class_page', slug=slug)
        else:
            # Add material
            name = request.POST.get('name')
            if 'General' in request.POST:
                group = FileUpload.FileGroup.GENERAL
            elif 'Lecture' in request.POST:
                group = FileUpload.FileGroup.LECTURE
            else:
                group = 'assignment'

            if group != 'assignment':
                # Upload material
                type = FileUpload.FileType.FILE
                link = request.POST.get('link')
                if link == '':
                    type = FileUpload.FileType.FILE
                else:
                    type = FileUpload.FileType.LINK

                # Check input all infomations
                if name == '':
                    messages.warning(request, "Missing name of material!")
                    return redirect('courses:class_page', slug=slug)
                if type == FileUpload.FileType.FILE:
                    if request.FILES is None:
                        messages.warning(request, "Missing file upload!")
                        return redirect('courses:class_page', slug=slug)
                else:
                    if link == '':
                        messages.warning(request, "Missing link!")
                        return redirect('courses:class_page', slug=slug)

                form = FileUploadForm({'name': name, 'group': group, 'type': type, 'link': link, 'inClass': course}, request.FILES)
                
                if form.is_valid():
                    form.save()
                    messages.success(request, "Upload " + name + " successful!")
                    return redirect('courses:class_page', slug=slug)
                else:
                    return render(request, 'courses/View_course_teacher.html', 
                            {'user': user, 'notifies': notifications, 'events': events,
                             'course' : course, 'files': files, 'assignments': assignments, 
                             'form': form, 'aform' : AssignmentForm()})
            else:
                # Create Assignment
                title = request.POST.get('title')
                date_closed = request.POST.get('date_closed')
                aform = AssignmentForm({'author' : user, 'ForClass': course, 'title': title, 'date_closed': date_closed}, request.FILES)

                if aform.is_valid():
                    aform.save()
                    Create_Notification_Assignment(aform.instance)
                    messages.success(request, "Upload " + title + " assignment successful!")
                    return redirect('courses:class_page', slug=slug)
                else:
                    return render(request, 'courses/View_course_teacher.html', 
                            {'user': user, 'notifies': notifications, 'events': events,
                             'course' : course, 'files': files, 'assignments': assignments,
                             'aform': aform, 'form' : FileUploadForm()})

        
    # Teacher view
    if user.is_staff and not user.is_superuser:
        return render(request, 'courses/View_course_teacher.html', 
                  {'user': user, 'notifies': notifications, 'events': events,
                   'course' : course, 'files': files, 'assignments': assignments,
                    'form': FileUploadForm(), 'aform' : AssignmentForm()})
    else:
    # Student view
        return render(request, 'courses/View_course.html', 
                    {'user': user, 'notifies': notifications, 'events': events,
                     'course' : course, 'files': files, 'assignments': assignments})

@login_required(login_url='users:login')
def view_participants(request, slug):
    course = Class.objects.get(slug=slug)
    user, notifications, events = getIn4(request)
    if user not in course.participants.all():
        return Http404NotFound(request)

    users = User.objects.filter(id__in=course.participants.all()).order_by('-is_superuser', '-is_staff', 'username')
    page = Paginator(users, 20)

    page_number = request.GET.get("page")
    try:
        mode = 0
        participants = page.page(page_number)
    except PageNotAnInteger:
        participants = page.page(1)
    except EmptyPage:
        participants = page.page(page.num_pages)

    return render(request, 'courses/View_participants.html', 
                  {'user': user, 'notifies': notifications, 'events': events,
                   'participants': participants, 'course' : course})

@login_required(login_url='users:login')
def view_material(request, slug, filename):
    user, notifications, events = getIn4(request)
    if user not in Class.objects.get(slug=slug).participants.all():
        return Http404NotFound(request)
    
    file = FileUpload.objects.get(id=filename)
    comments = Comment.objects.filter(file=file).order_by('-date_created')

    if request.method == "POST":
        text = request.POST.get("comment")
        new_comment = Comment(user=user, file=file, text=text)
        new_comment.save()
        return redirect('courses:view_material', slug=slug, filename=filename)

    return render(request, 'courses/View_material.html', 
                  {'user': user, 'notifies': notifications, 'events': events,
                   'file': file, 'comments': comments})

@login_required(login_url='users:login')
def view_announcement(request, slug, id):
    user, notifications, events = getIn4(request)
    if user not in Class.objects.get(slug=slug).participants.all():
        return Http404NotFound(request)
    
    notify = Notification.objects.get(id=id)

    return render(request, 'courses/View_annoucement.html', 
                  {'user': user, 'notifies': notifications, 'events': events, 'notify': notify})

@login_required(login_url='users:login')
def view_post_announcement(request, slug):
    course = Class.objects.get(slug=slug)
    user, notifications, events = getIn4(request)
    if user not in course.participants.all() or not(user.is_staff and not user.is_superuser):
        return Http404NotFound(request)

    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('text')
        form = AnnouncementForm({'title' : title, 'text' : text, 'author' : user, 'ForClass' : course})
        if form.is_valid:
            notify = form.save()
            sendNotification(notify)
            messages.success(request, 'Successfully post announcement!')
            return redirect('courses:class_page', slug=slug)
        else:
            return render(request, 'courses/Post_annoucement.html', 
                          {'user': user, 'notifies': notifications, 'events': events, 'form': form})

    return render(request, 'courses/Post_annoucement.html', 
                  {'user': user, 'notifies': notifications, 'events': events, 'form': AnnouncementForm()})

@login_required(login_url='users:login')
def view_assignment(request, slug, assignmentname):
    user, notifications, events = getIn4(request)
    course = Class.objects.get(slug=slug)
    if user not in course.participants.all():
        return Http404NotFound(request)
    
    assignment = Assignment.objects.get(id=assignmentname)

    if user.is_staff and not user.is_superuser:
        # Teacher view
        students_list = User.objects.filter(id__in=course.participants.all()).exclude(is_staff=1).exclude(is_superuser=1).order_by('username')
        submission_list = []
        numsub = 0
        for student in students_list:
            if Submission.objects.filter(author=student.id, ForAssignment=assignment).exists():
                numsub += 1
                submission = Submission.objects.get(author=student.id, ForAssignment=assignment)
            else:
                submission = {'date_upload': '--', 'grade': None, 'author': None}
            submission_list.append({'student': student, 'submit': submission})

        page = Paginator(submission_list, 20)

        page_number = request.GET.get("page")
        try:
            submissions = page.page(page_number)
        except PageNotAnInteger:
            submissions = page.page(1)
        except EmptyPage:
            submissions = page.page(page.num_pages)

        return render(request, 'courses/View_assignment_teacher.html', 
                    {'user': user, 'notifies': notifications, 'events': events, 'course': course,
                    'numsub': numsub, 'numall': len(students_list),
                        'assignment': assignment, 'submissions': submissions})
    else:
        # Student view
        if request.method == "POST":
            if "add_assignment" in request.POST:
                # Add submission
                new_submit = Submission()
                new_submit.author = user
                new_submit.ForAssignment = assignment
                new_submit.file = request.FILES['submit_file']
                new_submit.save()
                messages.success(request, "Submit successful!")
                return redirect('courses:view_assignment', slug=slug, assignmentname=assignmentname)
            else:
                # Delete submission
                submit = Submission.objects.get(auhor=user)
                submit.delete()
                messages.warning(request, "Delete submission successful!")
                return redirect('courses:view_assignment', slug=slug, assignmentname=assignmentname)

        if Submission.objects.filter(author=user, ForAssignment=assignment).exists():
            submission = Submission.objects.get(author=user, ForAssignment=assignment).file.name.split('/')[-1]
        else:
            submission = "--"
        
        return render(request, 'courses/View_assignment.html', 
                      {'user': user, 'notifies': notifications, 'events': events, 'course': course,
                       'assignment': assignment, 'submission': submission})

def view_grading(request, slug, assignmentname, submission):
    course = Class.objects.get(slug=slug)
    user, notifications, events = getIn4(request)
    if user not in course.participants.all() or not(user.is_staff and not user.is_superuser):
        return Http404NotFound(request)
    
    assignment = Assignment.objects.get(id=assignmentname) 
    submit = Submission.objects.get(id=submission)
    
    
    if request.method == "POST":
        form = GradingForm(request.POST, instance=submit)
        if form.is_valid():
            form.save()
            return redirect('courses:view_assignment', slug=slug, assignmentname=assignmentname)
    else:
        form = GradingForm(instance=submit)


    return render(request, 'courses/View_grading.html',
                  {'user': user, 'notifies': notifications, 'events': events,
                   'course': course, 'assignment': assignment, 'submit': submit, 'form': form})

def view_all_grades(request, slug):
    course = Class.objects.get(slug=slug)
    user, notifications, events = getIn4(request)
    if user not in course.participants.all() or user.is_staff:
        return Http404NotFound(request)
    
    assignments = Assignment.objects.filter(ForClass=course).order_by('date_opened', 'date_opened')
    submissions = Submission.objects.filter(ForAssignment__in=assignments, author=user).order_by('-date_upload')
    return render(request, 'courses/View_all_grades_student.html',
                  {'user': user, 'notifies': notifications, 'events': events,
                   'course': course, 'submissions': submissions})

def view_comment(request, slug, assignmentname, submission):
    course = Class.objects.get(slug=slug)
    user, notifications, events = getIn4(request)

    assignments = Assignment.objects.get(id=assignmentname)
    submit = Submission.objects.get(id=submission)
    if not user == submit.author:
        return Http404NotFound(request)
    
    
    return render(request, 'courses/View_grade_comment.html',
                  {'user': user, 'notifies': notifications, 'events': events,
                   'course': course, 'submit': submit, 'assignment' : assignments})