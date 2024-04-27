from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from markupsafe import escape
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

#Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'cblaha1'
app.config['MYSQL_PASSWORD'] = 'Uq2pg8gG'
app.config['MYSQL_DB'] = 'cblaha1'

#Initialize MySQL
mysql = MySQL(app)

#index file
@app.route('/')
def index():
    if('loggedin') in session:
        print('HELLO')
    if('username') in session:
        print('yes')
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')
    

#catalog
@app.route('/catalog')
def catalog():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from product")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    return render_template('catalog.html',Products=data)

@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        cursor.close()
        if account:
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
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
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
    app.run(host='localhost', port=5005)