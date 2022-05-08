from flask import Flask 
from flask import render_template, request, redirect, url_for, flash
from ipaddress import IPv4Address  # for your IP address
from pyairmore.request import AirmoreSession  # to create an AirmoreSession
from pyairmore.services.messaging import MessagingService  # to send messages
# from openpyxl import load_workbook
import time
import os

app = Flask(__name__)

#a path should be provided here:
app.config["FILE_UPLOADS"] = str(r"C:\Users\hp\OneDrive\Desktop\Final SMS send\upload")
app.secret_key = os.urandom(12)
ALLOWED_EXTS = {"txt", "csv", "xlsc"}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/connect', methods = ['GET',  'POST'])
def connect():
    if request.method == 'POST':
        ip_address = request.form['ip']
        ip = IPv4Address(ip_address)  # let's create an IP address object
        # now create a session
        session = AirmoreSession(ip)
        # if your port is not 2333
        # session = AirmoreSession(ip, 2334)  # assuming it is 2334

        was_accepted = session.request_authorization()
        if was_accepted:
            flash("Connected Successfully!")
            service = MessagingService(session)
            def sendSms(telephone, message):
                service.send_message(telephone, message)

            return render_template("index.html"), ip_address
        else:
            flash("Please open your airmore app on your mobile.")
            return "Not connected!"
    else:
        render_template('index.html')

@app.route('/send', methods = ['GET','POST'])
def send():
    print(request.files)
    if request.method == 'POST':
        print("It's me!!")
        path = r'C:\Users\hp\OneDrive\Desktop\Final SMS send\upload\sms.txt'
        print(path)


        fh = open(path,'r')
        topic = request.form["topic"]
        meet = request.form["meetLink"]
        when = request.form["time"]
        aspace = request.form["aspace"]
        sign = request.form["sign"]
        message = str(request.form["message"]) + "\n" + str(topic) + "\nTime: "+str(when)+"\nmeet: "+str(meet) +"\n"+ str(sign) + "\n" + str(aspace)

        print(message)

        if not str(topic) or not str(meet) or not str(time) or not str(message) or not str(sign):
            return "failure"
        
        else:
            txtfh = fh.read()
            uniqlist = []
            ip_address = request.form['ip']
            print(ip_address)
            ip = IPv4Address(ip_address)
            print(ip)
            session = AirmoreSession(ip)
            service = MessagingService(session)
            def sendSms(telephone, message):
                 return service.send_message(telephone, message)
            def namesep(firstName):
                return firstName.split(" ")[0]

            def format(phone):
                cln = phone.replace(" ","").replace("-","")
                if (cln.startswith("251")):
                    return "+"+cln
                elif (cln.startswith("9")):
                    return "0"+cln
                else:
                    return cln
            for i in txtfh.split('\n'):
                if i in uniqlist:
                    pass
                else:
                    uniqlist.append(namesep(i.split(",")[0])+","+format(i.split(",")[-1]))
            
            for i in uniqlist:
                msg = "Hi "+i.split(",")[0]+",\n"+message
                number = str(i.split(",")[1])
                content = "Send to: " + i
                sendSms(number,msg)
                time.sleep(1)

            flash("Congratulations! You sent an invitation.")
            return render_template("success.html", content = content)
    else:
        render_template('index.html')



if __name__ == "__main__":
    app.run(debug = True) 
