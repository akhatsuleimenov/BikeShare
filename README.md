# NYUAD Bikeshare System

## Project Overview
This project is designed to manage and automate the process of bike sharing at NYUAD, facilitating easy access to bicycles for students. It includes a web interface for managing reservations, user accounts, and bike availability.

## Directory and File Structure

### `/data`
Contains CSV files that store critical data for the application:
- **`contacts.csv`**: Stores contact information gathered from the website's contact form.
- **`reservations_weekXX.csv`**: Weekly reservation files containing details about bike bookings.
- **`selected_weekXX.csv`**: Weekly files listing students who have been allocated bikes.
- **`sessions.csv`**: Manages active user sessions for logged-in users.
- **`users.csv`**: User registration details including encrypted passwords and personal information.

### `/python`
Python scripts providing backend functionality:
- **`contact.py`**: Handles submissions from the contact form.
- **`login.py`**: Manages user logins, verifying credentials against `users.csv`.
- **`logout.py`**: Handles user logout and session termination.
- **`profile.py`**: Allows users to view their profile information.
- **`randomize.py`**: Implements the logic for randomly selecting students for bike allocations based on availability and randomization.
- **`register.py`**: Manages new user registrations, storing credentials securely.
- **`submit-reservation.py`**: Processes bike reservation requests from users and save them in the csv file.

### `/static`
Stores static assets used by the web application:
- **`/css`**: CSS files for styling the web pages.
- **`/images`**: Images used across the website, such as logos, bike photos, and icons.

### `/templates`
HTML files that serve as the visual backbone of the website:
- **`about.html`**: Information about the bike share program.
- **`bike.html`**: Details available bikes and allows users to make reservations.
- **`contact.html`**: Contact form for user inquiries.
- **`index.html`**: The homepage of the website, introducing the bike share system.
- **`login.html`**: Login page for returning users.
- **`randomize.html`**: Interface for admins to randomize and finalize weekly bike allocations.
- **`rec.html`**: Recommendations or special offers page (if applicable).
- **`registration.html`**: Sign up page for new users.
- **`terms.html`**: Terms and conditions of the bike share program.
