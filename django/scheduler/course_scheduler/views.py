#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import Class, MeetingTime, Instructs, Instructor
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

    if setcookie == True:
        response = render(request, 'schedule.html', {'id' : id})
        response.__setitem__('Set-Cookie', cookie)
        return response
    else:
        return render(request, 'schedule.html', {'id' : id})

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
            if setcookie == True:
                response = render(request, 'add.html', {'classes' : classes, 'id' : id})
                response.__setitem__('Set-Cookie', cookie)
                return response
            else:
                return render(request, 'add.html', {'classes' : classes, 'id' : id})
        else:
            return render(request, 'add.html')

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
        if setcookie == True:
            response = render(request, 'info.html', {'course' : theCourse, 'classes' : classes, 'id' : id})
            response.__setitem__('Set-Cookie', cookie)
            return response
        else:
            return render(request, 'info.html', {'course' : theCourse, 'classes' : classes, 'id' : id})
    return render(request, 'info.html')

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
        if setcookie == True:
            response = render(request, 'instructor.html', {'prof' : prof, 'id' : id})
            response.__setitem__('Set-Cookie', cookie)
            return response
        else:
            return render(request, 'instructor.html', {'prof' : prof, 'id' : id})
    return render(request, 'instructor.html')

def inscourse(request):
    ins = request.GET.get('name', None)
    if ins != None:
        classes = Instructs.objects.filter(instructor=ins)
        return render(request, 'add.html', {'classes' : classes})
    return render(request, 'add.html')

def inssearch(request):
        if request.method == 'GET':
            name = request.GET.get('name', None)
            if name != None:
                profs = Instructor.objects.filter(Q(name__icontains=name) | Q(email__icontains=name))
        
                return render(request, 'inssearch.html', {'profs' : profs})
            return render(request, 'inssearch.html')
        else:
            return render(request, 'inssearch.html')
