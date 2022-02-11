# Program uses code from the FLASK micro framework and SQLAlchemy
# link to FLASK framework - https://github.com/pallets/flask
# link to SQlAlchemy - https://www.sqlalchemy.org/
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


# Creates an instance 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contactdatabase.db'
db = SQLAlchemy(app)


# The Contact Database Table Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    phonenumber = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(2048), nullable=False, default="")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)



# Searches the contact database and tries to see if the searchItem
# Matches with any name of an contact 
def SearchContacts(searchItem):
    # Get all records in the Contact Database Table
    contacts = Contact.query.all()
    # This is the list that will contain all the possible search results and will be returned
    search_result = list()

    # Iterates through all items in the contact database and checks if any
    # Contact name matches with searchItem and also if searchItem is a substring
    # of a name, if any checks are true, that contact is added to search result
    for item in contacts:
        if searchItem in item.name.lower():
            search_result.append(item)

    return search_result


@app.route('/')
def Index():
    # Checks if the route included a search query
    if (request.args.get("search")):
        # Get search query from the GET request
        search = request.args.get("search").lower()

        # Check if any of contacts name matches the users search by
        # Calling SearchContact
        result = SearchContacts(search)
        
        # Render the search_result HTMl and passing the search result as contacts data
        return render_template('search_result.html', search_results=result)
    else:
        return render_template('index.html')

@app.route('/viewall')
def viewAll():
    # Get all records in Contact Database Table
    contacts = Contact.query.all()
    
    # Renders view_all HTML with contacts data being passed
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
            # Add the new contact to the contact database session
            db.session.add(new_contact)
            
            # Commit the current transaction to the database
            db.session.commit()
            # Redirect user to /viewall URL
            return redirect('/viewall')
        except:
            # Display error if adding or commiting to database failed
            return 'There was a issue when creating and adding the term'
    else:
        # If request was a GET, render the add contact HTML to allow user to create a contact
        return render_template('add_contact.html')


@app.route('/deletecontact/<int:id>')
def delete(id):
    # Get the contact to delete using it's ID
    delete_contact = Contact.query.get_or_404(id)

    try:
        # Attempt to delete the contact by passing in its object form
        db.session.delete(delete_contact)
        # Commit the current transaction to the database
        db.session.commit()
        return redirect('/viewall')
    except:
        # Display error if adding or commiting to database failed
        return 'We ran into an issue while removing the contact, please try again'


if __name__ == "__main__":
    app.run(debug=True)
