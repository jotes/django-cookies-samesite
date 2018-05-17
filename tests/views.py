from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def cookies_test(request):
    """
    Initialize sessions and CSRF modules.
    """
    request.session['test'] = 'testing'

    request.META["CSRF_COOKIE_USED"] = True
    response = HttpResponse('cookies!')
    response.set_cookie('custom_cookie', 'something')
    response.set_cookie('zcustom_cookie', 'something')

    return response
