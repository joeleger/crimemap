import dbconfig
import json
import os

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

from flask import Flask, render_template, request

app = Flask(__name__)
DB = DBHelper()

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")


@app.route('/')
def home():
    try:
        api_key = API_KEY
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)

    except Exception as e:
        print(e)
        data = None
    return render_template("home.html", crimes=crimes, api_key=api_key)


@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB.add_crime(category, date, latitude, longitude, description)
    return home()


@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print(e)
        data = None
    return home()


@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
        data = 'No Records'
    return home()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
