#from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from poll.models import Class
#from django.core.urlresolvers import reverse

#from poll.models import Choice, Poll
#
#def vote(request, poll_id):
#    p = get_object_or_404(Poll, pk=poll_id)
#    try:
#        selected_choice = p.choice_set.get(pk=request.POST['choice'])
#    except (KeyError, Choice.DoesNotExist):
#        # Redisplay the poll voting form.
#        return render(request, 'poll/detail.html', {
#            'poll': p,
#            'error_message': "You didn't select a choice.",
#        })
#    else:
#        selected_choice.votes += 1
#        selected_choice.save()
#        # Always return an HttpResponseRedirect after successfully dealing
#        # with POST data. This prevents data from being posted twice if a
#        # user hits the Back button.
#        return HttpResponseRedirect(reverse('poll:results', args=(p.id,)))
    
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