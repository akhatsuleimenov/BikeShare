#!/usr/bin/python3

import cgi
import csv
import hashlib
from http.cookies import SimpleCookie
import os
import uuid

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
	<link href='../style.css' rel='stylesheet'>

	</head>
	<body>
	''')

def htmltail():
    navigate = '<h3>Already registered? <a href="../login.html">Log in</a></h3>'
    html_end = '</body></html>'
    return navigate + html_end

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(email):
    if not os.path.isfile(users_csv):
        return False
    with open(users_csv, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[2] == email:
                return True
    return False


def register_user(first_name, last_name, email, password, year):
    user_info = [first_name, last_name, email, hash_password(password), year]

    # Open your CSV file in append mode
    with open(users_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_info)

def generate_session_id():
    return str(uuid.uuid4())

def save_session_to_csv(session_id, email):
    with open(session_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([session_id, email])

def set_session_cookie(session_id):
    cookie = SimpleCookie()
    cookie['session_id'] = session_id
    cookie['session_id']['httponly'] = True
    cookie['session_id']['path'] = '/'


    # ASSUME THAT THIS WORKS    
    # send cookie id and navigate to next page
    print(cookie.output())
    print("Content-type: text/html\n")
    print("Location: ./profile.py\n\n")


def main():
    # get values from the form
    form = cgi.FieldStorage()
    email = form.getvalue("email")
    password = form.getvalue("password")
    first_name = form.getvalue("first_name")
    last_name = form.getvalue("last_name")
    year = form.getvalue("year")

    # check if they are not empty
    if email and password:
        # if user exists navigate them to login
        if user_exists(email):
            htmlhead()
            print("<h1>You are already registered, try to login.</h1>" + htmltail())
        # else regsiter them and navigate to profile page
        else:
            register_user(first_name, last_name, email, password, year)
            session_id = generate_session_id()
            save_session_to_csv(session_id, email)
            set_session_cookie(session_id)
    else:
        htmlhead()
        print("<h1>Email and password are required.</h1>" + htmltail())

main()