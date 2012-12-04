#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import Class
from django.http import Http404

def schedule(request):
    return render(request, 'schedule.html')

def add(request):
    criterion = request.GET.get('Search', None)
    classes = Class.objects.order_by('class_number')
    numb = len(Class.objects.all())
        
    return render(request, 'add.html', {"number" : "hey", "classes" : classes})

def info(request):
    course = request.GET.get('course', NONE)
    return render(request, 'info.html', {'course' : course})
    
class SearchForm(forms.Form):
        criterion = forms.CharField(max_length=100)
