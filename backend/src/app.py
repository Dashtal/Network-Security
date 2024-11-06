#!/usr/bin/env python3

import os
import sys
import time
from flask import Flask, make_response, jsonify, request # type: ignore
from functools import wraps
from threading import Thread

BACKEND_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BACKEND_PATH)
from utils.mail import send_email

def cors_headers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    return decorated_function

app = Flask(__name__)

EMAILS = BACKEND_PATH + '/data/emails.txt'
SEND_MAILS_TIMEOUT_MINUTES = 5/60


# -------------------------------------------------- ENDPOINTS --------------------------------------------------

@app.route('/petition', methods=['POST', 'OPTIONS'])
@cors_headers
def save_user():
    if request.method == 'OPTIONS':
        return '', 200

    email = request.data.decode('utf-8')

    create_data_file_if_not_exists()
    with open(EMAILS, 'a') as f:
        f.write(email + '\n')

    return jsonify({"message": "Email saved successfully"}), 200


# -------------------------------------------------- UTILS --------------------------------------------------

def create_data_file_if_not_exists():
    if not os.path.exists(EMAILS):
        with open(EMAILS, 'w') as f:
            pass  # Just create the file if it doesn't exist


def emails_loop():
    while True:
        if os.path.exists(EMAILS):
            with open(EMAILS, 'r') as f:
                emails = [email.strip() for email in f.readlines()]

            for email in emails:
                send_email(email)

            open(EMAILS, 'w').close() # Clear mails to prevent sending to the same person again

        time.sleep(SEND_MAILS_TIMEOUT_MINUTES * 60)


def emails_thread():
    email_thread = Thread(target=emails_loop)
    email_thread.daemon = True  # Ensures the thread will exit when the main program exits
    email_thread.start()


# -------------------------------------------------- ENTRYPOINT --------------------------------------------------

if __name__ == '__main__':
    emails_thread()
    app.run(debug=True, port=5001)
