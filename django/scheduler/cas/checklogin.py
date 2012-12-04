import sys
sys.path.append('/srv/www/scheduler/application/scheduler/cas/')
import pycas
from pycas import CAS_OK, CAS_COOKIE_EXPIRED, CAS_COOKIE_INVALID
from pycas import CAS_TICKET_INVALID, CAS_GATEWAY, CAS_NOTLOGGED, CAS_MSG
from django.http import HttpResponse
from django.http import HttpResponseRedirect

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
    elif (status == CAS_COOKIE_INVALID):
        return True, id, ""
    else:
        return False, status, ""

def redirect_to_cas(SERVICE_URL):
    CAS_SERVER  = "http://login.case.edu"
    return HttpResponseRedirect(CAS_SERVER + "/cas/login?service=" + SERVICE_URL)
