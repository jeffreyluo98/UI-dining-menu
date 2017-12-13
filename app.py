# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.error import HTTPError

import json
import os
import urllib.request
import re, requests, datetime, random

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "menuRequest":
        return
    
    output = getMenu(req)
    res = makeWebhookResult(output)
    return res


def getMenu(req):
    
    result = req.get("result")
    parameters = result.get("parameters")
    date = parameters.get("date")
    diningHall = parameters.get("dining-hall")
    mealPeriod = parameters.get("meal-period")
    
    if mealPeriod == "":
            currentHour = datetime.datetime.now().hour
            if currentHour <= 10:
                mealPeriod = 'breakfast'
            elif currentHour <= 13:
                mealPeriod = 'lunch'
            elif currentHour <= 15:
                mealPeriod = 'light lunch'
            elif currentHour > 20 and date == "":
                mealPeriod = 'breakfast'
                date = str(datetime.date.today() + datetime.timedelta(days=1))
            else: mealPeriod = 'dinner'
    if date == "":
        date = str(datetime.date.today())


    dateArray = date.split('-')
    date = "/".join([dateArray[1], dateArray[2], dateArray[0]])
    print(date)

    if diningHall == 'Ikenberry':
        diningHallValue = "Don's Chophouse Serving, Gregory Drive Diner Serving, Hortensia's Serving, Penne Lane Serving, Prairie Fire Serving, Soytainly Serving, Euclid Street Deli Serving, Baked Expectations Serving, Better Burger IKE Serving, Neo Soul Serving"
    elif diningHall == 'PAR':
        diningHallValue = "Abbondante Serving, Arugula's Serving, La Avenida Serving, Panini Bar, Provolone Serving, Sky Garden Serving, Better Burger Serving"
    else:
        diningHallValue = diningHall + ' Serving'
    payload = {'pagebody_0$txtServingDate': date,
               'pagebody_0$ddlLocations': diningHallValue,
               'pagebody_0$btnSubmit': 'Select',
               '__VIEWSTATE': '/wEPDwUKMTMyMzQxOTk2Ng8WAh4TVmFsaWRhdGVSZXF1ZXN0TW9kZQIBFgICAg9kFgJmD2QWAmYPZBYCAgEQZGQWBAIFDxBkDxYGZgIBAgICAwIEAgUWBhAFC0J1c2V5LUV2YW5zBRNCdXNleS1FdmFucyBTZXJ2aW5nZxAFA0ZBUgULRkFSIFNlcnZpbmdnEAUJSWtlbmJlcnJ5BesBRG9uJ3MgQ2hvcGhvdXNlIFNlcnZpbmcsIEdyZWdvcnkgRHJpdmUgRGluZXIgU2VydmluZywgSG9ydGVuc2lhJ3MgU2VydmluZywgUGVubmUgTGFuZSBTZXJ2aW5nLCBQcmFpcmllIEZpcmUgU2VydmluZywgU295dGFpbmx5IFNlcnZpbmcsIEV1Y2xpZCBTdHJlZXQgRGVsaSBTZXJ2aW5nLCBCYWtlZCBFeHBlY3RhdGlvbnMgU2VydmluZywgQmV0dGVyIEJ1cmdlciBJS0UgU2VydmluZywgTmVvIFNvdWwgU2VydmluZ2cQBQNJU1IFC0lTUiBTZXJ2aW5nZxAFA0xBUgULTEFSIFNlcnZpbmdnEAUDUEFSBYMBQWJib25kYW50ZSBTZXJ2aW5nLCBBcnVndWxhJ3MgU2VydmluZywgTGEgQXZlbmlkYSBTZXJ2aW5nLCBQYW5pbmkgQmFyLCBQcm92b2xvbmUgU2VydmluZywgU2t5IEdhcmRlbiBTZXJ2aW5nLCBCZXR0ZXIgQnVyZ2VyIFNlcnZpbmdnZGQCCw9kFgJmD2QWAmYPZBYCAgEPFgIeC18hSXRlbUNvdW50AgkWEmYPZBYCZg8VAyovL3d3dy5ob3VzaW5nLmlsbGlub2lzLmVkdS9Ub29scy9NeUhvdXNpbmcGb3JhbmdlCU1ZSE9VU0lOR2QCAQ9kFgJmDxUDOC8vd3d3LmhvdXNpbmcuaWxsaW5vaXMuZWR1L0Fib3V0VXMvc3RhZmYtZW1wbG95bWVudC9Kb2JzBGJsdWUESk9CU2QCAg9kFgJmDxUDPS8vd3d3LmhvdXNpbmcuaWxsaW5vaXMuZWR1L1Jlc291cmNlcy9yZXNpZGVuY2UtaGFsbC1saWJyYXJpZXMGeWVsbG93CUxJQlJBUklFU2QCAw9kFgJmDxUDLy8vd3d3LmhvdXNpbmcuaWxsaW5vaXMuZWR1L1Jlc291cmNlcy9UZWNobm9sb2d5BWdyZWVuClRFQ0hOT0xPR1lkAgQPZBYCZg8VAyYvL3d3dy5ob3VzaW5nLmlsbGlub2lzLmVkdS9tYWludGVuYW5jZQZwdXJwbGULTUFJTlRFTkFOQ0VkAgUPZBYCZg8VAyxodHRwczovL3dlYi5ob3VzaW5nLmlsbGlub2lzLmVkdS9NeUJhbGFuY2VzLwNyZWQLSUxMSU5JIENBU0hkAgYPZBYCZg8VAzEvL3d3dy5ob3VzaW5nLmlsbGlub2lzLmVkdS9SZXNvdXJjZXMvR2V0LUludm9sdmVkCmxpZ2h0LWJsdWUMR0VUIElOVk9MVkVEZAIHD2QWAmYPFQMoLy93d3cuaG91c2luZy5pbGxpbm9pcy5lZHUvVG9vbHMvbW92ZS1pbgtsaWdodC1ncmVlbgdNT1ZFLUlOZAIID2QWAmYPFQMkLy93d3cuaG91c2luZy5pbGxpbm9pcy5lZHUvYXBwbHktbm93CWRhcmstYmx1ZQlBcHBseSBOb3dkZM4Nfyq3wnFCV5FSr3SK1LwFjXv0zIrtghi3tNeHp6Em',
               '__VIEWSTATEGENERATOR': '6C13C3D4',
               '__EVENTVALIDATION': '/wEdAAndPAajAdsmwoOZ/gfzhOZ0WSHE2RXo8/7qyel4z+uwDmS/tYTfV6F4P9ytm+uBq3Oh9DmNqfhtvp0A+P2a1qVCeMEESUkmlwAnmRGbejy/kVSnCSYCDKMPW6tER5EH5YTU/RMGCO28nRolFRITlJPZ7+Uf8k9kfSWslLyENoaAtZw6htKKHrAZ0Z/A8f+XAckjJ/hf3kan4/T6O8WK/46pAJZsdE5yecCiz5zRwcmDrw=='
                }
    url = 'http://www.housing.illinois.edu/dining/menus/dining-Halls'
    r = requests.post(url, data=payload)
    web_data = r.text

    ret = []
    filter_str = r'<h4.*?diningmealperiod">(.*?) - (.*?)</h4>.*?<strong>Entrees</strong>(.*?)<br />.*?'

    pattern = re.compile(filter_str, re.DOTALL)
    items = re.findall(pattern, web_data)
    menu = []
    for item in items:
        this_meal_period = item[0].lower()
        if this_meal_period == 'brunch':
            this_meal_period = 'lunch'
        elif this_meal_period == 'specialty dinner':
            this_meal_period = 'dinner'
        entrees = " ".join(item[2].split())
        entrees = re.split(r"\s,\s*", entrees)
        if this_meal_period == mealPeriod:
            menu += entrees
    return [diningHall, menu]


def makeWebhookResult(output):
    diningHall = output[0]
    menu = output[1]
    if len(menu) > 8:
        speechMenu = ", ".join(random.sample(set(menu), 8))
    else:
        speechMenu = ", ".join(menu)
    menu = ", ".join(menu)

    respArray = []
    respArray += [diningHall + ' is serving ']
    respArray += ['Entrees served at ' + diningHall + " include "]
    respArray += ['On ' + diningHall + "'s menu, there is "]
    resp = respArray[random.randint(0, 2)]

    speech = resp + speechMenu + "."
    displayText = resp + menu + "."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": displayText,
        # "data": data,
        # "contextOut": [],
        "source": "ui-dining"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
