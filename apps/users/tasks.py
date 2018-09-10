from restfuldemo.celery import app
import traceback,os
from utils.gitlab_api import gl
from django.core.mail import send_mail


@app.task(name="create_gitlab_user")
def useradd(username, password, email, name):
   try:
       res = gl.users.create(
           {'username': username, 'password': password,
            'email': email,'name': name})
       print(res)
   except:
        print('fail')
        traceback.print_exc()


@app.task(name="sendmail")
def mail(title, contents, email_from, email_to):
    try:
        send_mail(title, contents, email_from, email_to)
    except:
        print('fail')
        traceback.print_exc()


@app.task(name="touchfile")
def touchfile():
    os.mkdir("/tmp/abc")
