#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import Class
from django.http import Http404
from django.db.models import Q
import re

def schedule(request):
    return render(request, 'schedule.html')

def add(request):
    if request.method == 'GET':
        criterion = request.GET.get('Search', None)
        patt = re.compile('\w\w\w\w (\w\w\w)|(\w\w\w\w)')
        if criterion != None:
            if patt.match(criterion):
                arr = criterion.split(' ')
                classes = Class.objects.filter(dept__icontains=arr[0], class_number__icontains=arr[1])
            else:
                classes = Class.objects.filter(Q(classname__icontains=criterion) | Q(dept__icontains=criterion) | Q(class_number__icontains=criterion))
                numb = len(Class.objects.all())
    
            return render(request, 'add.html', {'classes' : classes})
        else:
            return render(request, 'add.html')

def info(request):
    course = request.GET.get('course', NONE)
    return render(request, 'info.html', {'course' : course})
    
class SearchForm(forms.Form):
        criterion = forms.CharField(max_length=100)
