#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import Class
from django.http import Http404

def schedule(request):
    return render(request, 'schedule.html')

def add(request):
    if request.method == 'GET':
        criterion = request.GET.get('Search', None)
        #classes = Class.objects.filter(classname__contains=criterion)
        classes = {Class.objects.all()}
        numb = {len(Class.objects.all())}
        
        return render(request, 'add.html', {"numb" : numb, "classes" : classes})
    raise Http404

def info(request):
    course = request.GET.get('course', NONE)
    return render(request, 'info.html', {'course' : course})
    
class SearchForm(forms.Form):
        criterion = forms.CharField(max_length=100)
