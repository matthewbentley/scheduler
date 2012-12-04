#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import Class, MeetingTime, Instructs, Instructor
from django.http import Http404
from django.db.models import Q
import re

def schedule(request):
    return render(request, 'schedule.html')

def add(request):
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
    
            return render(request, 'add.html', {'classes' : classes})
        else:
            return render(request, 'add.html')

def info(request):
    theCourse = request.GET.get('course', None)
    if theCourse != None:
        arr = theCourse.split('~!~')
        classes = Instructs.objects.filter(meeting__meeting_class__dept__icontains=arr[0], meeting__meeting_class__class_number__icontains=arr[1])
        return render(request, 'info.html', {'course' : theCourse, 'classes' : classes})
    return render(request, 'info.html')

def instructor(request):
    ins = request.GET.get('instructor', None)
    if ins != None:
        prof = Instructor.objects.get(name=ins)
        return render(request, 'instructor.html', {'prof' : prof})
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
