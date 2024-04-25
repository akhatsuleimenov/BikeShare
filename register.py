#!/usr/bin/python3

import cgi
import hashlib
import http
import sqlite3
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
    navigate = '<h3>Already registered? <a href="login.html">Log in</a></h3>'
    html_end = '</body></html>'
    return navigate + html_end

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def user_exists(email):
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Prepare SQL query to search for an email
    cursor.execute('SELECT COUNT(*) FROM users WHERE email = ?', (email,))
    
    # Fetch the result
    # This will return a tuple like (0,) if no rows, or (1,) if exists
    result = cursor.fetchone()
    
    # Close the connection to the database
    conn.close()
    
    return result[0] > 0


def register_user(email, password, first_name, last_name, age, year):
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    sql = 'INSERT INTO users (email, password, first_name, last_name, age, year) VALUES (?, ?, ?, ?, ?, ?)'
    
    # add the user info to the db
    cursor.execute(sql, (email, hash_password(password) , first_name, last_name, age, year))
    
    # Commit and close
    conn.commit()
    conn.close()


def generate_session_id():
    return str(uuid.uuid4())

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


def set_session_cookie(session_id):
    cookie = http.cookies.SimpleCookie()
    cookie['session_id'] = session_id
    cookie['session_id']['httponly'] = True
    cookie['session_id']['path'] = '/'
    
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
    age = form.getvalue("age")
    year = form.getvalue("year")

    # check if they are not empty
    if email and password:
        # if user exists navigate them to login
        if user_exists(email):
            htmlhead()
            print("<h1>You are already registered, try to login.</h1>" + htmltail())
        # else regsiter them and navigate to profile page
        else:
            register_user(email, password, first_name, last_name, age, year)
            session_id = generate_session_id()
            save_session(session_id, email)
            set_session_cookie(session_id)
    else:
        htmlhead()
        print("<h1>Email and password are required.</h1>" + htmltail())

main()