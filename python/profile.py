#!/usr/bin/python3

import cgi

import csv
from http.cookies import SimpleCookie
import os
import sys


users_csv = "../data/users.csv" # USE ABSOLUTE PATH FOR LOCAL DEVELOPMENT
session_csv = "../data/sessions.csv"

filename = "users.txt"

def htmlhead():
    print("Content-Type: text/html \n\n")
    print('''

	<!DOCTYPE html>
	<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Bike</title>
		<link rel="stylesheet" href="../static/css/main.css">
		<link rel="stylesheet" href="../static/css/responsive.css">
		<link rel="shortcut icon" type="image/jpg" href="../static/images/nyuad logo.png">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.min.css"
			crossorigin="anonymous" />
		<link rel="preconnect" href="https://fonts.gstatic.com">
		<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap" rel="stylesheet">
		<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
		<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap" rel="stylesheet">
	</head>
	<body>
	''')

def htmltail():
    html_end = '</body></html>'
    return html_end 

def errormessage(message):
    print("Content-Type: text/html \n\n")
    print(f"""
			<!DOCTYPE HTML>
			<head>
			<title> Hello Program </title>
				<link rel='Stylesheet' href='register.css'>
				</head>
				<body>
				<div  class='wrapper'>
              <div  class="wrapper">
              <h1>{message}</h1>
              </div>
              </div>
			""")

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
    session_id = get_session_id_from_cookie()
    if session_id:
        sys.stderr.write(os.path.dirname(os.path.abspath(__file__)))
        email = get_email_from_session(session_id)
        if email:
            user_info = get_user_info(email)            
            if user_info:
                htmlhead()
                print('''
                    <header>
						<div class="header-wrapper">
							<span class="menu-logo hp-viewport fas fa-ellipsis-h"></span>
							<ul class="header-list">
								<li class="header-content hp-viewport bike-header"><a href="#"><img class="logo" src="../static/images/nyuad logo.png"></a></li>
								<li class="header-content hp-viewport-hide"><a href="../templates/index.html">Home</a></li>
								<li class="header-content hp-viewport-hide"><a href="../templates/about.html">About Us</a></li>
								<li class="header-content hp-viewport-hide"><a href="../templates/bike.html">Book A Bike</a></li>
								<li class="header-content hp-viewport-hide"><a href="../templates/contact.html">Contact Us</a></li>
								<li class="header-content hp-viewport-hide"></li>
								<li class="header-content hp-viewport-hide"><a href="../python/profile.py"><img src="../static/images/dummy.png" class="profile-img">My Profile</a></li>
							</ul>
						</div>
					</header>
                    
                     <main>
						<div class="bgimg display-container">
							<div class="display-middle center">
							<span class="text-white" style="font-size:100px">NYUAD<br>Bikeshare</span>
							</div>
						</div>

						<div class="section-container">

						<section id="profile" class="about-section">
							<div class="about-image">
								<img src="../static/images/faiza.jpeg" alt="Profile Picture">
							</div>
							<div class="about-content">''')
                print(f"<h2>My Profile</h2>")
                print(f"<div class='contact-info'>")
                print(f"<p>Name:{user_info['first_name']} {user_info['last_name']}</p>")
                print(f"<p>Email: {user_info['email']}</p>")
                print(f'<p>Age: {user_info["age"]}</p>')
                print(f'<p>Age: {user_info["class_year"]}</p>')
		print('<a href="logout.py"><button>Log out</button></a>')
                print('''
						</div>
						</div>
						</section>
						</main>
                ''')
            else:
                errormessage("No user info stored in the data")
        else:
            errormessage("No user_id info stored in the data")
    else:
        errormessage("No session_id info stored in the cookie")
    
    htmltail()

main() # type: ignore
