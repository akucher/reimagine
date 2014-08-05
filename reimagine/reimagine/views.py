from django.shortcuts import render, render_to_response, RequestContext
import urllib, urllib2
import json


LINKEDIN_API_KEY = "776ywpl03eew4l"
LINKEDIN_API_SECRET_KEY = "r6jfeipGFChJCPTi"


def profile(request):
    context = locals()
    code = request.GET.get('code')

    if code:
        url = 'https://www.linkedin.com/uas/oauth2/accessToken'
        values = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': 'http://127.0.0.1:8000/profile/', 'client_id': LINKEDIN_API_KEY, 'client_secret': LINKEDIN_API_SECRET_KEY}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        decoded = json.loads(response.read())
        context['auth_token'] = response.read()
        context['access_token'] = decoded['access_token']
        context['expires_in'] = decoded['expires_in']
        url_getBasics = "https://api.linkedin.com/v1/people/~:(firstName,lastName)?oauth2_access_token=" + decoded['access_token'] + "&format=json"
        #basicInfo = urllib2.urlopen(url_getBasics).read()
        req1 = urllib2.Request(url_getBasics)
        response1 = urllib2.urlopen(req1)
        the_page1 = response1.read()
        context['basicInfo'] = the_page1
    else:
        context['auth_url'] = "https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=" + LINKEDIN_API_KEY + "&state=dksaddwkeke2i489873893eujklsdkjskljd&redirect_uri=http://127.0.0.1:8000/profile/"
        ##context['auth_url'] = request.GET.get('message')
    return render_to_response("profile.html", context, context_instance=RequestContext(request))