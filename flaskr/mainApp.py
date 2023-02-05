import os
from flask import Flask, render_template, redirect, request
from flaskr.init_db import DBManager


def create_app():
    """Creates and configures the flask app."""
    app = Flask(__name__, instance_relative_config=True, template_folder="..\\flaskr\\templates")
    app.config.from_mapping(
        # This is used by Flask and extensions to keep data safe.
        # Should be overridden with a random value when deploying
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        EXPLAIN_TEMPLATE_LOADING=True
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


app = create_app()


@app.route('/')
def index():
    """Navigate to the home page."""
    return redirect('/home')


@app.route('/home')
def home():
    """Render the home page."""
    return render_template("/home.html")


@app.route('/menu')
def menu():
    """Render the menu page. Get menu items from the database."""
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Gets all the rows from menu.
    sql_connection.execute("SELECT * FROM menu;")
    rows = sql_connection.fetchall()

    db_manager.close()

    # Passes the rows of the table to the pages .html file.
    return render_template('/menu.html', rows=rows)


@app.route('/addMenuItem')
def add_menu_item():
    """Render the page to add a menu item."""
    return render_template('/addMenuItem.html')


@app.route('/addToMenu', methods=['POST'])
def add_to_menu():
    """Render the page to add a menu item. Adds an item to menu based on items from an HTML form."""
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Stores the items from the form in addMenuItem.html.
    name = request.form['name']
    price = request.form['price']
    calories = request.form['calories']
    allergens = request.form['allergens']

    # Add an item to the menu table.
    sql_connection.execute("INSERT INTO menu (name, price, calories, allergens)"
                   " VALUES (?, ?, ?, ?)", (name, price, calories, allergens))

    db_manager.get_db().commit()
    db_manager.close()

    return redirect('/menu')


@app.route('/editMenuItem')
def edit_menu_item():
    """Renders the page to edit the menu."""
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Gets all the rows in menu.
    sql_connection.execute("SELECT * FROM menu;")
    rows = sql_connection.fetchall()

    db_manager.close()

    # Passes the rows of the table to editMenuItem.html.
    return render_template('/editMenuItem.html', rows=rows)


@app.route('/removeMenuItem', methods=['POST'])
def remove_menu_item():
    """Renders the page to remove an item from the menu."""
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Iterate over data from the form in editMenuItem.html.
    for key, value in request.form.items():

        # Is the checkbox checked.
        if value == 'on':

            # Delete selected rows.
            sql_connection.execute("DELETE FROM menu WHERE itemID = ?", key)
            db_manager.get_db().commit()

    db_manager.close()

    return redirect('/menu')


@app.route('/login')
def login():
    """Renders the page to login."""
    return render_template('/login.html')
