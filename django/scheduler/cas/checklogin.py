sys.path.append('/srv/www/scheduler/application/scheduler/cas/')
import pycas
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def check_login(request)
    CAS_SERVER  = "http://login.case.edu"
    SERVICE_URL = "http://concertina.case.edu/"
    token = request.GET.get('token', None)
    cookies = {}
    if request.COOKIES != None:
        cookies = request.COOKIES
    if token == None:
        token = ""
    status, id, cookie = pycas.login(CAS_SERVER, SERVICE_URL, cookies, token, secure=0, opt="gateway")
    if (status == CAS_OK):
        return True, id, cookie
    else:
        return False, "", ""

def redirect_to_cas()
    CAS_SERVER  = "http://login.case.edu"
    SERVICE_URL = "http://concertina.case.edu/"
    return = HttpResponseRedirect(CAS_SERVER + "/cas/login?service=" + SERVICE_URL)
