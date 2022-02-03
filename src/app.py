from flask import Flask, render_template, url_for, request, redirect
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdictionary.db'
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    phonenumber = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(2048), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Contact %r>' % self.id



@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/addcontact', methods=["GET", "POST"])
def addContact():
    if request.method == 'POST':
        contact_name = request.form['name']
        contact_phonenumber = request.form['phonenumber']
        contact_email = request.form['email']

        new_contact = Contact(name=contact_name, phonenumber=contact_phonenumber, email=contact_email)

        try:
            #db.session.add(new_contact)
            #db.session.commit()
            return redirect('/')
        except:
            return 'There was a issue when creating and adding the term'
    else:
        return render_template('add_contact.html')




if __name__ == "__main__":
    app.run(debug=True)
