import os
import sys
import rsa
from flask import Flask, render_template, redirect, request, session
from flaskr.init_db import DBManager
from flaskr.menu_item_model import MenuItemModel
from flaskr.user_account_model import UserAccountModel

publicKey, privateKey = rsa.newkeys(512)


def create_app():
    """Creates and configures the flask app."""
    app = Flask(__name__, instance_relative_config=True,
                template_folder="templates")
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
    if 'user' not in session:
        session['user'] = ['', '', '', 0]
    if 'order' not in session:
        session['order'] = ['', '', '']
    return redirect('/home')


@app.route('/home')
def home():
    """Render the home page."""
    return render_template('home.html', user=session.get('user'))


@app.route('/call', methods=['GET', 'POST'])
def call():
    """Assigns a waiter to a customer table, should they need help."""
    if request.method == 'GET':
        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        sql_connection.execute("INSERT INTO users (userID, first_name , last_name, password_hash , role)"
                               + " VALUES (69, 'Mahid', 'Gondal', '###', 1)")

        sql_connection.execute("INSERT INTO users (userID, first_name , last_name, password_hash , role)"
                               + " VALUES (96, 'Jhon', 'Snow', '##1', 1)")

        sql_connection.execute("SELECT first_name, last_name FROM users"
                               + " WHERE  role = 2"
                               + " ORDER BY RANDOM()"
                               + "  LIMIT 1;")
        rows = sql_connection.fetchall()

        db_manager.close()

        return render_template('calling.html', rows=rows)


@app.route('/menuFilter', methods=['GET', 'POST'])
def menu():
    """Filters the menu page. Get menu items from the database."""
    if request.method == 'POST':
        rows = filter_menu()
        return render_template('order.html', rows=rows, user=session.get('user'))


def get_menu():
    """Fetches every row of the menu from the database."""

    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute("SELECT * FROM menu;")
    rows = sql_connection.fetchall()

    db_manager.close()

    return rows


@app.route('/addMenuItem', methods=['GET', 'POST'])
def add_menu_item():
    """Render the page to add a menu item.
    Collects item info from an HTML form, checks the data is valid, and adds it to the database."""
    if request.method == 'GET':
        return render_template('addMenuItem.html', user=session.get('user'))

    elif request.method == 'POST':

        try:
            menu_item = MenuItemModel(request.form['name'],
                                      request.form['price'],
                                      request.form['category'],
                                      request.form['calories'],
                                      request.form.getlist('options'))
            add_item(menu_item)
        except Exception as ex:
            return render_template('addMenuItem.html', error=str(ex), user=session.get('user'))

        return redirect('/custMenu')


def add_item(menu_item):
    """Gets passed a menu item as an object and adds it to the database."""
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Add an item to the menu table.
    sql_connection.execute("INSERT INTO menu (name, price, category, calories, allergens)"
                           " VALUES (?, ?, ?, ?, ?)",
                           (menu_item.name, menu_item.price, menu_item.category, menu_item.calories,
                            menu_item.allergens))

    db_manager.get_db().commit()
    db_manager.close()

    return redirect('/custMenu')


@app.route('/editMenuItem', methods=['GET', 'POST'])
def edit_menu_item():
    """Displays all menu items, and allows you to select and delete them."""

    if request.method == 'GET':

        rows = get_menu()

        return render_template('/editMenuItem.html', rows=rows, user=session.get('user'))

    elif request.method == 'POST':

        item_id = request.form['itemID']
        delete_item(item_id)

        return redirect('/editMenuItem')


def delete_item(item):
    """Delete a menu item from the database."""

    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute("DELETE FROM menu WHERE itemID = ?", item)
    db_manager.get_db().commit()

    db_manager.close()

    return redirect('/editMenuItem')


@app.route('/login', methods=['GET', 'POST'])
def fetch_login():
    """Loads the login page. Fetches the user details and logs them in,"""

    if request.method == 'GET':
        return render_template('login.html', user=session.get('user'))

    elif request.method == 'POST':
        try:
            user_account = UserAccountModel(request.form['fname'],
                                            request.form['sname'],
                                            request.form['pass'],
                                            # UserAccountModel is used for logging in and creating an account.
                                            None)  # This is the role, which is irrelevant for logging in.
            try:
                login(user_account)
            except TypeError as ex:
                return render_template('login.html', loginError="Invalid credentials")
        except TypeError as ex:
            return render_template('login.html', loginError=str(ex))
        return redirect('/home')


def login(user_account):
    """Logs in a provided user."""
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute("""SELECT DISTINCT password_hash FROM users WHERE first_name=? AND last_name=?""",
                           (user_account.first_name, user_account.last_name))
    hashed_password_db = sql_connection.fetchone()[0]

    if user_account.password == hashed_password_db:
        sql_connection.execute("""SELECT DISTINCT * FROM users WHERE first_name=? AND last_name=?""",
                               (user_account.first_name, user_account.last_name))
        user = sql_connection.fetchone()
        db_manager.close()

        session['user'] = [user[0], user[1], user[2], user[4]]

        return redirect('/home')

    db_manager.close()
    raise TypeError("Invalid credentials")


@app.route('/createLogin', methods=['GET', 'POST'])
def create_login():
    """Loads the page to create a login. Fetches entered details, creates the account, and logs them in."""
    if request.method == 'GET':
        return redirect('/login')

    elif request.method == 'POST':
        try:
            user_account = UserAccountModel(request.form['firstName'],
                                            request.form['surname'],
                                            request.form['password'],
                                            1)
            try:
                create_account(user_account)
            except TypeError as ex:
                return render_template('login.html', createError="Invalid credentials", user=session.get('user'))
        except TypeError as ex:
            return render_template('login.html', createError=str(ex), user=session.get('user'))

        return redirect('/home')


def create_account(user_account):
    """Creates a user account with a provided user. Logs that user in after account creation."""
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute("""INSERT INTO users (first_name, last_name, password_hash, role)
                           VALUES (?, ?, ?,?)""",
                           (user_account.first_name,
                            user_account.last_name,
                            user_account.password,
                            user_account.role))

    db_manager.get_db().commit()
    db_manager.close()

    login(user_account)

    return redirect('/home')


@app.route('/logout')
def logout():
    """Logs out the current logged-in user."""
    session['user'] = ['', '', '', 0]
    session['order'] = [0, 0, 0]
    return redirect('/home')


@app.route('/order', methods=['GET', 'POST'])
def order():
    """Takes the details of a customer's order."""

    if request.method == 'GET':

        rows = get_menu()
        return render_template('order.html', rows=rows, user=session.get('user'))

    if request.method == 'POST':

        table_number = int(request.form['tableNumber'])
        setup_order(table_number)

        take_order()

        return redirect('/orderPayment')


def setup_order(table_num):
    """Insert the table number into the database, then set an order session using the ID of the order."""

    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Insert the table number, and the unpaid state into orders.
    sql_connection.execute("INSERT INTO orders (tableNum, paid)"
                           " VALUES (?, ?)", (table_num, 0))
    db_manager.get_db().commit()

    # The database autoincrements IDs.
    # Fetch the ID of the order just inserted.
    latest_order = sql_connection.lastrowid

    sql_connection.execute("SELECT * FROM orders WHERE orderID=?", (latest_order,))
    current_order = sql_connection.fetchone()

    session['order'] = [current_order[0],  # ID
                        current_order[1],  # table number
                        current_order[2]]  # paid/unpaid boolean

    db_manager.close()


def take_order():
    """From the HTML order form, insert every item with a quantity > 0 into the database for the order in the current
    session."""

    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    for key, value in request.form.items():
        # Ignore the table number of the form, we only care about menu items here.
        if key != 'tableNumber':
            # A valid quantity for each item is greater than 0.
            if value != '0':
                sql_connection.execute("INSERT INTO orderDetails "
                                       "(orderID, itemID, customerID, qty, state, order_time) "
                                       "VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                                       (session['order'][0], key, session['user'][0], value, 0))

                db_manager.get_db().commit()

    db_manager.close()


@app.route('/orderPayment', methods=['GET', 'POST'])
def order_payment():
    """Summarises the customer's order, provides a total cost, and requests payment details."""

    if request.method == 'GET':
        rows, total_price = summarise_order()
        return render_template('orderPayment.html', rows=rows, totalPrice=total_price)

    elif request.method == 'POST':
        # This is where the payment information would be processed.

        return redirect('/orderConfirmation')


def summarise_order():
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute(
        """SELECT menu.name, orderDetails.qty, menu.price
           FROM menu
           JOIN orderDetails ON menu.itemID=orderDetails.itemID
           WHERE orderDetails.orderID=?""",
        (session['order'][0],))
    rows = sql_connection.fetchall()

    return rows, calculate_total_price(rows)


def calculate_total_price(order_details):
    total_price = 0
    for item in order_details:
        price = item[2]
        qty = item[1]
        total_price += (price * qty)
    return total_price


@app.route('/orderConfirmation', methods=['GET', 'POST'])
def order_confirmation():
    """Tells the customer their order has been confirmed."""

    if request.method == 'GET':
        return render_template('orderConfirmation.html')

    elif request.method == 'POST':
        return redirect('/home')


@app.route('/kitchenOrders', methods=['GET', 'POST'])
def kitchen_orders():
    """Displays the orders that kitchen staff need to work on."""

    if request.method == 'GET':

        all_orders = get_orders_to_make()
        return render_template('kitchenOrders.html', all_orders=all_orders)

    elif request.method == 'POST':

        order_id = request.form['orderID']
        update_state_to('2', order_id)  # mark order as 'ready to deliver'

        return redirect('/kitchenOrders')


def get_orders_to_make():
    """Fetch the orders that need to be made in the order they were placed, then return as a dictionary."""

    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Gets all the rows from menu.  <-- No it fucking doesn't?
    sql_connection.execute(
        "SELECT orderID, itemID, qty, order_time FROM orderDetails WHERE state=1 ORDER BY orderID ASC;")
    rows = sql_connection.fetchall()

    all_orders = format_kitchen_orders_in_dictionary(rows, sql_connection)

    db_manager.close()

    return all_orders


def format_kitchen_orders_in_dictionary(rows, sql_connection):
    """Receives the orders to be made, and an sql cursor to fetch the name to add to a dictionary."""

    all_orders = {}

    for row in rows:

        order_num = row[0]
        if order_num not in all_orders:
            all_orders[order_num] = []

        sql_connection.execute(
            "SELECT name FROM menu WHERE itemID=?", (row[1],))
        name = sql_connection.fetchone()  # this is returned as a list - ('x',)

        all_orders[order_num].append([name[0], row[2], row[3]])

    return all_orders


# TODO: I'm fairly sure this never gets used, and also wouldn't work if it was...
@app.route('/updateOrderStatus', methods=['GET'])
def update_order_status():
    if request.method == 'GET':
        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()
        sql_connection.execute("SELECT state FROM orderDetails;")

        # Update the order status in the database
        order_state = 0
        sql_connection.execute("UPDATE orderDetails SET (state)"
                               " WHERE (?)", order_state)
        db_manager.close()
    # Return a response indicating the status of the update
    return {"message": "Order status updated successfully"}


def filter_menu():
    """Filters the menu by allergens, price, or calories."""
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()
    # Initial SQL command Built up over filtering
    command = "SELECT * FROM menu "

    # Sort by ranges (both price and calorie)
    pri_min = str(request.form['Price_Min'])
    pri_max = str(request.form['Price_Max'])
    cal_min = str(request.form['Calories_Min'])
    cal_max = str(request.form['Calories_Max'])
    if pri_max or pri_min or cal_max or cal_min:
        command += "WHERE price >= 0 "
        if pri_max:
            command += "AND price <= " + pri_max + " "
        if pri_min:
            command += "AND price >= " + pri_min + " "
        if cal_max:
            command += "AND calories <= " + cal_max + " "
        if cal_min:
            command += "AND calories >= " + cal_min + " "

    # Sort By Dropdown menu
    sort = request.form['Sort']
    if sort == 'HPrice':
        command += "ORDER BY price DESC"
    elif sort == 'LPrice':
        command += "ORDER BY price"
    elif sort == 'HCalorie':
        command += "ORDER BY calories DESC"
    elif sort == 'LCalorie':
        command += "ORDER BY calories"
    command += ';'
    sql_connection.execute(command)
    rows = sql_connection.fetchall()

    # Allergens removed from menu
    allergies = request.form.getlist('options')
    if allergies:
        filtered_rows = []
        for row in rows:
            found = False
            allergens = row[5].split(", ")
            for i in range(len(allergens)):
                for j in range(len(allergies)):
                    if allergens[i] == allergies[j]:
                        found = True
            if not found:
                filtered_rows.append(row)
        return filtered_rows
    else:
        return rows


@app.route('/custMenu')
def cust_menu():
    """Displays the menu."""
    foods = get_menu()
    return render_template('customerMenu.html', foods=foods, user=session.get('user'))


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', user=session.get('user'))


@app.route('/waiterOrders', methods=['GET', 'POST'])
def waiter_order_confirm():
    """Shows the waiters the orders taken, and lets them confirm them."""

    if request.method == 'GET':
        all_orders = get_waiter_orders('0')
        return render_template('waiterOrderConfirm.html', all_orders=all_orders)

    elif request.method == 'POST':
        order_id = request.form['orderID']
        update_state_to('1', order_id)

        return redirect('/waiterOrders')


def get_waiter_orders(state):
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute(
        """SELECT orderDetails.orderID,
                  menu.name, 
                  orders.tableNum,
                  orderDetails.qty, 
                  orderDetails.order_time
           FROM orderDetails 
           JOIN menu ON orderDetails.itemID=menu.itemID
           JOIN orders ON orderDetails.orderID=orders.orderID
           WHERE state=?
           ORDER BY orderDetails.orderID;""", state)
    rows = sql_connection.fetchall()
    db_manager.close()

    return format_waiter_orders_in_dictionary(rows)


def format_waiter_orders_in_dictionary(rows):
    all_orders = {}
    for row in rows:

        order_id = row[0]
        if order_id not in all_orders:
            all_orders[order_id] = []

        name = row[1]
        table_num = row[2]
        qty = row[3]
        order_time = row[4]

        all_orders[order_id].append([name, table_num, qty, order_time])

    return all_orders


@app.route('/waiterOrdersCancel', methods=['GET', 'POST'])
def waiter_order_cancel():
    """Cancels the selected order."""

    if request.method == 'GET':
        return redirect('/waiterOrders')

    elif request.method == 'POST':
        order_id = request.form['orderID']
        update_state_to('5', order_id)

        return redirect('/waiterOrders')


@app.route('/waiterOrdersDelivered', methods=['GET', 'POST'])
def waiter_order_delivered():
    """Shows the orders to be delivered, and allows them to be marked as such."""

    if request.method == 'GET':
        all_orders = get_waiter_orders('2')
        return render_template('waiterOrderDeliver.html', all_orders=all_orders)

    elif request.method == 'POST':
        order_id = request.form['orderID']
        update_state_to('3', order_id)

        return redirect('/waiterOrdersDelivered')


def update_state_to(state, order_id):
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Update the orderDetails table
    sql_connection.execute(
        "UPDATE orderDetails SET state=? WHERE orderID=?", (state, order_id))
    db_manager.get_db().commit()

    db_manager.close()


@app.route('/manageAccounts', methods=['GET', 'POST'])
def manage_accounts():
    """Managers can change the admin level of accounts here to hire or fire kitchen staff, waiters, and managers. This
    displays all accounts and their current privilege level."""

    if request.method == 'GET':
        users = get_all_users()
        return render_template('managerAccounts.html', rows=users)

    elif request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']

        users = get_users_with_name(first_name, last_name)

        return render_template('managerAccounts.html', rows=users)


def get_all_users():
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute(
        "SELECT userID, first_name, last_name, role FROM users")
    users = sql_connection.fetchall()

    db_manager.close()

    return users


def get_users_with_name(first_name, last_name):
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute("SELECT userID, first_name, last_name, role"
                           " FROM users WHERE first_name=? AND last_name=?;", (first_name, last_name))
    users = sql_connection.fetchall()

    db_manager.close()

    return users


@app.route('/manageAccountsEdit', methods=['GET', 'POST'])
def manage_accounts_edit():
    """Allows managers to edit the admin level of an account."""

    if request.method == 'GET':
        return redirect('/manageAccounts')

    elif request.method == 'POST':
        user_id = request.form['userID']
        role = request.form['role']

        update_user(user_id, role)

        return redirect('/manageAccounts')


def update_user(user_id, role):
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute(
        "UPDATE users SET role=? WHERE userID=?", (role, user_id))
    db_manager.get_db().commit()

    db_manager.close()

    return redirect('/manageAccounts')


@app.route('/assign_table', methods=['POST'])
def assign_table():
    waiter_id = request.form.get('waiter_id')
    table_num = request.form.get('tableNum')

    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute('SELECT waiter_id FROM table_assignments WHERE table_id=?', (table_num,))
    result = sql_connection.fetchone()
    if result:
        return 'Table', table_num, 'is already assigned to waiter', (result[0])
    sql_connection.execute('INSERT INTO table_assignments (table_id, waiter_id) VALUES (?, ?)', (table_num, waiter_id))
    db_manager.get_db().commit()
    db_manager.close()

    return 'Table', table_num, 'has been assigned to waiter', waiter_id


@app.route('/customerOrders')
def customer_orders():
    """Shows a customer the details of their orders, along with their current statuses."""

    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Gets all the rows from menu.
    sql_connection.execute(
        "SELECT orderID, itemID, qty, order_time, state FROM orderDetails WHERE customerID=? ORDER BY orderID ASC;",
        (session['user'][0], ))
    rows = sql_connection.fetchall()

    all_orders = {}
    for row in rows:
        if row[0] not in all_orders:
            all_orders[row[0]] = []
        sql_connection.execute(
            "SELECT name FROM menu WHERE itemID=?", (row[1],))
        name = sql_connection.fetchone()
        temp_list = [name[0], row[2], row[3], row[4]]
        all_orders[row[0]].append(temp_list)

    db_manager.close()

    return render_template('customerOrderTracking.html', all_orders=all_orders)
