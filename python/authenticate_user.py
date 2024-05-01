#!/usr/bin/python3

import cgi
import http.cookies

import csv

import json

import os


session_csv = "../data/sessions.csv"

def is_session_valid(session_id):
    with open(session_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == session_id:
                return True
    return False

def get_session_cookie():
    if 'HTTP_COOKIE' in os.environ:
        cookie_string = os.environ['HTTP_COOKIE']
        cookie = http.cookies.SimpleCookie()
        cookie.load(cookie_string)
        if 'session_id' in cookie:
            return cookie['session_id'].value
    return None

def main():
    print("Content-Type: application/json\n")
    session_id = get_session_cookie()
    if session_id and is_session_valid(session_id):
        print(json.dumps({"isLoggedIn": True}))
    else:
        print(json.dumps({"isLoggedIn": False}))

if __name__ == "__main__":
    main()