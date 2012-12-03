# Create your views here.
from django.shortcuts import render
from django import forms

def schedule(request):
    return render(request, 'schedule.html')

def add(request):
    if request.method == 'get':
        form = SearchForm(request.POST)
    else:
        form = SearchForm()
        
    return render(request, 'add.html', {'form': form, 'crit' : request.GET.get('Search', None)})

def search(request):
    return render(request, 'add.html')
    
class SearchForm(forms.Form):
        criterion = forms.CharField(max_length=100)