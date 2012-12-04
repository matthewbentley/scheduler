#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import *
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
import re
import sys
sys.path.append('/srv/www/scheduler/application/scheduler/cas/')
from checklogin import check_login
from checklogin import redirect_to_cas

def schedule(request):
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/')
    if cookie != "":
        setcookie = True

    stu, created = Student.objects.get_or_create(case_id=id)
    classes = []
    if created == False
        classes = CourseEnrollment.objects.filter(student=stu.case_id)

    response = render(request, 'schedule.html', {'classes' : classes, 'id' : id})
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response

def add(request):
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/add/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/add/')
    if cookie != "":
        setcookie = True

    if request.method == 'GET':
        criterion = request.GET.get('Search', None)
        patt = re.compile('\w\w\w\w ((\w\w\w)|(\w\w\w\w))')
        if criterion != None:
            if patt.match(criterion):
                arr = criterion.split(' ')
                #classes = MeetingTime.objects.filter(meeting_class__dept__icontains=arr[0], meeting_class__class_number__icontains=arr[1])
                classes = Instructs.objects.filter(meeting__meeting_class__dept__icontains=arr[0], meeting__meeting_class__class_number__icontains=arr[1])
            else:
                #classes = MeetingTime.objects.filter(Q(meeting_class__classname__icontains=criterion) | Q(meeting_class__dept__icontains=criterion) | Q(meeting_class__class_number__icontains=criterion))
                classes = Instructs.objects.filter(Q(meeting__meeting_class__classname__icontains=criterion) | Q(meeting__meeting_class__dept__icontains=criterion) | Q(meeting__meeting_class__class_number__icontains=criterion))
                numb = len(Class.objects.all())

            response = render(request, 'add.html', {'classes' : classes, 'id' : id})
            if setcookie == True:
                response.__setitem__('Set-Cookie', cookie)
            return response
        else:
            return render(request, 'add.html', {'id' : id})

def info(request):
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/info/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/info/')
    if cookie != "":
        setcookie = True

    theCourse = request.GET.get('course', None)
    if theCourse != None:
        arr = theCourse.split('~!~')
        classes = Instructs.objects.filter(meeting__meeting_class__dept__icontains=arr[0], meeting__meeting_class__class_number__icontains=arr[1])

        response = render(request, 'info.html', {'course' : theCourse, 'classes' : classes, 'id' : id})
        if setcookie == True:
            response.__setitem__('Set-Cookie', cookie)
        return response
    return render(request, 'info.html', {'id' : id})

def instructor(request):
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/instructor/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/instructor/')
    if cookie != "":
        setcookie = True

    ins = request.GET.get('instructor', None)
    if ins != None:
        prof = Instructor.objects.get(name=ins)

        response = render(request, 'instructor.html', {'prof' : prof, 'id' : id})
        if setcookie == True:
            response.__setitem__('Set-Cookie', cookie)
        return response
    return render(request, 'instructor.html', {'id' : id})

def inscourse(request):
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/instructor/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/instructor/')
    if cookie != "":
        setcookie = True

    ins = request.GET.get('name', None)
    if ins != None:
        classes = Instructs.objects.filter(instructor=ins)

        response = render(request, 'add.html', {'classes' : classes, 'id' : id})
        if setcookie == True:
            response.__setitem__('Set-Cookie', cookie)
        return response
    return render(request, 'add.html', {'id' : id})

def inssearch(request):
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/instructor/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/instructor/')
    if cookie != "":
        setcookie = True

    if request.method == 'GET':
        name = request.GET.get('name', None)
        if name != None:
            profs = Instructor.objects.filter(Q(name__icontains=name) | Q(email__icontains=name))

            response = render(request, 'inssearch.html', {'profs' : profs, 'id' : id})
            if setcookie == True:
                response.__setitem__('Set-Cookie', cookie)
            return response
        return render(request, 'inssearch.html')
    else:
        return render(request, 'inssearch.html', {'id' : id})

def addcourse(request):
    if request.method == 'POST':
        eventId = request.POST['eventID']
        Enrollment.objects.get_or_create(student__case_id=id, event__id=eventID)
        return schedule(request)
    raise Http404
