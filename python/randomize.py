#!/usr/bin/python3

import cgi
import csv
import datetime
import json
import os
import random


#function to dertermine which the file bases on a week 
def get_weekly_filenames():
    """Generate filenames based on the current week number."""
    
    current_date = datetime.datetime.now()
    current_week = current_date.isocalendar()[1]

    previous_week = current_week - 1 if current_week > 1 else 52  # Adjust for year transition

    current_week_file = f"../data/reservations_week{current_week}.csv"
    selected_this_week_file = f"../data/selected_week{current_week}.csv"
    selected_last_week_file = f"../data/selected_week{previous_week}.csv"
    
    return current_week_file, selected_this_week_file, selected_last_week_file

#function to read all student bike reservations and categorize them by the bike types
def read_reservations(filename):
    """Read reservations from file and organize by bike type."""
    reservations = {'Road': [], 'Mountain': [], 'Hybrid': []}
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                fullname = row[0]
                email = row[1]
                date_str = row[2]
                bike_type = row[3]
                session = row[4]
                reservations[bike_type].append((fullname, email, date_str, bike_type,session))
    except FileNotFoundError:
        print(json.dumps({"success": False, "message": "Reservation file not found"}))
        return {}
    return reservations

#function to read students who were seleted to get bikes last week. 
def read_previous_selections(filename):
    """Read emails from last week's selections to filter them out."""
    previous_selections = set()
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)        
            for row in reader:
                email = row[1]
                previous_selections.add(email)
    except FileNotFoundError:
        pass
    return previous_selections

#function to filter out students who got bike last week and also remove duplicates 
def remove_duplicates_and_previous(reservations, previous_selections):
    """Filter out duplicates and previous week's selections."""
    filtered = {}
    for bike_type, entries in reservations.items():
        unique_entries = {}
        for entry in entries:
            email = entry[1]  
            if email not in previous_selections:
                unique_entries[email] = entry 

        filtered[bike_type] = list(unique_entries.values()) 
    return filtered

def randomize_and_select(reservations, available_counts):
    """Randomize entries within each bike type and select based on available counts."""
    selected_students = []
    for bike_type, count in available_counts.items():
        if bike_type in reservations:
            if len(reservations[bike_type]) > count:
                selected_students.extend(random.sample(reservations[bike_type], count))
            else:
                selected_students.extend(reservations[bike_type])
    return selected_students

def store_selected(selected_students,selected_this_week_file):
    """Store selected students in a file."""
    with open(selected_this_week_file, "w", newline='') as file:
        writer = csv.writer(file)
        for student in selected_students:
            writer.writerow([student[0], student[1], student[2], student[3],student[4]])

def print_json(selected_students):
    # Convert each student's data into a dictionary format for JSON serialization
    data_to_json = [
        {
            "name": student[0],
            "email": student[1],
            "date": student[2],
            "bike_type": student[3],
            "session": student[4]
        } for student in selected_students
    ]
    print("Content-Type: application/json\n")
    print(json.dumps({"success": True, "students": data_to_json}))


def main():
    form = cgi.FieldStorage()
    available_counts = {
        'Road': int(form.getvalue('roadCount')),
        'Mountain': int(form.getvalue('mountainCount')),
        'Hybrid': int(form.getvalue('hybridCount'))
    }
    # File locations
    current_week_file, selected_this_week_file, selected_last_week_file = get_weekly_filenames()
    
    reservations = read_reservations(current_week_file)

    previous_selections = read_previous_selections(selected_last_week_file)

    filtered_reservations = remove_duplicates_and_previous(reservations, previous_selections)

    selected_students = randomize_and_select(filtered_reservations, available_counts)
  
    store_selected(selected_students,selected_this_week_file)

    print_json(selected_students)
    

if __name__ == '__main__':
    main()