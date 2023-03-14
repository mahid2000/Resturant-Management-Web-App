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
    #Render the home page.
    return render_template('home.html', user=session.get('user'))


@app.route('/call', methods=['GET', 'POST'])
def call():
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


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    """Render the menu page. Get menu items from the database."""
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    # Gets all the rows from menu or apply the filter if made.
    if not request.form:
        sql_connection.execute("SELECT * FROM menu;")
        rows = sql_connection.fetchall()
    else:
        if request.method == 'GET':
            return render_template('menu.html')
        elif request.method == 'POST':
            rows = filter_menu()

    db_manager.close()

    # Passes the rows of the table to the pages .html file.
    return render_template('menu.html', rows=rows, user=session.get('user'))


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
            return render_template('addMenuItem.html', error=str(ex))

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

    return redirect('/menu')


@app.route('/editMenuItem', methods=['GET', 'POST'])
def edit_menu_item():
    """Displays all menu items, and allows you to select and delete them."""
    if request.method == 'GET':
        # Render the page to edit the menu.
        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        # Gets all the rows in menu.
        sql_connection.execute("SELECT * FROM menu;")
        rows = sql_connection.fetchall()

        db_manager.close()

        # Passes the rows of the table to editMenuItem.html.
        return render_template('/editMenuItem.html', rows=rows, user=session.get('user'))

    elif request.method == 'POST':

        itemID = request.form['itemID']

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        sql_connection.execute("DELETE FROM menu WHERE itemID = ?", (itemID, ))
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
                return render_template('login.html', error="Invalid credentials", user=session.get('user'))
        except TypeError as ex:
            return render_template('login.html', error=str(ex), user=session.get('user'))
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
                                            request.form['role'])
            try:
                create_account(user_account)
            except TypeError as ex:
                return render_template('login.html', error="Invalid credentials", user=session.get('user'))
        except TypeError as ex:
            return render_template('login.html', error=str(ex), user=session.get('user'))

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

    if request.method == 'GET':

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        # Gets all the rows from menu.
        sql_connection.execute("SELECT * FROM menu;")
        rows = sql_connection.fetchall()

        db_manager.close()

        return render_template('order.html', rows=rows, user=session.get('user'))

    if request.method == 'POST':

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        table_number = int(request.form['tableNumber'])

        sql_connection.execute("INSERT INTO orders (tableNum, paid)"
                               " VALUES (?, ?)", (table_number, 0))

        db_manager.get_db().commit()

        last_row = sql_connection.lastrowid

        sql_connection.execute(
            "SELECT * FROM orders WHERE orderID=?", (last_row,))
        current_order = sql_connection.fetchone()

        session['order'] = [current_order[0],
                            current_order[1], current_order[2]]

        for key, value in request.form.items():

            if key != 'tableNumber':

                if value != '0':

                    sql_connection.execute("INSERT INTO orderDetails "
                                           "(orderID, itemID, customerID, qty, state, order_time) "
                                           "VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                                           (session['order'][0], key, session['user'][0], value, 0))

                    db_manager.get_db().commit()

        db_manager.close()

        return redirect('/orderPayment')


@app.route('/orderPayment', methods=['GET', 'POST'])
def order_payment():

    if request.method == 'GET':

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        sql_connection.execute(
            "SELECT itemID, qty FROM orderDetails WHERE orderID=?", (session['order'][0],))
        orderRows = sql_connection.fetchall()

        menuRows = []
        for orderRow in orderRows:
            sql_connection.execute(
                "SELECT name, price FROM menu WHERE itemID=?", (orderRow[0],))
            menuRow = sql_connection.fetchone()
            menuRows.append(menuRow)

        rows = []
        totalPrice = 0
        for i in range(0, len(menuRows)):
            price = menuRows[i][1] * orderRows[i][1]
            row = [menuRows[i][0], orderRows[i][1], price]
            rows.append(row)
            totalPrice += price

        return render_template('orderPayment.html', rows=rows, totalPrice=totalPrice, user=session.get('user'))
    elif request.method == 'POST':
        # This is where the payment information would be processed.
        return redirect('/orderConformation')


@app.route('/orderConformation', methods=['GET', 'POST'])
def order_conformation():

    if request.method == 'GET':
        return render_template('orderConformation.html', user=session.get('user'))
    elif request.method == 'POST':
        return redirect('/home')


@app.route('/kitchenOrders', methods=['GET', 'POST'])
def kitchen_orders():

    if request.method == 'GET':

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        # Gets all the rows from menu.
        sql_connection.execute(
            "SELECT orderID, itemID, qty, order_time FROM orderDetails WHERE state=1 ORDER BY orderID ASC;")
        rows = sql_connection.fetchall()

        all_orders = {}
        for row in rows:
            if row[0] not in all_orders:
                all_orders[row[0]] = []
            sql_connection.execute(
                "SELECT name FROM menu WHERE itemID=?", (row[1],))
            name = sql_connection.fetchone()
            temp_list = [name[0], row[2], row[3]]
            all_orders[row[0]].append(temp_list)

        db_manager.close()

        return render_template('kitchenOrders.html', all_orders=all_orders, user=session.get('user'))
    elif request.method == 'POST':

        orderID = request.form['orderID']

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        sql_connection.execute(
            "UPDATE orderDetails SET state=2 WHERE orderID=?", (orderID,))
        db_manager.get_db().commit()

        db_manager.close()

        return redirect('/kitchenOrders')


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
def custMenu():
    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute("SELECT * FROM menu;")
    foods = sql_connection.fetchall()

    db_manager.close()

    return render_template('customerMenu.html', foods=foods, user=session.get('user'))


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', user=session.get('user'))


@app.route('/waiterOrders', methods=['GET', 'POST'])
def waiter_order_confirm():

    if request.method == 'GET':

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        # Gets all the rows from menu.
        sql_connection.execute(
            "SELECT orderID, itemID, qty, order_time FROM orderDetails WHERE state=0 ORDER BY orderID ASC;")
        rows = sql_connection.fetchall()

        all_orders = {}
        for row in rows:
            if row[0] not in all_orders:
                all_orders[row[0]] = []
            sql_connection.execute(
                "SELECT name FROM menu WHERE itemID=?", (row[1],))
            name = sql_connection.fetchone()
            sql_connection.execute(
                "SELECT tableNum FROM orders WHERE orderID=?", (row[0],))
            tableNum = sql_connection.fetchone()
            temp_list = [name[0], tableNum[0], row[2], row[3]]
            all_orders[row[0]].append(temp_list)

        db_manager.close()

        return render_template('waiterOrderConfirm.html', all_orders=all_orders, user=session.get('user'))

    elif request.method == 'POST':
        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        orderID = request.form['orderID']

        # Update the orderDetails table
        sql_connection.execute(
            "UPDATE orderDetails SET state=1 WHERE orderID=?", (orderID,))
        db_manager.get_db().commit()

        db_manager.close()

        return redirect('/waiterOrders')


@app.route('/waiterOrdersCancel', methods=['GET', 'POST'])
def waiter_order_cancel():

    if request.method == 'GET':
        return redirect('/waiterOrders')
    elif request.method == 'POST':
        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        orderID = request.form['orderID']

        # Update the orderDetails table
        sql_connection.execute(
            "UPDATE orderDetails SET state=5 WHERE orderID=?", (orderID,))
        db_manager.get_db().commit()

        db_manager.close()

        return redirect('/waiterOrders')


@app.route('/waiterOrdersDelivered', methods=['GET', 'POST'])
def waiter_order_delivered():

    if request.method == 'GET':

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        # Gets all the rows from menu.
        sql_connection.execute(
            "SELECT orderID, itemID, qty, order_time FROM orderDetails WHERE state=2 ORDER BY orderID ASC;")
        rows = sql_connection.fetchall()

        all_orders = {}
        for row in rows:
            if row[0] not in all_orders:
                all_orders[row[0]] = []
            sql_connection.execute(
                "SELECT name FROM menu WHERE itemID=?", (row[1],))
            name = sql_connection.fetchone()
            sql_connection.execute(
                "SELECT tableNum FROM orders WHERE orderID=?", (row[0],))
            tableNum = sql_connection.fetchone()
            temp_list = [name[0], tableNum[0], row[2], row[3]]
            all_orders[row[0]].append(temp_list)

        db_manager.close()

        return render_template('waiterOrderDeliver.html', all_orders=all_orders, user=session.get('user'))
    elif request.method == 'POST':
        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        orderID = request.form['orderID']

        # Update the orderDetails table
        sql_connection.execute(
            "UPDATE orderDetails SET state=3 WHERE orderID=?", (orderID,))
        db_manager.get_db().commit()

        db_manager.close()

        return redirect('/waiterOrdersDelivered')


@app.route('/manageAccounts', methods=['GET', 'POST'])
def manage_accounts():

    if request.method == 'GET':

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        sql_connection.execute(
            "SELECT userID, first_name, last_name, role FROM users")
        rows = sql_connection.fetchall()

        db_manager.close()

        return render_template('managerAccounts.html', rows=rows, user=session.get('user'))

    elif request.method == 'POST':

        firstName = request.form['firstName']
        lastName = request.form['lastName']

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        sql_connection.execute("SELECT userID, first_name, last_name, role"
                               " FROM users WHERE first_name=? AND last_name=?;", (firstName, lastName))
        rows = sql_connection.fetchall()

        db_manager.close()

        return render_template('managerAccounts.html', rows=rows, user=session.get('user'))


@app.route('/manageAccountsEdit', methods=['GET', 'POST'])
def manage_accounts_edit():

    if request.method == 'GET':
        return redirect('/manageAccounts')
    elif request.method == 'POST':

        userID = request.form['userID']
        role = request.form['role']

        db_manager = DBManager(app)
        sql_connection = db_manager.get_connection()

        sql_connection.execute(
            "UPDATE users SET role=? WHERE userID=?", (role, userID))
        db_manager.get_db().commit()

        db_manager.close()

        return redirect('/manageAccounts')


@app.route('/assign_table', methods=['POST'])
def assign_table():
    waiter_id = request.form.get('waiter_id')
    tableNum = request.form.get('tableNum')

    db_manager = DBManager(app)
    sql_connection = db_manager.get_connection()

    sql_connection.execute('SELECT waiter_id FROM table_assignments WHERE table_id=?', (tableNum,))
    result = sql_connection.fetchone()
    if result:
        return 'Table', tableNum, 'is already assigned to waiter', (result[0])
    sql_connection.execute('INSERT INTO table_assignments (table_id, waiter_id) VALUES (?, ?)', (tableNum, waiter_id))
    db_manager.get_db().commit()
    db_manager.close()

    return 'Table', tableNum, 'has been assigned to waiter', waiter_id


@app.route('/customerOrders')
def customer_orders():

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

    print(all_orders)

    db_manager.close()

    return render_template('customerOrderTracking.html', all_orders=all_orders, user=session.get('user'))
