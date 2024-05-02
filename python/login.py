#!/usr/bin/python3

import cgi
import json

import csv
import hashlib
import http.cookies

import uuid

# USE ABSOLUTE PATH FOR LOCAL DEVELOPMENT
users_csv = "../data/users.csv"
session_csv = "../data/sessions.csv"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    with open(users_csv, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[2] == email and row[3] == hash_password(password):
                return True
    return False

def generate_session_id():
    return str(uuid.uuid4())

def save_session_to_csv(session_id, email):
    with open(session_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([session_id, email])

def set_session_cookie(session_id):
    """Print the HTTP header to set a session cookie."""
    cookie = http.cookies.SimpleCookie()
    cookie['session_id'] = session_id
    # cookie['session_id']['httponly'] = True
    cookie['session_id']['path'] = '/'
    print(cookie.output())
    return True


def main():
    # get values from the form
    form = cgi.FieldStorage()
    email = form.getvalue("email")
    password = form.getvalue("password")

    # check if they are not empty
    if email and password:
        # if details correct then direct to profile page
        if authenticate_user(email, password):
            session_id = generate_session_id()
            save_session_to_csv(session_id, email)
            cookie_header = set_session_cookie(session_id)
            if cookie_header:
                print("Content-Type: application/json")
                print()  # End of headers
                print(json.dumps({"success": True, "message": "set cookie."}))
            else:
                print("Content-Type: application/json")
                print()  # End of headers
                print(json.dumps({"success": False, "message": "Error in setting cookie!"}))

        else:
            # Set HTTP header
            print("Content-Type: application/json")
            print()  # End of headers
            # Send a JSON response
            print(json.dumps({"success": False, "message": "Username and password are incorrect. Please try again."}))
    else:
        # Set HTTP header
        print("Content-Type: application/json")
        print()  # End of headers
        # Send a JSON response
        print(json.dumps({"success": False, "message": "Email and password are required."}))

if __name__ == "__main__":
    main()