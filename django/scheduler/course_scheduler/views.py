#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import Class

def schedule(request):
    return render(request, 'schedule.html')

def add(request):
    classes = {len(Class.objects.all())}
    if request.method == 'GET':
        classes = Class.objects.all()
        classes = {len(Class.objects.all())}
        
    return render(request, 'add.html', {'crit' : request.GET.get('Search', None), "classes" : classes})

def info(request):
    return render(request, 'info.html')
    
class SearchForm(forms.Form):
        criterion = forms.CharField(max_length=100)
