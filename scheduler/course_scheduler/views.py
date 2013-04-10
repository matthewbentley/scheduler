from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from course_scheduler.models import *
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.exceptions import ValidationError
import datetime
import re
import sys
import random
import string

sys.path.append('/srv/www/scheduler/application/scheduler/cas/')
from checklogin import check_login
from checklogin import redirect_to_cas


#   The view for schedule.html
#   once the user has logged in
#   database is queried for all
#   the events associated with
#   that user's id.
#   The function calculates the
#   absolute position for the colored
#   square for each event and the height
#   for each square for display on the
#   user's schedule. The function also
#   assigns each event a different
#   random color. Each event is put
#   into a dictionary with the event
#   as a key and an array corresponding
#   to the top, height, and color
#   of the square as the value.
#   This dictionary is passed as a
#   context to the schedule.html
#   template which is returned to the
#   webrowser as an HTTPresponse
#   See https://docs.djangoproject.com/en/dev/topics/http/views/
def schedule(request):
    #check to see if the user is logged in
    #if not make the user login
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
            height += 3
            randColor = random.randint(0, len(colors)-1)
            color = colors[randColor] + ''
            del colors[randColor]
            toSend[event] = [top, height, color]


    response = render(request, 'schedule.html', {'events' : toSend, 'id' : id})
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response

#   The view for add.html. This
#   view function is a little more
#   complicated because it sometimes
#   a 'Search' parameter as part
#   of the passed request. It also
#   uses python regexes to check
#   the request against formats
#   such as EECS 337 or EECS341, that
#   way we can query on the proper
#   event attributes. Finally, after
#   finding the querySet for the passed
#   search parameter, we create a dictionary
#   with each event as a key. Then, we run
#   through all of the results and check to see
#   if the current user is enrolled in that event.
#   If so we set the value for that event's key
#   in our dict to the corresponding boolean value.
#   This dictionary is passed as a
#   context to the add.html
#   template which is returned to the
#   webrowser as an HTTPresponse
#   See https://docs.djangoproject.com/en/dev/topics/http/views/
def add(request):
    #check to see if the user is logged in
    #if not make the user login
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/add/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/add/')
    if cookie != "":
        setcookie = True

    toSend = {}
    if request.method == 'GET':
        form = SearchForm(request.GET)
        #criterion = request.GET.get('Search', None)
        #TODO better regexes
        #patt = re.compile('(\w\w\w\w ((\w\w\w)|(\w\w\w\w)))|(\w\w\w\w\w\w\w)')
        patt = re.compile('(\w\w\w\w( )*(\d+|(\d+w)))')
        if form.is_valid():
            criterion = form.cleaned_data['criterion']
            if patt.match(criterion):
                str = string.replace(criterion, ' ', '')
                arr = [None]*2
                arr[0] = str[0:3]
                arr[1] = str[4:]
                #arr = criterion.split(' ')
                classes = Instructs.objects.filter(meeting__meeting_class__dept__icontains=arr[0], meeting__meeting_class__class_number__icontains=arr[1])
            else:
                classes = Instructs.objects.filter(Q(meeting__meeting_class__classname__icontains=criterion) | Q(meeting__meeting_class__dept__icontains=criterion) | Q(meeting__meeting_class__class_number__icontains=criterion))
                numb = len(Class.objects.all())

            for c in classes:
                if Enrollment.objects.filter(student_id=id, event_id=c.meeting.id).exists():
                    toSend[c] = True
                else:
                    toSend[c] = False
    else:
        form = SearchForm()
    response = render(request, 'add.html', {'classes' : toSend, 'id' : id, 'form' : form})
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response

#   The info view is called whenever
#   the user clicks on a meeting-time's
#   name. The function is passed a
#   request with a query string containing
#   the desired course's department and
#   course number. We perform a query search
#   on the Instructs relation to find all
#   classes that match the passed dept and
#   number combination (or at least contain
#   those strings). Then we perform the same
#   search throught the enrollment table
#   to find classes the user is already enrolled
#   in as we did in the add view.
#   This dictionary is passed as a
#   context to the add.html
#   template which is returned to the
#   webrowser as an HTTPresponse
#   See https://docs.djangoproject.com/en/dev/topics/http/views/
def info(request):
    #check to see if the user is logged in
    #if not make the user login
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/info/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/info/')
    if cookie != "":
        setcookie = True

    theCourse = request.GET.get('course', None)
    if theCourse != None:
        #the course is passed in as dept~!~coursenumber
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

#   The instructor view is the view
#   function for the instructor.html.
#   page. This function expects to be
#   sent an 'instructor' query string
#   with the name of the 'clicked-on'
#   instructor. We query the instructor
#   table for the instructor with that name
#   and send that instructor as a context
#   to the instructor.html template, and
#   that html file is returned as a
#   HTTPresponse page
#   See https://docs.djangoproject.com/en/dev/topics/http/views/s
def instructor(request):
    #check to see if the user is logged in
    #if not make the user login
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

#   The inscourse view is a temporary view
#   that redirects the user back to the
#   add.html page. However, the query we
#   have to perform is slightly different,
#   thus neccessitating an entirely new view.
#   Here we are passed an instructor name
#   as part of the request. We query the
#   Instructs table for all of the tuples
#   whose instructor's name matched the
#   name query string. We then perform
#   the same filter from add where
#   we check to see which of the courses
#   from the first queryset the user is enrolled
#   in. We create a dictionary of classes to booleans
#   and pass that as a context to the add.html template
#   and return as a HttpResponse
#   See https://docs.djangoproject.com/en/dev/topics/http/views/
def inscourse(request):
    #check to see if the user is logged in
    #if not make the user login
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

        response = render(request, 'add.html', {'classes' : toSend, 'id' : id, 'form' : SearchForm()})
        if setcookie == True:
            response.__setitem__('Set-Cookie', cookie)
        return response
    return render(request, 'add.html', {'id' : id, 'form' : SearchForm()})

#   The insearch view is the view function
#   for the insearch.html page. This view
#   can take in a name query string but does
#   not neccessarily expect it. If there is
#   a valid name query string, we query the
#   intructor table for all of the instructors
#   whose name or email contains the query
#   string. We then send that query set as a
#   context to the 'inssearch.html' template
#   file which is then returned as a
#   HttpResponse
#   See https://docs.djangoproject.com/en/dev/topics/http/views/
def inssearch(request):
    #check to see if the user is logged in
    #if not make the user login
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

#   The addcourse is a temporary view
#   that is called when a user click
#   an 'add course' button. The view
#   expects a request containing an
#   'eventId' string representing the
#   id of the event the user is trying
#   to add and an 'id' query string that
#   is the id of the current user. We then
#   create a new enroll tuple with the
#   student's id and the event's id
#   as the two foreign keys. Then we
#   redirect the application to the
#   scheduler page with a
#   HttpResponseRedirect
#   See https://docs.djangoproject.com/en/dev/topics/http/views/
def addcourse(request):
    if request.method == 'POST':
        eventId = request.POST['eventID']
        caseId = request.POST['id']
        stu = Student.objects.get(case_id=caseId)
        enroll = Enrollment(student_id=stu.pk, event_id=eventId)
        enroll.save()
        return HttpResponseRedirect('/scheduler/')
    raise Http404

#   The removecourse is a temporary view
#   that is called when a user click
#   an 'remove course' button. The view
#   expects a request containing an
#   'eventId' string representing the
#   id of the event the user is trying
#   to remove and an 'id' query string that
#   is the id of the current user. We then
#   query the enroll table for the tuple
#   ith the user's id as the event's id
#   as the query parameters and delete
#   the resulting tupe. Then we
#   redirect the application to the
#   scheduler page with a
#   HttpResponseRedirect
#   See https://docs.djangoproject.com/en/dev/topics/http/views/
def removecourse(request):
    if request.method == 'POST':
        eventId = request.POST['eventID']
        caseId = request.POST['id']
        stu = Student.objects.get(case_id=caseId)
        enroll = Enrollment.objects.get(student_id=stu.pk, event_id=eventId)
        enroll.delete()
        return HttpResponseRedirect('/scheduler/')
    raise Http404

#   The mycourses view function is another
#   view function for the add.html page.
#   Unlike the other two, this function
#   immediately finds all of the courses
#   that the current user is enrolled in
#   and sends that dictionary as a context
#   to add.html
#   See https://docs.djangoproject.com/en/dev/topics/http/views/
def mycourses(request):
    #check to see if the user is logged in
    #if not make the user login
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

    response = render(request, 'add.html', {'classes' : toSend, 'id' : id, 'form' : SearchForm()})
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response

#   The about view function
#   is the trivial view function
#   that just returns the rendering
#   of the about.html template file
def about(request):
    #check to see if the user is logged in
    #if not make the user login
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/instructor/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/instructor/')
    if cookie != "":
        setcookie = True

    return render(request, 'about.html')

#   The customevent view function is the view
#   for the custom.html field. If the event
#   is passed a request with a POST method,
#   ie the user hit a submit button, then
#   the view all of the query strings and,
#   if the strings are valid (see below),
#   we create a new entry in the customevent
#   table with the query strings set as the
#   corresponding attributes. Then we create
#   a new enrollment table entry linking the
#   current user to the newly created custom
#   event. Then we return a HttpResponseRedirect
#   to the home page If this view is called without
#   a POST request method, then we simply
#   pass the custom.html template
#   an empty instance of an EventForm
#   (see below) and return the rendered
#   custom.html page as a HttpResponse.
#   See https://docs.djangoproject.com/en/dev/topics/http/views/
def customevent(request):
    #check to see if the user is logged in
    #if not make the user login
    status, id, cookie = check_login(request, 'http://concertina.case.edu/scheduler/instructor/')
    setcookie = False
    if status == False:
        return redirect_to_cas('http://concertina.case.edu/scheduler/instructor/')
    if cookie != "":
        setcookie = True

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['event_title']
            time = form.cleaned_data['times']
            sdate = form.cleaned_data['start_date']
            edate = form.cleaned_data['end_date']
            
            try:
                loc = form.cleaned_data['location']
            except:
                loc = ""

            startTimeArr, endTimeArr = parse_time(time)

            dayStr = ''
            if form.cleaned_data['su']:
                dayStr += 'Su'
            if form.cleaned_data['m']:
                dayStr += 'M'
            if form.cleaned_data['tu']:
                dayStr += 'Tu'
            if form.cleaned_data['w']:
                dayStr += 'W'
            if form.cleaned_data['th']:
                dayStr += 'Th'
            if form.cleaned_data['f']:
                dayStr += 'F'
            if form.cleaned_data['sa']:
                dayStr += 'Sa'

            if '' == dayStr:
                return render(request, 'custom.html', {'id' : id, 'form' : form, 'dayErr' : True})
            
            #event = CustomEvent(start_time=datetime.time(startTimeArr[0], startTimeArr[1]), end_time=datetime.time(endTimeArr[0], endTimeArr[1]), recur_type=days, event_name=name)
            event = CustomEvent(start_time=datetime.time(startTimeArr[0], startTimeArr[1]), end_time=datetime.time(endTimeArr[0], endTimeArr[1]), start_date=sdate, end_date=edate, recur_type=dayStr, event_name=name, location=loc)
            event.save()

            stu = Student.objects.get(case_id=id)
            enroll = Enrollment(student_id=stu.pk, event_id=event.id)
            enroll.save()
            
            return HttpResponseRedirect('/scheduler/')
    else:
        form = EventForm()
    
    response = render(request, 'custom.html', {'id' : id, 'form' : form})
    if setcookie == True:
        response.__setitem__('Set-Cookie', cookie)
    return response

#   This function is the validation function for
#   the times field in EventForm. It uses regexes
#   to check that the user's passed time is in a form
#   such as 9:00am-10:00 pm. If the times input does not
#   match the regex, or if the end date is before
#   the start date, we raise a validationError,
#   which refuses the user's submission
#   and supplies the appropriate error message.
#   See https://docs.djangoproject.com/en/dev/ref/validators/
def validate_time(value):
    validAMs = '([6-9]|10|11|12):[0-5][0-9](am|AM)'
    validPMs = '([1-9]|12):[0-5][0-9](pm|PM)'
    validTimes = '(' + validAMs + '( )*-( )*' + validAMs + ')|(' + validAMs + '( )*-( )*' + validPMs + ')|(' + validPMs + '( )*-( )*' + validPMs + ')'
    
    patt = re.compile(validTimes)
    if not patt.match(value):
        raise ValidationError('%s is not a valid time format!' % value)

    if not ""==(re.sub(validTimes, "", value)):
        raise ValidationError('%s is not a valid time format!' % value)
    
    startTimeArr, endTimeArr = parse_time(value)
    
    actSTime = startTimeArr[0] + startTimeArr[1] / 60.0
    actETime = endTimeArr[0] + endTimeArr[1] / 60.0

    if actSTime >= actETime:
        raise ValidationError('Start Time must be after end Time!')

#   This function is the validation function for
#   the days field in EventForm. It uses regexes
#   to check that the user's passed days is in a form
#   such as MWF or FSu. If the days input does not
#   match the regex, we raise a validationError,
#   which refuses the user's submission
#   and supplies the appropriate error message.
#   See https://docs.djangoproject.com/en/dev/ref/validators/
def validate_day(value):
    validDays = '((Su)|(M)|(Tu)|(W)|(Th)|(F)|(Sa))+'
    patt = re.compile(validDays)
    if not patt.match(value):
        raise ValidationError('%s is not a valid day format!' % value)

    if not ""==(re.sub(validDays, "", value)):
        raise ValidationError('%s is not a valid day format!' % value)

#   The parse_time function
#   is a helper function that
#   takes in an array whose
#   first index is a start time
#   and whose second index is
#   an end time. It then converts
#   those strings to python datetime.time
#   objects and returns two arrays, one
#   for the converted starttime and one
#   for the converted endtime
def parse_time(array):
    timeArr = array.split('-')
    timeArr[0]=re.sub(r'( )+', "", timeArr[0])
    timeArr[1]=re.sub(r'( )+', "", timeArr[1])

    startTimeArr = timeArr[0].split(':')
    startTimeArr[1] = startTimeArr[1][:2]
    startTimeArr[0] = int(startTimeArr[0])
    startTimeArr[1] = int(startTimeArr[1])
    if 'pm' in timeArr[0] or 'PM' in timeArr[0]:
        if startTimeArr != 12:
            startTimeArr[0] = startTimeArr[0] + 12
            
    endTimeArr = timeArr[1].split(':')
    endTimeArr[1] = endTimeArr[1][:2]
    endTimeArr[0] = int(endTimeArr[0])
    endTimeArr[1] = int(endTimeArr[1])
    if 'pm' in timeArr[1] or 'PM' in timeArr[1]:
        if endTimeArr != 12:
            endTimeArr[0] = endTimeArr[0] + 12
    return startTimeArr, endTimeArr

#   The EventForm class is a simple
#   instance of a forms.Form. Every
#   field we want the user to supply
#   data for is set an a member attribute
#   of this class. Two of the fields, location
#   and days, are given their own custom validators
#   since we allow any chars to be entered but we
#   want those strings to have a certain form, eg
#   MWF is valid for days but CANDV is not.
#   See https://docs.djangoproject.com/en/dev/topics/forms/?from=olddocs
class EventForm(forms.Form):
    event_title=forms.CharField(max_length=100)
    location=forms.CharField(max_length=100, required=False)
    times=forms.CharField(max_length=20, validators=[validate_time])
    start_date=forms.DateField()
    end_date=forms.DateField()
    #days=forms.CharField(max_length=14, validators=[validate_day])
    CHOICES=((0,'M'),(0,'Tu'),(0,'W'),(0,'Th'),(0,'F'),(0,'Sa'),(0,'Su'))
    m = forms.BooleanField(label="day", required=False)
    tu = forms.BooleanField(label="day", required=False)
    w = forms.BooleanField(label="day", required=False)
    th = forms.BooleanField(label="day", required=False)
    f = forms.BooleanField(label="day", required=False)
    sa = forms.BooleanField(label="day", required=False)
    su = forms.BooleanField(label="day", required=False)
    
class SearchForm(forms.Form):
    criterion=forms.CharField(max_length=100)

