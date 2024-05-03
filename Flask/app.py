from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
import re
import os
print(os.getcwd())



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
    


#catalog
@app.route('/catalog')
def catalog():
    cursor = mysql.connection.cursor()
    with open('/users/kent/student/jgillis8/Database-Project/Flask/schema.sql') as f:
        cursor.execute(f.read())
    #with open('/users/kent/student/jgillis8/Database-Project/Flask/data.sql') as g:
    #    cursor.execute(g.read())
    cursor.execute("SELECT * from product")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    return render_template('catalog.html',Products=data)

@app.route('/Profile', methods=['GET', 'POST'])
def Profile():
    msg=''
    if('loggedin') in session and 'username' in session:
        current_username = session['username']
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            street = request.form['street']
            street_num = request.form['street_num']
            apt_num = request.form['apt_num']
            city = request.form['city']
            zip_code = request.form['zip_code']
            email=request.form['email']
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #cursor.execute('INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (current_username, first_name, last_name, email, street_num, street,
            #apt_num, city, zip_code, ))
            cursor.execute("""INSERT INTO customer (customer_ID, FirstName, LastName, email, street_number, street_name, apt_num, city, zip_code)
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                              ON DUPLICATE KEY UPDATE
                              FirstName = VALUES(FirstName),
                              LastName = VALUES(LastName),
                              email = VALUES(email),
                              street_number = VALUES(street_number),
                              street_name = VALUES(street_name),
                              apt_num = VALUES(apt_num),
                              city = VALUES(city),
                              zip_code = VALUES(zip_code)""",
                           (current_username, first_name, last_name, email, street_num, street, apt_num, city, zip_code))
            mysql.connection.commit()
            msg = 'You have successfully changed your profile information'
            cursor.close()

        return render_template('profilein.html')
    else:
        return redirect(url_for('login'))

    #cursor = mysql.connection.cursor()
    #cursor.execute("SELECT * from product")
    #mysql.connection.commit()
    #data = cursor.fetchall()
    #cursor.close()
    #return render_template('catalog.html',Products=data)

@app.route('/login', methods=['GET','POST'])
def login():
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

@app.route('/register', methods=['GET','POST'])
def register():
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
            msg = 'You have successfully registered!'
        cursor.close()
    elif request.method == 'POST':
        msg = 'Please fill out registration form!'
    return render_template('/register.html', error=msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('id', None)
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='localhost', port=5006)
