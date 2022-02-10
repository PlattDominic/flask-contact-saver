# Program uses code from the FLASK micro framework and SQLAlchemy
# link to FLASK framework - https://github.com/pallets/flask
# link to SQlAlchemy - https://www.sqlalchemy.org/
from flask import Flask, render_template, url_for, request, redirect
from flask.wrappers import Request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import json

# Creates an instance 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdictionary.db'
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    phonenumber = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(2048), nullable=False, default="")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Contact %r>' % self.id


def SearchContacts(contactList, searchItem):
    search_result = list()

    for item in contactList:
        if item.name.lower() == searchItem or searchItem in item.name.lower():
            search_result.append(item)
    return search_result


@app.route('/')
def Index():
    if (request.args.get("search")):
        search = request.args.get("search").lower()
        contacts = Contact.query.all()

        result = SearchContacts(contacts, search)

        return render_template('search_result.html', contacts=result)
    else:
        return render_template('index.html')

@app.route('/viewall')
def viewAll():
    contacts = Contact.query.all()

    return render_template('view_all.html', contacts=contacts)


@app.route('/addcontact', methods=["GET", "POST"])
def addContact():
    # Checks if the request is a POST request
    if request.method == 'POST':
        # Get the contact information from the HTML form
        contact_name = request.form['name']
        contact_phonenumber = request.form['phonenumber']
        contact_email = request.form['email']

        # Create a Contact object using the data from the form
        new_contact = Contact(name=contact_name, phonenumber=contact_phonenumber, email=contact_email)

        try:
            # Add the new contact to the contact dictionary 
            db.session.add(new_contact)
            
            # Commit 
            db.session.commit()
            return redirect('/viewall')
        except:
            return 'There was a issue when creating and adding the term'
    else:
        return render_template('add_contact.html')


@app.route('/deletecontact/<int:id>')
def delete(id):
    delete_contact = Contact.query.get_or_404(id)

    try:
        db.session.delete(delete_contact)
        db.session.commit()
        return redirect('/viewall')
    except:
        return 'We ran into an issue while removing the contact, please try again'


if __name__ == "__main__":
    app.run(debug=True)
