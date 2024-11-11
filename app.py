from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = 'your_secret_key'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'  # Replace with your actual password
app.config['MYSQL_DB'] = 'flask_users'

mysql = MySQL(app)

# Calculate 1RM function
def calculate_1rm(weight, reps):
    return weight * (1 + reps / 30)

# Calculate percentages
def calculate_percentages(one_rm):
    percentages = {}
    for reps in range(1, 16):  # Reps from 1 to 15
        percentage = 1 - (reps - 1) * 0.03  # Rough estimate per rep
        percentages[reps] = round(one_rm * percentage, 2)  # Round to 2 decimal places
    return percentages

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    percentages = None
    if request.method == 'POST':
        weight = float(request.form['weight'])
        reps = int(request.form['reps'])
        
        # Calculate 1RM
        result = calculate_1rm(weight, reps)
        
        # Calculate percentages
        percentages = calculate_percentages(result)
    
    return render_template('home.html', result=result, percentages=percentages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM tbl_users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and bcrypt.check_password_hash(user[1], pwd):
            session['username'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        hashed_pwd = bcrypt.generate_password_hash(pwd).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_users (username, password) VALUES (%s, %s)", (username, hashed_pwd))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
