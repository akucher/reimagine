from django.shortcuts import render, render_to_response, RequestContext, redirect
import urllib, urllib2
import json
from models import LinkedIn


LINKEDIN_API_KEY = "776ywpl03eew4l"
LINKEDIN_API_SECRET_KEY = "r6jfeipGFChJCPTi"


def profile(request):

    context = locals()
    context['flag'] = True
    code = request.GET.get('code')
    try:
        entry = LinkedIn.objects.get(user_name='akucher')
    except:
        entry = ''
    if code:

        if entry:
            entry.code = code
            entry.save()
        else:
            linkedin_code = LinkedIn(user_name='akucher', code=code)
            linkedin_code.save()
        url = 'https://www.linkedin.com/uas/oauth2/accessToken'
        values = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': 'http://127.0.0.1:8000/profile/', 'client_id': LINKEDIN_API_KEY, 'client_secret': LINKEDIN_API_SECRET_KEY}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        decoded = json.loads(response.read())
        context['auth_token'] = response.read()
        context['access_token'] = decoded['access_token']
        context['expires_in'] = decoded['expires_in']
        entry = LinkedIn.objects.get(user_name='akucher')
        entry.token = decoded['access_token']
        entry.save()
        return redirect("/profile/", context)
    else:
        context['auth_url'] = "https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=" + LINKEDIN_API_KEY + "&state=dksaddwkeke2i489873893eujklsdkjskljd&redirect_uri=http://127.0.0.1:8000/profile/"
        if entry:
            if entry.token:
                context['flag'] = False
                url_getbasics = "https://api.linkedin.com/v1/people/~:(id,firstName,lastName,headline,public-profile-url,positions,summary,skills,interests,languages,educations,volunteer,three-current-positions,three-past-positions,honors-awards)?oauth2_access_token=" + entry.token + "&format=json"
                #basicInfo = urllib2.urlopen(url_getBasics).read()
                req1 = urllib2.Request(url_getbasics)
                response1 = urllib2.urlopen(req1)
                #the_page1 = response1.read()
                decoded_info = json.loads(response1.read())
                #context['basicInfo'] = the_page1
                context['firstName'] = decoded_info['firstName']
                context['lastName'] = decoded_info['lastName']
                context['headline'] = decoded_info['headline']
                context['id'] = decoded_info['id']
                context['publicProfileUrl'] = decoded_info['publicProfileUrl']
                context['summary'] = decoded_info['summary']
                #context['educations'] = decoded_info['educations']

                context['educations'] = ""

                for rows in decoded_info['educations']['values']:
                    try:
                        rows['degree']
                    except KeyError:
                        rows['degree'] = ""

                    try:
                        rows['fieldOfStudy']
                    except KeyError:
                        rows['fieldOfStudy'] = ""

                    context['educations'] += rows['schoolName'] + ", " + rows['degree'] + ", " + rows['fieldOfStudy'] + " (" + \
                                            str(rows['startDate']['year']) + "-" + str(rows['endDate']['year']) + ")<br>\n"
                context['skills'] = ""
                for rows in decoded_info['skills']['values']:
                    context['skills'] += rows['skill']['name'] + ", "

                context['languages'] = ""
                for rows in decoded_info['languages']['values']:
                    context['languages'] += rows['language']['name'] + " "
    return render_to_response("profile.html", context, context_instance=RequestContext(request))