import json, xmltodict, requests
from slugify import slugify


class SMS:
    """SMS API Consuming of Mobildev
        Api Info Address : http://www.mobildev.com/kutuphane.asp?sid=127
        Api Consuming Adress : http://8bit.mobilus.net/
        Consuming Type : XML
        Error Status :
            01 = Invalid Cred.
            02 = No credit
            10 = Cant send
    """

    def __init__(self):
        self.apiurl = "http://gateway.mobilus.net/com.mobilus"
        self.username = "yourusername"
        self.companycode = "yourcompanycode"
        self.password = "yourpassword"
        self.originator = "youroriginator"
        self.charlimit = 152  # This is default char limit for messages
        self.multimessagecode = "40"  # This is for sending messages to many
        self.amessagecode = "0"

    def sendrequest(self, url, data):
        print(data)
        headers = {'Content-Type': 'application/xml'}

        if type(data) != 'bytes':
            data = bytes(data, 'utf-8')

        result = requests.post(url, data, headers=headers).text
        return result

    def checkuser(self):
        usercheckxml = "<MainReportRoot><UserName>" + self.username + "-" + self.companycode + "</UserName><PassWord>" + self.password + "</PassWord><Action>4</Action></MainReportRoot>"
        print(usercheckxml)
        response = self.sendrequest(self.apiurl, usercheckxml)
        if response == "01" or response == 1:
            print('invalid username password')
        elif response == "02" or response == 2:
            print('No credit')
        elif response == "10" or response == 10:
            print('CantSend')
        else:
            print(response)  # Add a logging system for tracing errors for all site.
        return response

    def sendsms(self, message, numbers):

        # Get Numbers with array and join with comma
        if len(message) > self.charlimit:
            action = self.multimessagecode
        else:
            action = self.amessagecode

        message = slugify(message)

        preparednumbers = "5555555555"
        sendsmsxml = "<MainmsgBody><UserName>" + self.username + "-" + self.companycode + "</UserName><PassWord>" + self.password + "</PassWord><Action>" + action + "</Action>"
        sendsmsxml += "<Mesgbody>" + message + "</Mesgbody>"
        sendsmsxml += "<Numbers>" + preparednumbers + "</Numbers>"
        sendsmsxml += "<Originator>" + self.originator + "</Originator>"
        sendsmsxml += "<SDate></SDate>"
        sendsmsxml += "</MainmsgBody>"
        response = self.sendrequest(self.apiurl, sendsmsxml)
        return response
