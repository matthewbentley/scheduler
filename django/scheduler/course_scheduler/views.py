#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import Class
from django.http import Http404
from django.db.models import Q

def schedule(request):
    return render(request, 'schedule.html')

def add(request):
    if request.method == 'GET':
        criterion = request.GET.get('Search', None)
        if criterion not None:
            classes = Class.objects.get(Q(classname__contains=criterion) | Q(dept__contains=criterion) | Q(class_number__contains=criterion))
            #classes = Class.objects.order_by('class_number')[:5]
            numb = len(Class.objects.all())
    
            return render(request, 'add.html', {'number' : numb, 'classes' : classes})
        else:
            return render(request, 'add.html')

def info(request):
    course = request.GET.get('course', NONE)
    return render(request, 'info.html', {'course' : course})
    
class SearchForm(forms.Form):
        criterion = forms.CharField(max_length=100)
