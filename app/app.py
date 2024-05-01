from flask import Flask, flash, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import hashlib
import random
import string

 
app = Flask(__name__, static_url_path='/static')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'tradeforge'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Return query results as dictionaries

mysql = MySQL(app)
app.secret_key = "123456"


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        socialid = generate_social_id()

        if not is_username_available(username):
            flash("Username is already taken. Please choose another one.", "error")
            return render_template('signup.html')
        

        # Check if email is available
        if not is_email_available(email):
            flash("Email is already registered. Please use another one.", "error")
            return render_template('signup.html')


        hashPassword =  hashlib.md5(password.encode()).hexdigest()

        cursor = mysql.connection.cursor()

        cursor.execute("INSERT INTO Users (UserName, PasswordHash, Email, SocialId) VALUES (%s, %s, %s, %s)",
                       (username, hashPassword, email,socialid ))
        
        mysql.connection.commit()

        # Close connection
        cursor.close()
        flash("SIGNED UP SUCCESSFULLY!!!")
        # NEED USERNAME CHECK 

        
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query to fetch user from database
        cur.execute("SELECT * FROM Users WHERE UserName = %s", (username,))
        user = cur.fetchone()

        # Close cursor
        cur.close()

        if user:
            if user['PasswordHash'] == hashlib.md5(password.encode()).hexdigest():  # Check if passwords match
                # Store user information in session
                session['user_id'] = user['Id']
                session['username'] = user['UserName']
                return render_template('main.html')
            else:
                error = "Incorrect password. Please try again."
                flash("WRONG PASSWORD OR USER NAME!!!")
                return render_template('signin.html', error=error)
        else:
            error = "User not found. Please check your username."
            flash("USER NAME NOT FOUND!!!")

            return render_template('signin.html', error=error)

    return render_template('signin.html')



@app.route('/about')
def about():
    return render_template('about.html')




def generate_social_id(length=10):
    # Define the characters to choose from
    characters = string.ascii_uppercase + string.digits

    # Generate random string
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string


def is_username_available(username):
    """Check if the username is available (not already used)."""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM Users WHERE UserName = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    return result['count'] == 0

def is_email_available(email):
    """Check if the email is available (not already used)."""
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM Users WHERE Email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    return result['count'] == 0

if __name__ == "__main__":
    app.run(debug=True)



#░██████╗███████╗██╗░░░██╗███████╗██████╗░███████╗██╗░░██╗
#██╔════╝██╔════╝██║░░░██║██╔════╝██╔══██╗██╔════╝██║░██╔╝
#╚█████╗░█████╗░░╚██╗░██╔╝█████╗░░██████╔╝█████╗░░█████═╝░
#░╚═══██╗██╔══╝░░░╚████╔╝░██╔══╝░░██╔══██╗██╔══╝░░██╔═██╗░
#██████╔╝███████╗░░╚██╔╝░░███████╗██║░░██║███████╗██║░╚██╗
#╚═════╝░╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝

#░█████╗░██╗░░░░░███████╗░█████╗░███████╗░██████╗░██╗███╗░░░███╗
#██╔══██╗██║░░░░░██╔════╝██╔══██╗██╔════╝██╔════╝░██║████╗░████║
#██║░░██║██║░░░░░█████╗░░██║░░╚═╝█████╗░░██║░░██╗░██║██╔████╔██║
#██║░░██║██║░░░░░██╔══╝░░██║░░██╗██╔══╝░░██║░░╚██╗██║██║╚██╔╝██║
#╚█████╔╝███████╗███████╗╚█████╔╝███████╗╚██████╔╝██║██║░╚═╝░██║
#░╚════╝░╚══════╝╚══════╝░╚════╝░╚══════╝░╚═════╝░╚═╝╚═╝░░░░░╚═╝