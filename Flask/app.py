from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

#Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'jgillis8'
app.config['MYSQL_PASSWORD'] = '3mkwN8wO'
app.config['MYSQL_DB'] = 'jgillis8'

#Initialize MySQL
mysql = MySQL(app)



#index file
@app.route('/')
def index():
    if('loggedin') in session and 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')
    
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    if 'loggedin' not in session:
        return redirect('./login')
    if request.method == 'POST' and 'product_id' in request.form:
        # Get the product ID from the form data
        product_id = request.form.get('product_id')
        if product_id:
            # Check if the user is logged in
            if 'loggedin' in session:
                # Get the customer ID from the session
                customer_id = session['id']

                # Insert the item into the cart table
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE quantity = quantity + 1", (customer_id, product_id))
                mysql.connection.commit()
                cursor.close()
                flash('Product added to cart.', 'success')
            else:
                flash('Please log in to add products to the cart.', 'error')
        search_query = request.form.get('search')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM product WHERE product_name LIKE %s", ('%' + search_query + '%',))
        search_query = cursor.fetchall()
        cursor.close()
        return render_template('catalog.html', Products=search_query)
    elif request.method == 'POST' and 'search' in request.form:
        search = request.form['search']
        if search:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM product WHERE product_name LIKE %s", ('%' + search + '%',))
            search_query = cursor.fetchall()
            cursor.close()
            return render_template('catalog.html', Products=search_query)


    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM product")
    data = cursor.fetchall()
    cursor.close()
    return render_template('catalog.html', Products=data)

@app.route('/Profile', methods=['GET', 'POST'])
def Profile():
    msg=''
    if('loggedin') in session:
        current_customerID = session['id']
        if request.method == 'POST':
            
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #if 'first_name' in request.form:
                #sql query insert FirstName into customer
                #change first name
            #if 'last_name' in request.form:
            if 'first_name' in request.form:
                first_name = request.form['first_name']
                cursor.execute("""INSERT INTO customer(customer_ID, FirstName)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE
                                FirstName=VALUES(FirstName)""",
                                (current_customerID, first_name))
            if 'last_name' in request.form:
                last_name = request.form['last_name']
                cursor.execute("""INSERT INTO customer(customer_ID, LastName)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE
                                LastName=VALUES(LastName)""",
                                (current_customerID, last_name))
            if 'email' in request.form:
                email = request.form['email']
                cursor.execute("""INSERT INTO customer(customer_ID, email)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE
                                email=VALUES(email)""",
                                (current_customerID, email))
            if 'street_num' in request.form:
                street_num = request.form['street_num']
                cursor.execute("""INSERT INTO customer(customer_ID, street_number)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE
                                street_number=VALUES(street_number)""",
                                (current_customerID, street_num))
            if 'city' in request.form:
                city = request.form['city']
                cursor.execute("""INSERT INTO customer(customer_ID, city)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE
                                city=VALUES(city)""",
                                (current_customerID, city))
            if 'street' in request.form:
                street = request.form['street']
                cursor.execute("""INSERT INTO customer(customer_ID, street_name)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE
                                street_name=VALUES(street_name)""",
                                (current_customerID, street))
            if 'first_name' in request.form:
                first_name = request.form['first_name']
                cursor.execute("""INSERT INTO customer(customer_ID, FirstName)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE
                                FirstName=VALUES(FirstName)""",
                                (current_customerID, first_name))
            if 'apt_num' in request.form:
                apt_num = request.form['apt_num']
                cursor.execute("""INSERT INTO customer(customer_ID, apt_num)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE
                                apt_num=VALUES(apt_num)""",
                                (current_customerID, apt_num))
            if 'zip_code' in request.form:
                zip_code = request.form['zip_code']
                cursor.execute("""INSERT INTO customer(customer_ID, zip_code)
                                VALUES (%s, %s)
                                ON DUPLICATE KEY UPDATE
                                zip_code=VALUES(zip_code)""",
                                (current_customerID, zip_code))
            #cursor.execute('INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (current_username, first_name, last_name, email, street_num, street,
            #apt_num, city, zip_code, ))
            mysql.connection.commit()
            msg = 'You have successfully changed your profile information'
            cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM customer WHERE customer_ID = %s", (current_customerID,))
        user_data = cursor.fetchone()  # Assuming there's only one row per customer ID
        cursor.close()
        return render_template('profilein.html', user_data=user_data)
    else:
        return redirect(url_for('login'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle POST request to remove a product from the cart
        if 'loggedin' in session:
            remove = request.form['product_id']
            if remove:
                # Retrieve the customer ID from the session
                customer_id = session['id']
                # Delete the item from the cart table
                mysql.connection.cursor()
                cursor = mysql.connection.cursor()
                
                cursor.execute("DELETE FROM cart WHERE customer_id = %s AND product_id = %s", (customer_id, remove))
                mysql.connection.commit()
                flash('Product removed from cart.', 'success')
                cursor.close()
        else:
            flash('Please log in to remove products from the cart.', 'error')
        return redirect(url_for('cart'))

    # Handle GET request to display the cart
    if 'loggedin' in session:
        # Retrieve the customer ID from the session
        customer_id = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT p.*, c.quantity FROM product p INNER JOIN cart c ON p.product_ID = c.product_ID WHERE c.customer_ID = %s", (customer_id,))
        products = cursor.fetchall()
         
        sum = 0
        quantities=[]
        for item in products:
             product_id = item[0]  
             price = item[4]
             cursor.execute('SELECT quantity FROM cart WHERE product_ID = %s AND customer_ID = %s', (product_id, session['id']))
             quantity= cursor.fetchone()
             if quantity:
                sum+=quantity[0]*price
                quantities.append(quantity[0])

        cursor.close()

        return render_template('cart.html', products=products, total_price=sum ,total_quantity=quantities)
    else:
        flash('Please log in to view your cart.', 'error')
        return redirect(url_for('login'))


@app.route('/checkout', methods=['GET' , 'POST'])
def checkout():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    order = False
    if request.method == 'POST' and 'card' in request.form:
        order = True
        card = request.form['card']

    # Retrieve the customer ID from the session
    customer_id = session['id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT p.*, c.quantity FROM product p INNER JOIN cart c ON p.product_ID = c.product_ID WHERE c.customer_ID = %s", (customer_id,))
    products = cursor.fetchall()
        
    sum = 0
    quantitys=[]
    for item in products:
        product_id = item[0]  
        price = item[4]
        cursor.execute('SELECT quantity FROM cart WHERE product_ID = %s AND customer_ID = %s', (product_id, session['id']))
        quantity= cursor.fetchone()
        if quantity:
            sum+=quantity[0]*price
            quantitys.append(quantity[0])

    #Retrieve Payment Information for selected customer
    customer_id = session.get('id')

    #SQL query for retrieving payment information
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT card_number FROM payment WHERE customer_ID = %s", (customer_id,))
    existing_payments = cursor.fetchall()
    cursor.close()

    #store store order in database and everything in cart
    if order == True:
        #cursor.mysql.connection.cursor()
        count = 0
        for product in products:
            product_name = product[0]
            quantity = quantitys[count]

            #increment orders_ID
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT MAX(orders_ID) from orders")
            maxpayment = cursor.fetchone()
            cursor.close()
            maxpayment = maxpayment[0]
            maxpayment += 1
            
            #insert order into orders table
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT MAX(orders_ID) from orders")
            maxpayment = cursor.fetchone()
            cursor.close()

            count+=1

    return render_template('checkout.html',total_price=sum, cards=existing_payments, Products=products, quantity=quantitys)



@app.route('/login', methods=['GET','POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('index'))
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (escape(username),))
        account = cursor.fetchone()
        cursor.close()
        if account and check_password_hash(account['password'],password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect('/')
        else:
            return render_template('/login.html', error = 'Incorrect username/Password!')
    return render_template('/login.html')
  

@app.route('/payment', methods=['GET','POST'])
def payment():
    # Check if logged in 
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    # Retrieve customer_ID from session
    customer_id = session.get('id')

    # Display current payment info for the logged-in user
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT card_number FROM payment WHERE customer_ID = %s", (customer_id,))
    existing_payments = cursor.fetchall()
    cursor.close()

    # Form for adding payment info 
    if request.method == 'POST' and 'cardNum' in request.form and 'date' in request.form and 'cvc' in request.form and 'zip' in request.form:
        cardNum = request.form['cardNum']
        date = request.form['date']
        cvc = request.form['cvc']
        zip = request.form['zip']

        # Adding info to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "INSERT INTO payment (customer_ID, card_number, expiration_date, security_code) VALUES (%s, %s, %s, %s)"
        values = (customer_id, cardNum, date, cvc)
        cursor.execute(sql, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('payment'))

    elif request.method == 'POST' and 'remove_payment' in request.form:
        cardNum = request.form['remove_payment']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "DELETE FROM payment WHERE customer_ID = %s AND card_number = %s"
        values = (customer_id, cardNum)
        cursor.execute(sql, values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('payment'))

    return render_template('/payment.html', existing_payments=existing_payments)


@app.route('/register', methods=['GET','POST'])
def register():
    if('loggedin') in session and 'username' in session:
        return redirect(url_for('index'))

    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password = generate_password_hash(password)
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg='Account with that username already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, hashed_password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered! Please sign in!'
        cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out registration form!'
    return render_template('/register.html', error=msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    session.pop('loggedin', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='localhost', port=5005)