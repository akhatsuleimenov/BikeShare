#!/usr/bin/python3

import cgi
import hashlib
import os
import sqlite3
import http.cookies
import uuid

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
    navigate = "<h3>Don't have an account?  <a href='registration.html'>Register</a></h3>"
    html_end = "</body></html>"
    return navigate + html_end


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Prepare SQL query to find the user by email and hashed password
    cursor.execute('SELECT id, name FROM users WHERE email = ? AND password = ?', (email, hash_password(password)))

    # Fetch the result
    user = cursor.fetchone()

    # Close the connection to the database
    conn.close()

    return True if user else None

def generate_session_id():
    return str(uuid.uuid4())

def set_session_cookie(session_id):
    cookie = http.cookies.SimpleCookie()
    cookie['session_id'] = session_id
    cookie['session_id']['httponly'] = True
    cookie['session_id']['path'] = '/'
    
    # send cookie id and navigate to next page
    print(cookie.output())
    print("Content-type: text/html\n")
    print("Location: ./profile.py\n\n")


def save_session(session_id, email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # First, retrieve the user_id from the users table using the email
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    
    # If the user exists, proceed to save the session
    if result:
        cursor.execute('INSERT INTO sessions (session_id, user_id) VALUES (?, ?)', (session_id, result[0]))
        conn.commit()
    else:
        print("No user found with that email")
    conn.close()


def main():
    # get values from the form
    form = cgi.FieldStorage()
    email = form.getvalue("email")
    password = form.getvalue("password")

    # check if they are not empty
    if email and password:
        # if details correct them direct to profile page
        if authenticate_user(email, password):
            session_id = generate_session_id()
            save_session(session_id, email)
            set_session_cookie(session_id)
        # else navigate to register page
        else:
            htmlhead()
            print("<h1>Username and password are incorrect, try to register?</h1>" + htmltail())
    else:
        htmlhead()
        print("<h1>Email and password are required.</h1>" + htmltail())

main()