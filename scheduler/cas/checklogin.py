import sys
import course_scheduler
from course_scheduler.strings import Strings

sys.path.append(Strings.SYSTEM_PATH_PREFIX + 'application/scheduler/cas/')
import pycas
from pycas import CAS_OK, CAS_COOKIE_EXPIRED, CAS_COOKIE_INVALID
from pycas import CAS_TICKET_INVALID, CAS_GATEWAY, CAS_NOTLOGGED, CAS_MSG
from django.http import HttpResponse
from django.http import HttpResponseRedirect


#Check login takes the request object from Django and the Service URL to which to redirect.
#This allows the user to re-log-in from any page, rather than from just the main page.
#Check login authenticates the user with CAS and passes the user's id back to views.py
#If the user is not authenticated, it returns false back to views.py
def check_login(request, SERVICE_URL):
    CAS_SERVER  = "http://login.case.edu"
    ticket = request.GET.get('ticket', None)
    cookies = {}
    print >> sys.stderr, "testing"
    if request.COOKIES != None:
        cookies = request.COOKIES
    if ticket == None:
        ticket = ""
    status, id, cookie = pycas.login(CAS_SERVER, SERVICE_URL, cookies, ticket, secure=0, opt="gateway")
    if (status == CAS_OK):
        return True, id, cookie
    else:
        return False, "", ""

#Redirect_To_CAS is very straightforward - it simply returns a redirect object that redirects the user to CAS.
def redirect_to_cas(SERVICE_URL):
    CAS_SERVER  = "http://login.case.edu"
    return HttpResponseRedirect(CAS_SERVER + "/cas/login?service=" + SERVICE_URL)
