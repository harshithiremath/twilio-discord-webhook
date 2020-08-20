from flask import Flask, request
import requests
from DiscordWHUrl import retWHUrl
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


msgObject = {'username': "Twilio Whatsapp WebHook"}
# the dict object used by the fetch api in the discord wh

wh_url = retWHUrl()
# the WebHook URL for your server. I haven't pushed this file to GitHub, due to obvious security reasons


@app.route("/")
# the default route of the Flask server
def hello():
    return "Hey world!"


@app.route("/sms", methods=['POST'])
def sms_reply():
    # msg now contains the message sent by the User to Twilio Whatsapp
    msg = request.form.get('Body')
    # set 'content' for the payload of the Discord POST request
    msgObject["content"] = msg
    resp = MessagingResponse()
    r = requests.post(wh_url, json=msgObject)
    if r.ok:
        resp.message(
            "Sent the following message to your server : \n{}".format(msg))
    else:
        resp.message("Your message didn't get sent!")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
