#!/usr/bin/python3

import cgi
import json


def validate_data(name, email, phone):
    if not name or not email or not phone:
        return False
    # Additional validation logic can be added here
    return True

def main():
    form = cgi.FieldStorage()
    
    name = form.getvalue('name')
    email = form.getvalue('email')
    phone = form.getvalue('phone')
    
    if validate_data(name, email, phone):
        with open("../data/contacts.csv", "a") as file:
            file.write(f"{name},{email},{phone}\n")
        print("Content-Type: application/json")
        print()  # End of headers
        print(json.dumps({"success": True, "message": "Thank you for signing up for our newsletter!."}))
    else:
         print("Content-Type: application/json")
         print()  # End of headers
         print(json.dumps({"success": False, "message": "Try again to sign up us!"}))

if __name__ == "__main__":
    main()