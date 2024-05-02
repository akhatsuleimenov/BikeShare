#!/usr/bin/python3

import cgi

import cgi
import http.cookies
import csv
import os
import sys


# USE ABSOLUTE PATH FOR LOCAL DEVELOPMENT
session_csv = "../data/sessions.csv"


def delete_session_from_csv(session_id):
    """Remove a session ID from the sessions CSV."""
    try:
        with open(session_csv, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = [row for row in reader if row[0] != session_id]
        with open(session_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return True
    except Exception as e:
        print("Failed to access or modify the sessions.csv file:", e, file=sys.stderr)
        return False

def get_session_cookie():
    """Retrieve the session ID from the cookie."""
    cookie_string = os.environ.get('HTTP_COOKIE')
    if not cookie_string:
        return None
    cookie = http.cookies.SimpleCookie()
    cookie.load(cookie_string)
    try:
        return cookie['session_id'].value
    except KeyError:
        return None

def clear_session_cookie():
    """Clear the session cookie."""
    print("Set-Cookie: session_id=; Path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT")

def main():
    print("Content-Type: text/html")  # HTTP header
    session_id = get_session_cookie()
    if session_id and delete_session_from_csv(session_id):
        clear_session_cookie()
        # Redirect immediately to the login page
        print("Location: ../BikeShare/login.html")
        print()  # End of headers
    else:
        # If the user is not logged in, show an error message
        print()
        print("<html><body><p>Error: You are not logged in.</p></body></html>")

if __name__== "__main__":
    main()
