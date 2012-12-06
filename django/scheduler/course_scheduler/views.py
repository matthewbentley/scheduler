from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import *
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.exceptions import ValidationError
import re
import sys
import random

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
    colors = ['#FF0000', '#32E01B', '#003CFF', '#FF9D00', '#00B7FF', '#9D00FF', '#FF00EA', '#B5AA59', '#79BF6B', '#CFA27E']


    stu, created = Student.objects.get_or_create(case_id=id)
    classes = []
    toSend = {}
    if created == False:
        enrolls = Enrollment.objects.filter(student__case_id=id)

        for enroll in enrolls:
            event = Event.objects.get(id=enroll.event_id)
            top = event.start_time.hour - 6
            top += event.start_time.minute / 60.0
            top *= 75
            top += 135
            height = event.start_time.hour + (event.start_time.minute / 60.0)
            height = (event.end_time.hour + event.end_time.minute / 60.0) - height
            height *= 60
            height *= 1.2
            randColor = random.randint(0, len(colors)-1)
            color = colors[randColor] + ''
            del colors[randColor]
            toSend[event] = [top, height, color]


    response = render(request, 'schedule.html', {'events' : toSend, 'id' : id})
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
            toSend = {}
            if patt.match(criterion):
                arr = criterion.split(' ')
                #classes = MeetingTime.objects.filter(meeting_class__dept__icontains=arr[0], meeting_class__class_number__icontains=arr[1])
                classes = Instructs.objects.filter(meeting__meeting_class__dept__icontains=arr[0], meeting__meeting_class__class_number__icontains=arr[1])
            else:
                #classes = MeetingTime.objects.filter(Q(meeting_class__classname__icontains=criterion) | Q(meeting_class__dept__icontains=criterion) | Q(meeting_class__class_number__icontains=criterion))
                classes = Instructs.objects.filter(Q(meeting__meeting_class__classname__icontains=criterion) | Q(meeting__meeting_class__dept__icontains=criterion) | Q(meeting__meeting_class__class_number__icontains=criterion))
                numb = len(Class.objects.all())

            for c in classes:
                if Enrollment.objects.filter(student_id=id, event_id=c.meeting.id).exists():
                    toSend[c] = True
                else:
                    toSend[c] = False

            response = render(request, 'add.html', {'classes' : toSend, 'id' : id})
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

        toSend = {}
        for c in classes:
            if Enrollment.objects.filter(student_id=id, event_id=c.meeting.id).exists():
                toSend[c] = True
            else:
                toSend[c] = False
                    
        response = render(request, 'info.html', {'classes' : toSend, 'id' : id})
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

    toSend={}
    ins = request.GET.get('name', None)
    if ins != None:
        classes = Instructs.objects.filter(instructor=ins)

        for c in classes:
            if Enrollment.objects.filter(student_id=id, event_id=c.meeting.id).exists():
                toSend[c] = True
            else:
                toSend[c] = False

        response = render(request, 'add.html', {'classes' : toSend, 'id' : id})
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
        caseId = request.POST['id']
        stu = Student.objects.get(case_id=caseId)
        enroll = Enrollment(student_id=stu.pk, event_id=eventId)
        enroll.save()
        return HttpResponseRedirect('/scheduler/')
    raise Http404

def removecourse(request):
    if request.method == 'POST':
        eventId = request.POST['eventID']
        caseId = request.POST['id']
        stu = Student.objects.get(case_id=caseId)
        enroll = Enrollment.objects.get(student_id=stu.pk, event_id=eventId)
        enroll.delete()
        return HttpResponseRedirect('/scheduler/')
    raise Http404

def mycourses(request):
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/instructor/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/instructor/')
    if cookie != "":
        setcookie = True

    toSend={}
    eventIDs = Enrollment.objects.filter(student_id=id).values_list('event_id', flat=True)
    classes = Instructs.objects.filter(meeting_id__in=eventIDs)
        
    for c in classes:
        toSend[c]=True

    response = render(request, 'add.html', {'classes' : toSend, 'id' : id})
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response

def customevent(request):
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/instructor/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/instructor/')
    if cookie != "":
        setcookie = True

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/scheduler/')
    else:
        form = EventForm()
    
    response = render(request, 'custom.html', {'id' : id, 'form' : form})
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response

def validate_time(value):
    validAMs = '([6-9]|10|11|12):[0-5][0-9](am|AM)'
    validPMs = '([1-9]|12):[0-5][0-9](pm|PM)'
    validTimes = '(' + validAMs + '( )*-( )*' + validAMs + ')|(' + validAMs + '( )*-( )*' + validPMs + ')|(' + validPMs + '( )*-( )*' + validPMs + ')'
    
    patt = re.compile(validTimes)
    if not patt.match(value):
        raise ValidationError('%s is not a valid time format!' % value)

    if not ""==(re.sub(validTimes, "", value)):
        raise ValidationError('%s is not a valid day format!' % value)

    
def validate_day(value):
    validDays = '((Su)|(M)|(Tu)|(W)|(Th)|(F)|(Sa))+'
    patt = re.compile(validDays)
    if not patt.match(value):
        raise ValidationError('%s is not a valid day format!' % value)

    if not ""==(re.sub(validDays, "", value)):
        raise ValidationError('%s is not a valid day format!' % value)
    
class EventForm(forms.Form):
    event_title=forms.CharField(max_length=100)
    times=forms.CharField(max_length=20, validators=[validate_time])
    days=forms.CharField(max_length=14, validators=[validate_day])


