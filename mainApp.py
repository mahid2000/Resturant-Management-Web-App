import os
from flask import Flask, render_template, redirect, request
from init_db import DBManager


def create_app():
    # Create and configure the flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # This is used by Flask and extensions to keep data safe.
        # Should be overridden with a random value when deploying
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sqlite3')
    )

    return app


app = create_app()


# Route for /.
@app.route('/')
def index():
    return redirect('/home')


# Route for the /home page.
@app.route('/home')
def home():
    return render_template('home.html')


# Route for the /menu page.
@app.route('/menu')
def menu():

    # Creates a connection to the database and a cursor.
    db_manager = DBManager(app)
    cursor = db_manager.get_cursor()

    # Cursor executes a statement returning all the rows in menu and stores results in a list.
    cursor.execute("SELECT * FROM menu;")
    rows = cursor.fetchall()

    # Close the cursor and the connection.
    db_manager.close()

    # Passes the rows of the table to the pages .html file.
    return render_template('menu.html', rows=rows)


# Route for /addMenuItem page.
@app.route('/addMenuItem')
def add_menu_item():
    return render_template('addMenuItem.html')


# Route when submitting a new menu item.
@app.route('/addToMenu', methods=['POST'])
def add_to_menu():

    # Creates a connection to the database and cursor.
    db_manager = DBManager(app)
    cursor = db_manager.get_cursor()

    # Stores the items from the form in addMenuItem.html.
    name = request.form['name']
    price = int(request.form['price'])
    calories = int(request.form['calories'])
    allergens = request.form['allergens']

    # Executes a SQL statement adding a row to the menu table.
    cursor.execute("INSERT INTO menu (name, price, calories, allergens)"
                   " VALUES (?, ?, ?, ?)", (name, price, calories, allergens))

    # Commit the changes to the databases.
    db_manager.get_db().commit()

    # Close the cursor and the connection.
    db_manager.close()

    # Return to the /menu page.
    return redirect('/menu')


# Route for the /editMenuItem page.
@app.route('/editMenuItem')
def edit_menu_item():

    # Creates a connection to the database and cursor.
    db_manager = DBManager(app)
    cursor = db_manager.get_cursor()

    # Cursor executes a statement returning all the rows in menu and stores results in a list.
    cursor.execute("SELECT * FROM menu;")
    rows = cursor.fetchall()

    # Close the cursor and the connection.
    db_manager.close()

    # Passes the rows of the table to the pages .html file.
    return render_template('editMenuItem.html', rows=rows)


# Route when removing a menu item.
@app.route('/removeMenuItem', methods=['POST'])
def remove_menu_item():

    # Creates a connection to the database and cursor.
    db_manager = DBManager(app)
    cursor = db_manager.get_cursor()

    # Iterate over the form data provided in editMenuItem.html.
    for key, value in request.form.items():

        # Check if the checkbox was checked.
        if value == 'on':

            # Executes a SQL statement deleting rows in menu that have been selected.
            cursor.execute("DELETE FROM menu WHERE itemID = ?", key)
            db_manager.get_db().commit()

    # Close the cursor and the connection.
    db_manager.close()

    # Returns to the /menu page.
    return redirect('/menu')

