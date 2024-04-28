#!/usr/bin/python3

import cgi
import csv
import hashlib
import http.cookies

import uuid

# USE ABSOLUTE PATH FOR LOCAL DEVELOPMENT
users_csv = "users.csv"
session_csv = "sessions.csv"

def htmlhead():
    print("Content-Type: text/html \n\n")
    print('''

	<!DOCTYPE html>
	<html>
	<head>
	<title> Registration </title>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link href='style.css' rel='stylesheet'>

	</head>
	<body>
	''')

def htmltail():
    navigate = "<h3>Don't have an account?  <a href='../registration.html'>Register</a></h3>"
    html_end = "</body></html>"
    return navigate + html_end


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
    cookie = http.cookies.SimpleCookie()
    cookie['session_id'] = session_id
    cookie['session_id']['httponly'] = True
    cookie['session_id']['path'] = '/'
    
    # ASSUME THAT THIS WORKS
    # send cookie id and navigate to next page
    print(cookie.output())
    # print("Content-type: text/html\n")
    # print("Location: ./profile.py\n\n")


def main():
    # Set HTTP header
    print("Content-Type: application/json")
    print()  # End of headers

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
            set_session_cookie(session_id)
            print(json.dumps({"success": True, "message": "Login successful"}))
        else:
            # Send a JSON response
            print(json.dumps({"success": False, "message": "Username and password are incorrect. Please try again."}))
    else:
        # Send a JSON response
        print(json.dumps({"success": False, "message": "Email and password are required."}))

if __name__ == "__main__":
    main()