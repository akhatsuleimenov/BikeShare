#!/usr/bin/python3

import cgi
import hashlib

filename = "users.txt"

def htmlhead():
    print("Content-Type: text/html \n\n")
    print('''

	<!DOCTYPE html>
	<html>
	<head>
	<title> Registration </title>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link href='styles.css' rel='stylesheet'>

	</head>
	<body>
	''')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(email):
    with open(filename, "r") as file:
        for line in file:
            stored_email, _ = line.strip().split(":")
            if stored_email == email:
                return True
    return False

def register_user(email, hashed_password):
    with open(filename, "a") as file:
        file.write(f"{email}:{hashed_password}\n")
    return True

def authenticate(email, hashed_password):
    with open(filename, "r") as file:
        for line in file:
            stored_email, stored_password = line.strip().split(":")
            if stored_email == email and stored_password == hashed_password:
                return True
    return False

form = cgi.FieldStorage()
email = form.getvalue("email")
password = form.getvalue("password")
action = form.getvalue("action")

go_back_button = '<button onclick="window.history.back();">Go Back</button>'
html_end = "</body></html>"



if email and password:
    hashed_password = hash_password(password)
    if action == "Register":
        if user_exists(email):
            htmlhead()
            print("<h1>You are already registered, try to login.</h1>" + go_back_button + html_end)
        else:
            register_user(email, hashed_password)
            print("Location: ./profile.html\n\n")
    elif action == "Login":
        if authenticate(email, hashed_password):
            print("Location: ./profile.html\n\n")
        else:
            htmlhead()
            print("<h1>User doesn't exist, try to register.</h1>" + go_back_button  + html_end)
else:
    htmlhead()
    print("<h1>Email and password are required.</h1>" + go_back_button + html_end)
