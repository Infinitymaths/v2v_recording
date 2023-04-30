from flask import Flask, redirect, url_for, render_template, request, flash
import os
from datetime import datetime, timedelta, timezone
import pytz
from cal_setup import get_calendar_service
from dateutil import parser
import sqlite3

FOLDER = os.path.join('static', 'logo')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = FOLDER
app.config['SECRET_KEY'] = "v2v2k17"
full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo_2.png')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if 'button1' in request.form:
            # Action for button1
            return redirect(url_for('add_event'))
        elif 'button2' in request.form:
            # Action for button2
            return redirect(url_for('delete_event'))
        elif 'button3' in request.form:
            return redirect(url_for('update_event'))
        elif 'button4' in request.form:
            return redirect(url_for('login'))
    return render_template("index.html", user_image=full_filename)


@app.route('/addevent', methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        name = request.form.get("nm")
        print(request.form.get("startdate"))
        start_date = parser.parse(request.form.get("startdate"))
        start_date = start_date.isoformat()
        end_date = parser.parse(request.form.get("enddate"))
        end_date = end_date.isoformat()
        print(start_date)
        print(end_date)
        service = get_calendar_service()
        event_result = service.events().insert(calendarId='sharathdinesh23@gmail.com',
                                               body={
                                                   "summary": 'Recording of ' + name,
                                                   "description": "Recording of " + name + " on " + str(start_date),
                                                   "start": {"dateTime": start_date, "timeZone": "UTC"},
                                                   "end": {"dateTime": end_date, "timeZone": "UTC"}
                                               }
                                               ).execute()

        return redirect(url_for('main'))
    return render_template("form.html", user_image=full_filename)


@app.route('/deleteevent', methods=["POST", "GET"])
def delete_event():
    if request.method == "POST":
        date = request.form.get('date')
        return redirect(url_for('show_event', date=date))
    return render_template("delete_event.html",user_image=full_filename)

@app.route('/showevent/<date>', methods=["POST", "GET"])
def show_event(date):
    # selected_options = request.form.get('options')
    date_split = date.split("-")
    start_date = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]), 00, 00, 00, 0)
    start_date = pytz.UTC.localize(start_date).isoformat()
    end_date = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]), 23, 59, 59, 99999)
    end_date = pytz.UTC.localize(end_date).isoformat()
    service = get_calendar_service()
    calendars_result = service.events().list(calendarId='primary', timeMin=start_date, timeMax=end_date,
                                             timeZone='UTC').execute()
    calendars = calendars_result.get('items', [])
    options = []
    for calendar in calendars:
        print(calendar['summary'])
        options.append(calendar['summary'])
    return render_template("show_event.html",user_image=full_filename, options=options)
    # return "<h1>hello</h1>"

@app.route('/deleted_event/<option>',methods=["POST","GET"])
def deleted_event(option):
    # selected_options = request.form.get('options')
    # print(selected_options)
    service = get_calendar_service()
    events_result = service.events().list(calendarId='primary',q=option).execute()
    events = events_result.get('items', [])
    for event in events:
        service.events().delete(calendarId='primary',eventId=event['id']).execute()
        flash('Deletion successful')
    return redirect(url_for("main"))

@app.route('/updateevent',methods=["POST","GET"])
def update_event():
    if request.method == "POST":
        date = request.form.get('date')
        return redirect(url_for('show_event_update', date=date))
    return render_template("update_event.html",user_image=full_filename)

@app.route('/showevent/<date>', methods=["POST", "GET"])
def show_event_update(date):
    # selected_options = request.form.get('options')
    date_split = date.split("-")
    start_date = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]), 00, 00, 00, 0)
    start_date = pytz.UTC.localize(start_date).isoformat()
    end_date = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]), 23, 59, 59, 99999)
    end_date = pytz.UTC.localize(end_date).isoformat()
    service = get_calendar_service()
    calendars_result = service.events().list(calendarId='primary', timeMin=start_date, timeMax=end_date,
                                             timeZone='UTC').execute()
    calendars = calendars_result.get('items', [])
    options = []
    for calendar in calendars:
        # print(calendar['summary'])
        options.append(calendar['summary'])
    return render_template("show_event_update.html",user_image=full_filename, options=options)

@app.route('/updated_event/<option>',methods=["POST","GET"])
def updated_event(option):
    if request.method == "POST":
        name = request.form.get('update')
        start_date = parser.parse(request.form.get("start_date"))
        start_date = start_date.isoformat()
        end_date = parser.parse(request.form.get("end_date"))
        end_date = end_date.isoformat()
        service = get_calendar_service()
        events_result = service.events().list(calendarId='primary', q=option).execute()
        events = events_result.get('items', [])
        for event in events:
            service.events().update(
                calendarId='primary',
                eventId=event['id'],
                body={
                    "summary": 'Updated Recording Time of '+ name,
                    "description": 'Recording of '+name,
                    "start": {"dateTime": start_date, "timeZone": 'Asia/Kolkata'},
                    "end": {"dateTime": end_date, "timeZone": 'Asia/Kolkata'},
                },
            ).execute()
        return redirect(url_for('main'))
    return render_template('updated_event.html',user_image=full_filename)


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get('username') != 'admin' or request.form.get('password') != 'v2v2k17':
            flash("Invalid credentials. try again later")
            return redirect(url_for('login'))
        else:
            flash('you are succesfully logged in')
            return redirect(url_for('admin'))
    return render_template("login.html", user_image=full_filename)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        if 'add_user' in request.form:
            return redirect(url_for('add_user'))
        elif "delete_user" in request.form:
            return redirect(url_for('delete_user'))
        elif "show_user" in request.form:
            return redirect(url_for('show_user'))
        elif 'update_user' in request.form:
            return redirect(url_for('update_user'))
    return render_template('admin.html', user_image=full_filename)


@app.route("/adduser", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        teacher_name = request.form.get('name')
        email_address = request.form.get('email')
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO recording (name,email) VALUES (?,?)", (teacher_name, email_address))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    return render_template('add_user.html', user_image=full_filename)


@app.route("/deleteuser", methods=["GET", "POST"])
def delete_user():
    if request.method == "POST":
        name = request.form.get('name')
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        statement = 'DELETE FROM recording WHERE  name = "' + str(name) + '"'
        print(statement)
        cur.execute(statement)
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    return render_template('delete_user.html', user_image=full_filename)


@app.route("/showuser", methods=["GET", "POST"])
def show_user():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("select * from recording")
    data = cur.fetchall()
    return render_template('show_user.html', user_image=full_filename, data=data)


@app.route("/updateuser", methods=["GET", "POST"])
def update_user():
    if request.method == "POST":
        name = request.form.get('name')
        update = request.form.get('update')
        email = request.form.get('email')
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        if update:
            statement = 'UPDATE recording SET name = "' + str(update) + '" where name = "' + str(name) + '"'
            cur.execute(statement)
            conn.commit()
            conn.close()
        elif email:
            statement = 'UPDATE recording SET email = "' + str(email) + '" where name = "' + str(name) + '"'
            cur.execute(statement)
            conn.commit()
            conn.close()
        return redirect(url_for('admin'))
    return render_template("update_user.html", user_image=full_filename)


app.run()
