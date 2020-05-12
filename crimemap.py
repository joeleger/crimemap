from dbhelper import DBHelper
from flask import Flask, render_template, request

app = Flask(__name__)
DB = DBHelper()


@app.route('/')
def home():
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print(e)
        data = None
    return render_template("home.html", data=data)

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
        data = None


if __name__ == '__main__':
    app.run(host='localhost', port=6000, debug=True)