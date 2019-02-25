from flask import Flask, render_template, request, redirect, make_response
import os
import requests
from flask_mail import Mail
from flask_mail import Message
from pcPartPicker import pcPartPicker;

app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'andromedacomputersltd@gmail.com',
    MAIL_PASSWORD = 'Andromeda123',
))

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def my_form_size():
    n = str(request.form['name'])
    e = str(request.form['email'])
    l = str(request.form['link'])

    ppp = pcPartPicker()
    val = ppp.parseLink(l);

    msg = Message("Dear " + n + ",\nAndromeda Enterprises: PC Build Confirmation", sender="andromedacomputersltd@gmail.com", recipients=[e])
    msg.add_recipient("andromedacomputersltd@gmail.com")
    bodytext = "Thank you for contacting Andromeda Enterprises. One of our representatives will contact you shortly."

    if(not (val == 'N/A')):
        bodytext = bodytext + " Here is the PC Build we will review:\n\n" + val.replace('<br>', '\n')
    msg.body = bodytext;
    mail.send(msg)
    return render_template('form.html', name = n, email = e, build = val)


if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
