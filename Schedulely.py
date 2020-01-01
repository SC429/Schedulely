from flask import Flask, render_template, request, session    #need to download flask
from flask_session import Session    #need to download FLASK-SESSION
import os
from sqlalchemy import create_engine  #need to download sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

engine = create_engine('postgres://ehqnnhaxklfutw:28e7fb579f4bfc92d4039dcd34e693c689b57b211ea60b78240e3018f30c6940@ec2-174-129-33-30.compute-1.amazonaws.com:5432/dab40c5k7lkmt8')
db = engine.connect()

@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/create")
def create():
    data = db.execute("SELECT * FROM class_schedule").fetchall()
    return render_template('create.html', data = data, selection = 10)

@app.route("/result", methods=["POST"])
def result(selection):
    selections = [selection]
    startsession = [selection]
    endsession = [selection]
    for number in range(selection):
        selections[number] = request.form.get("{{ num }}.value")
        startsession[number] = db.execute("SELECT starttime FROM class_schedule WHERE id = %s", (selections[number])).fetchone()
        endsession[number] = db.execute("SELECT endtime FROM class_schedule WHERE id = %s", (selections[number])).fetchone()

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/thankyou", methods=["POST"])
def thankyou():
    def thankyou():
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        feedback = request.form.get("feedback")
        db.execute("INSERT INTO contact_info (fname, lname, email, feedback) VALUES (%s, %s, %s, %s)", (fname, lname, email, feedback))
        return render_template('thankyou.html', fname = fname)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
