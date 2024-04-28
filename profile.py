#!/usr/bin/python3

import csv
from http.cookies import SimpleCookie
import os
import sys


users_csv = "users.csv" # USE ABSOLUTE PATH FOR LOCAL DEVELOPMENT
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
    html_end = '</body></html>'
    return html_end 

def get_user_info(email):
    with open(users_csv, mode='r', newline='') as file:
        reader = csv.DictReader(file, fieldnames=['first_name', 'last_name', 'email', 'hashed_password', 'year'])
        for row in reader:
            if row['email'] == email:
                return row
    return None


# ASSUME THIS WORKS
def get_session_id_from_cookie():
    if 'HTTP_COOKIE' in os.environ:
        cookie_string = os.environ['HTTP_COOKIE']
        cookie = SimpleCookie()
        cookie.load(cookie_string)
        if 'session_id' in cookie:
            return cookie['session_id'].value
    return None

def get_email_from_session(session_id):
    with open(session_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == session_id:
                return row[1]
    return None



def main():
    htmlhead()
    
    # session_id = get_session_id_from_cookie()
    session_id = "52fd8fa3-7bf8-44e6-9767-486d5ae6f2cc"
    if session_id:
        sys.stderr.write(os.path.dirname(os.path.abspath(__file__)))
        email = get_email_from_session(session_id)
        if email:
            user_info = get_user_info(email)
            if user_info:
                print(f"<h1>Welcome, {user_info['first_name']} {user_info['last_name']}</h1>")
                print(f"<p>Email: {user_info['email']}</p>")
                print(f"<p>Year: {user_info['year']}</p>")
            else:
                print("<h1>User information not found.</h1>")
        else:
            print("<h1>No user associated with this session.</h1>")
    else:
        print('<h1>No valid session found. Please <a href="../login.html">Log in</a>.</h1>')
    
    htmltail()

main()

# type: ignore