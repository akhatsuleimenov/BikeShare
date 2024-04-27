#!/usr/bin/python3

import cgi

import hashlib

import os

import sqlite3

import http.cookies

import uuid

import json


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
    # print("Content-type: text/html\n")
    # print("Location: ./profile.py\n\n")


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
            save_session(session_id, email)
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