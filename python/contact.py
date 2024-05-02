#!/usr/bin/python3
import cgi

def validate_data(name, email, phone):
    if not name or not email or not phone:
        return False
    # Additional validation logic can be added here
    return True

def main():
    print("Content-Type: text/html\n")
    form = cgi.FieldStorage()
    
    name = form.getvalue('name')
    email = form.getvalue('email')
    phone = form.getvalue('phone')
    
    if validate_data(name, email, phone):
        print("<h1>Thank You for contacting us!</h1>")
        with open("../data/contacts.csv", "a") as file:
            file.write(f"{name},{email},{phone}\n")
    else:
        print("<h1>Error: Please fill all fields correctly.</h1>")

if __name__ == "__main__":
    main()
