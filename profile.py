#!/usr/bin/python3

import http
import os
import sqlite3


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
	<link href='style.css' rel='stylesheet'>

	</head>
	<body>
	''')

def htmltail():
    html_end = '</body></html>'
    return html_end 

def get_user_info(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email, first_name, last_name, age, year FROM users WHERE id = ?', (user_id,))
    user_info = cursor.fetchone()
    conn.close()
    return user_info


def get_session_id_from_cookie():
    # Check if any cookies are present
    if 'HTTP_COOKIE' in os.environ:
        cookie_string = os.environ['HTTP_COOKIE']
        cookie = http.cookies.SimpleCookie()
        cookie.load(cookie_string)
        if 'session_id' in cookie:
            return cookie['session_id'].value
    return None

def get_user_id_from_session(session_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM sessions WHERE session_id = ?', (session_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None



def main():
    htmlhead()
    
    session_id = get_session_id_from_cookie()
    if session_id:
        user_id = get_user_id_from_session(session_id)
        if user_id:
            user_info = get_user_info(user_id)
            if user_info:
                print(f"""
                    <h1>{user_info[1]}'s Profile</h1>
                    <p>Email: {user_info[0]}</p>
                    <p>Age: {user_info[3]}</p>
                    <p>Year: {user_info[4]}</p>
                """)
            else:
                print("""<h1>No user info stored in the database</h1>""")
        else:
            print("""<h1>No user_id info stored in the database</h1>""")
    else:
        print("""<h1>No session_id info stored in the cookie</h1>""")
    
    htmltail()

main()

# type: ignore