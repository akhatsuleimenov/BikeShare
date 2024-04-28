#!/usr/bin/python3

import cgi
import http.cookies as Cookie
import os

# Path to the reservations file
reservations_file = "reservations.txt"

def html_response(message):
    print("Content-Type: text/html\n")
    print(f"<html><body>{message}</body></html>")

def check_user_logged_in():
    if 'HTTP_COOKIE' in os.environ:
        cookie_string = os.environ.get('HTTP_COOKIE')
        cookie = Cookie.SimpleCookie()
        cookie.load(cookie_string)
        
        if 'session_id' in cookie:
            return cookie['session_id'].value
    return None

def get_user_details(session_id):
    """ This function would fetch user details from a file based on the session_id.
        Assuming user details are stored in a file like 'user_sessions.txt'
        Format: session_id, user_id, email
    """
    try:
        with open("user_sessions.txt", "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if parts[0] == session_id:
                    return parts[1:]  # Returns user_id, email
        return None
    except FileNotFoundError:
        return None

def store_reservation(user_details, bike_type, date, time_slot):
    with open(reservations_file, "a") as file:
        file.write(f"{user_details[0]}, {user_details[1]}, {bike_type}, {date}, {time_slot}\n")

def main():
    form = cgi.FieldStorage()
    bike_type = form.getvalue('bikeType')
    date = form.getvalue('date')
    time_slot = form.getvalue('timeSlot')
    
    session_id = check_user_logged_in()
    user_details = get_user_details(session_id) if session_id else None
    
    if user_details:
        store_reservation(user_details, bike_type, date, time_slot)
        html_response("Your reservation has been successfully submitted.")
    else:
        html_response("You are not logged in. Please log in to make a reservation.")

if __name__ == "__main__":
    main()
