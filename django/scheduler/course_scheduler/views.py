#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import Class, MeetingTime
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
                classes = MeetingTime.objects.filter(meeting_class__dept__icontains=arr[0], meeting_class__class_number__icontains=arr[1])
            else:
                classes = MeetingTime.objects.filter(Q(meeting_class__classname__icontains=criterion) | Q(meeting_class__dept__icontains=criterion) | Q(meeting_class__class_number__icontains=criterion))
                numb = len(Class.objects.all())
    
            return render(request, 'add.html', {'numb' : len(MeetingTime.objects.all()), 'classes' : classes})
        else:
            return render(request, 'add.html')

def info(request):
    course = request.GET.get('course', NONE)
    return render(request, 'info.html', {'course' : course})
    
class SearchForm(forms.Form):
        criterion = forms.CharField(max_length=100)
