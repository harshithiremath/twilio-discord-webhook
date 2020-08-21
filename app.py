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
    msgFromWhatsapp = request.form.get('Body')

    if msgFromWhatsapp.strip().split()[0].lower() == 'corona':
        resp = MessagingResponse()
        flagOrState = msgFromWhatsapp.strip().split()[1]
        if flagOrState == "--help":
            resp.message(
                "Called Help. \nYou can get the Covid Cases stats of Indian states by texting\n ```corona <state_name>``` \nFor example, send \n ```corona karnataka``` to get the Covid-19 cases stats of Karnataka State of India.")
        else:
            try:
                resFromApi = requests.get(
                    "https://api.covid19india.org/state_district_wise.json")
                resFromApi = resFromApi.json()
                confirm, deceased, recovered, delcon, deldec, delrec = 0, 0, 0, 0, 0, 0
                flagOrState = flagOrState.lower().capitalize()
                for i in resFromApi[flagOrState]["districtData"]:
                    confirm = confirm + \
                        resFromApi[flagOrState]["districtData"][i]["confirmed"]
                    deceased = deceased + \
                        resFromApi[flagOrState]["districtData"][i]["deceased"]
                    recovered = recovered + \
                        resFromApi[flagOrState]["districtData"][i]["recovered"]
                    delrec = delrec + \
                        resFromApi[flagOrState]["districtData"][i]["delta"]["recovered"]
                    delcon = delcon + \
                        resFromApi[flagOrState]["districtData"][i]["delta"]["confirmed"]
                    deldec = deldec + \
                        resFromApi[flagOrState]["districtData"][i]["delta"]["deceased"]

                resp.message("*"+flagOrState + "*\n\n  Confirmed: " + str(confirm) + " \n  Recovered: " + str(recovered) + "  \n  Deceased: " + str(deceased) + "  \n\nDaily change: \n\n Confirmed: " + (str(delcon)
                                                                                                                                                                                                          if delcon != 0 else "Not updated yet") + "\n  Recovered: " + (str(delrec) if delrec != 0 else "Not updated yet") + " \n  Deceased: " + (str(deldec) if deldec != 0 else "Not updated yet"))
                # resp.message("Probably too long")
            except:
                resp.message("Please enter the state name correctly.")
    else:
        # set 'content' for the payload of the Discord POST request
        msgObject["content"] = msgFromWhatsapp
        resp = MessagingResponse()
        r = requests.post(wh_url, json=msgObject)
        if r.ok:
            resp.message(
                "Sent the following message to your server : \n{}".format(msgFromWhatsapp))
        else:
            resp.message("Your message didn't get sent!")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
