from flask import Flask, request
import requests
from DiscordBotToken import retWHUrl
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# the dict object used by the fetch api in the discord wh
msgObject = {'username': "Twilio Whatsapp WebHook"}
wh_url = retWHUrl()


@app.route("/")
def hello():
    return "Hey world!"


@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    msgObject["content"] = msg
    resp = MessagingResponse()
    # resp.message("Guess you said: {}".format(msg))
    r = requests.post(wh_url, json=msgObject)
    if r.ok:
        resp.message(
            "Sent the follwoing message to your server : \n{}".format(msg))
    else:
        resp.message("Your message didn't get sent!")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
