#!/usr/bin/python3


import cgi

import csv

import hashlib

from http.cookies import SimpleCookie

import os

import uuid

import json


users_csv = "../data/users.csv"
session_csv = "../data/sessions.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(email):
    if not os.path.isfile(users_csv):
        return False
    with open(users_csv, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[2] == email:
                return True
    return False


def register_user(first_name, last_name, email, password, year,account_type):
    user_info = [first_name, last_name, email, hash_password(password), year,account_type]

    # Open your CSV file in append mode
    with open(users_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(user_info)
    
    return True

def generate_session_id():
    return str(uuid.uuid4())

def save_session_to_csv(session_id, email):
    with open(session_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([session_id, email])

def set_session_cookie(session_id):
    cookie = SimpleCookie()
    cookie['session_id'] = session_id
    # cookie['session_id']['httponly'] = True
    cookie['session_id']['path'] = '/'
    print(cookie.output())
    


def main():
    form = cgi.FieldStorage()
    email = form.getvalue("email")
    password = form.getvalue("password")
    first_name = form.getvalue("first_name")
    last_name = form.getvalue("last_name")
    year = form.getvalue("year")
    account_type="Student"

    if email and password and first_name and last_name and year and account_type:
        if user_exists(email):
            print("Content-Type: application/json")
            print()
            print(json.dumps({"success": False, "message": "You are already registered, try to login."}))
        else:
                register_user(first_name, last_name, email, password, year,account_type)
                session_id = generate_session_id()
                save_session_to_csv(session_id, email)
                set_session_cookie(session_id)
                print("Content-Type: application/json")
                print()
                print(json.dumps({"success": True, "message": "Registration successful"}))
    else:
        print("Content-Type: application/json")
        print()   
        print(json.dumps({"success": False, "message": "Email and password are required."}))

if __name__ == "__main__":
    main()