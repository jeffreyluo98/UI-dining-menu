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
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import re

import json
import os

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
        return {}
    res = makeWebhookResult(data)
    return res
    
    url = "http://housing.illinois.edu/Dining/Menus/Dining-Halls"
    request = urllib.request.Request(url)
    ret = []
    retTxt = []
    stri = r'<h4.*?diningmealperiod">(.*?) - (.*?)</h4>.*?<strong>(.*?)</strong>(.*?)<br />.*?'
    response = urllib.request.urlopen(request)
    webData = response.read()
    webData = webData.decode('utf-8')

    pattern = re.compile(stri, re.DOTALL)
    items = re.findall(pattern, webData)
    for item in items:
        mealPeriod = item[0].lower()

        dateArray = item[1].split('/')
        date = "-".join([dateArray[2], dateArray[0], dateArray[1]])
        cat = item[2]
        menu = " ".join(item[3].split())
        ret.append([date, mealPeriod, cat, menu])

    data = ""
    #for one in ret:
    #    if one[1] == "lunch" and one[2] == "Entrees":
    #        data += one[3] + ". "
    


#def getParameters(req):
#    result = req.get("result")
#    parameters = result.get("parameters")
#    date = parameters.get("date")
#    diningHall = parameters.get("dining-hall")
#    mealPeriod = parameters.get("meal-period")
    #if city is None:
    #   return None

#    return diningHall


def makeWebhookResult(data):

    diningHall = "Ikenberry"
    entrees = "Polenta with Roasted Vegetables , Macaroni & Cheeze"
    
    speech = diningHall + " is serving " + entrees

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "ui-dining"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
