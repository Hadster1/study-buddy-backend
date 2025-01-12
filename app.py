from flask import Flask, request, jsonify
from calendar import Calendar, Event
from course import Course
from datetime import datetime as dt
import mysql.connector

app = Flask(__name__)

# Database connection details
db_config = {
    'host': 'sql5.freesqldatabase.com',
    'database': 'sql5757142',
    'user': 'sql5757142',
    'password': 'tghuKCuYTv',
    'port': 3306
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Fetch the first entry's matriculationDate and graduationDate from the account table
cursor.execute("SELECT matriculationDate, graduationDate FROM users LIMIT 1")
result = cursor.fetchone()

if result:
    matriculation_date, graduation_date = result
    matriculation_date = matriculation_date
    graduation_date = graduation_date

    # Create a calendar using the fetched dates
    calendar = Calendar(matriculation_date, graduation_date)
    print(f"Calendar created from {matriculation_date} to {graduation_date}")

# Close the cursor and connection
cursor.close()
conn.close()

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.json
    try:
        # Create an Event object from the received JSON data
        event = Event(
            event_id=data['event_id'],
            name=data['name'],
            startDate=dt.strptime(data['startDate'], '%Y-%m-%d %H:%M'),
            endDate=dt.strptime(data['endDate'], '%Y-%m-%d %H:%M'),
            location=data['location'],
            recurrence=data['recurrence'],
            course=data.get('course'),
            isMultiDay=data.get('isMultiDay', False),
            color=data.get('color')
        )
        
        # Add the event to the calendar
        calendar.addEvent(event)
        
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Insert the event into the calendar table
        insert_query = """
        INSERT INTO calendar (event_id, name, startDate, endDate, location, recurrence, course, isMultiDay, color)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data['event_id'],
            data['name'],
            data['startDate'],
            data['endDate'],
            data['location'],
            data['recurrence'],
            data.get('course'),
            data.get('isMultiDay', False),
            data.get('color')
        ))
        conn.commit()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return success status
        return jsonify({"status": "success", "message": "Event added successfully"})
    except Exception as e:
        # Return error status
        return jsonify({"status": "error", "message": str(e)})

@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    user_id = request.json['user_id']
    try:
        # Convert the calendar to a JSON string
        calendar_json = calendar.to_json()
        
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Update the user's schedule in the users table
        update_query = "UPDATE users SET schedule = %s WHERE user_id = %s"
        cursor.execute(update_query, (calendar_json, user_id))
        conn.commit()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Return success status
        return jsonify({"status": "success", "message": "Schedule updated successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/add_course', methods=['POST'])
def add_course():
    courseList = []
    data = request.json
    try:
        # Create a Course object from the received JSON data
        new_course = Course(
            name=data['name'],
            startDate=dt.strptime(data['startDate'], '%Y-%m-%d'),
            endDate=dt.strptime(data['endDate'], '%Y-%m-%d'),
            program=data['program'],
            textbook=data['textbook'],
            topics=data['topics']
        )
        courseList.append(new_course)
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Insert the course into the courses table
        insert_query = """
        INSERT INTO courses (name, startDate, endDate, program, textbook, topics)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data['name'],
            data['startDate'],
            data['endDate'],
            data['program'],
            data['textbook'],
            json.dumps(data['topics'])  # Convert list of topics to JSON string
        ))
        conn.commit()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Return success status
        return jsonify({"status": "success", "message": "Course added successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
if __name__ == '__main__':
    app.run()
