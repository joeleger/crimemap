import datetime
import string

import dbconfig
import json
import os
import dateparser

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

from flask import Flask, render_template, request

app = Flask(__name__)
DB = DBHelper()
categories = ['mugging', 'break-in', ]
API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")


@app.route('/')
def home(error_message=None):
    try:
        api_key = API_KEY
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)

    except Exception as e:
        print(e)
        data = None
    return render_template("home.html",
                           crimes=crimes,
                           api_key=api_key,
                           error_message=error_message,
                           categories=categories)


@app.route("/submitcrime", methods=['POST'])
def submit_crime():
    category = request.form.get("category")
    if category not in categories:
        return home()
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        return home()
    date = format_date(request.form.get("date"))
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format")

    description = request.form.get("description")
    description = ''.join(sanitize_string(description))
    try:
        DB.add_crime(category, date, latitude, longitude, description)
    except Exception as err:
        print(err)
    return home()


@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
        data = 'No Records'
    return home()


def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None


def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    return [x for x in userinput if x in whitelist]


if __name__ == '__main__':
    app.run(port=5000, debug=True)
