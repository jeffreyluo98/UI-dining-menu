# UIUC Dining bot 

This is a CS125 project created by Zhili Luo (zhilil2).
Based on Weather Webhook Fulfillment Sample by DialogFlow(api.ai)

More info about Api.ai webhooks could be found here:
[Api.ai Webhook](https://docs.api.ai/docs/webhook)

# Deploy to:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# What does it do?
It is a simple AI program that can
automatically fetch the data of UI dining halls’ menu and
answer certain questions. Let’s first demonstrate its
function!

## How does it Work?
First we used DialogFlow to create natural dialogs and identify what the user wants. We send the parameters through webhook as a JSON request to our web application on Heroku. Heroku App will get this request, submit a form on the UIUC dining website, then fetch data from html and process the request. It will create an appropriate response and send it back to DialogFlow.

## License
See [LICENSE](LICENSE).

## Terms
Your use of this sample is subject to, and by using or downloading the sample files you agree to comply with, the [Google APIs Terms of Service](https://developers.google.com/terms/).

This is not an official Google product
