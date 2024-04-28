#!/usr/bin/python3

import cgi
import csv

from http.cookies import SimpleCookie

import os

import json

# Path to the reservations file
reservations_file = "reservations.txt"
users_csv = "users.csv"
session_csv = "sessions.csv"


def get_session_id_from_cookie():
    """Retrieve session ID from HTTP cookie."""
    if 'HTTP_COOKIE' in os.environ:
        cookie_string = os.environ['HTTP_COOKIE']
        cookie = SimpleCookie()
        cookie.load(cookie_string)
        if 'session_id' in cookie:
            return cookie['session_id'].value
    return None

def get_email_from_session(session_id):
    """Get user email from session using session ID."""
    with open(session_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == session_id:
                return row[1]
    return None

def get_user_info(email):
    """Retrieve user details from users CSV based on email."""
    with open(users_csv, mode='r', newline='') as file:
        reader = csv.DictReader(file, fieldnames=['first_name', 'last_name', 'email', 'hashed_password', 'year'])
        for row in reader:
            if row['email'] == email:
                return row
    return None

def store_reservation(user_details, bike_type, date, time_slot):
    full_name = f"{user_details['first_name']} {user_details['last_name']}"
    email = user_details['email']
    
    with open(reservations_file, "a") as file:
        file.write(f"{full_name}, {email}, {bike_type}, {date}, {time_slot}\n")

def main():
    form = cgi.FieldStorage()
    bike_type = form.getvalue('bikeType')
    date = form.getvalue('date')
    time_slot = form.getvalue('timeSlot')
    
    session_id = get_session_id_from_cookie()
    if session_id:
        email = get_email_from_session(session_id)
        if email:
            user_details = get_user_info(email)
            if user_details:
                store_reservation(user_details, bike_type, date, time_slot)
                print("Content-Type: application/json")
                print()  # End of headers
                print(json.dumps({"success": True, "message": "Your reservation has been successfully submitted"}))

            else:
                print("Content-Type: application/json")
                print()  # End of headers
                print(json.dumps({"success": False, "message": "No user details found. Please check your registration."}))
        else:
            print("Content-Type: application/json")
            print()  # End of headers
            print(json.dumps({"success": False, "message": "Session not linked to a valid user"}))
    else:
        print("Content-Type: application/json")
        print()  # End of headers
        print(json.dumps({"success": False, "message": "You are not logged in. Please log in to make a reservation."}))

if __name__ == "__main__":
    main()