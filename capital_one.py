"""
Example of OAuth 2.0 process with web server.
API of facebook is used: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
"""

import webbrowser
import urllib2
import json
from urllib import urlencode
from urlparse import parse_qsl, urlparse
import random
import pprint

def return_rewards():
    PROVIDER = 'capitalone'
    # capitalone
    CLIENT_KEY = 'vgw3sf4f8nq3b98i1gdfr8wpx4gpty0ska52'
    CLIENT_SECRET = 'eb5f6rda6v0d1ld8y4fymkudo86gorrc47cj'
    CALLBACK_URL = 'http://localhost:8081/authredirect'

    AUTHORIZE_URL = 'https://api.devexhacks.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.devexhacks.com/oauth2/token'
    API_RESOURCE_URL = 'https://api.devexhacks.com/rewards/accounts'

    ##########################
    # STEP 1: user cofirmation
    ##########################

    auth_params = {
        "client_id": CLIENT_KEY,
        "redirect_uri": CALLBACK_URL,
        "scope": "read_rewards_account_info",
        "response_type": "code",
    }

    url = "?".join([AUTHORIZE_URL, urlencode(auth_params)])
    print url,'\n'
    webbrowser.open_new_tab(url)
    redirected_url = raw_input("Paste here url you were redirected:\n")
    redirect_params = dict(parse_qsl(urlparse(redirected_url).query))
    auth_code = redirect_params['code']
    print 'auth_code obtained.'
    # print "auth_code", auth_code

    ######################
    # STEP 2: access token
    ######################
    access_token_params = {
        "client_id": CLIENT_KEY,
        "redirect_uri": CALLBACK_URL,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
    }

    access_token_params['grant_type'] = 'authorization_code'
    # send POST request.
    # print urlencode(access_token_params),'\n'
    resp = urllib2.urlopen(ACCESS_TOKEN_URL, data=urlencode(access_token_params))
    assert resp.code == 200
    resp_content = json.loads(resp.read())
    access_token = resp_content['access_token']
    print 'access_token obtained.'
    # print "access_token", access_token,'\n'

    ####################################
    # STEP 3: request to server resource
    ####################################
    headers = {"Authorization":"Bearer "+access_token}
    # print url, '\n'


    try:
        #page = urllib2.urlopen(API_RESOURCE_URL,data=urlencode(headers))
        # page = urllib2.urlopen(url)

        request = urllib2.Request(API_RESOURCE_URL, None, headers)

    except urllib2.HTTPError, e:
        print 'Error'
        print e.fp.read()

    resp = urllib2.urlopen(request)
    # print resp
    assert resp.code == 200
    resp_content = json.loads(resp.read())
    # print "All params:", resp_content

    account_detail = []
    for account in resp_content['rewardsAccounts']:
        account_ref_ID = account['rewardsAccountReferenceId']

        param = account_ref_ID
        # print param
        request = urllib2.Request(API_RESOURCE_URL + "/" + param, None, headers)

        resp = urllib2.urlopen(request)
        resp_content = json.loads(resp.read())

        account_detail.append(resp_content)
        # print resp_content

    # print 'account_detail'
    return account_detail

def inqury(account_detail, i, item):
    print '\nYour', item, 'is', account_detail[i][item]
    return account_detail[i][item]

if __name__ == "__main__":
    account_detail = return_rewards()
    item = 'rewardsBalance'
    # currency = 'points'
    currency = 'miles'
    if currency == 'points':
        i = 1
    elif currency == 'miles':
        i = 0 # Miles
    balance = inqury(account_detail, i, item)
# resp_content = return_rewards()
# print resp_content['rewardsAccounts']
# http://localhost:8081/authredirect?code=8151af36a0a8478987117a960308bfb0
