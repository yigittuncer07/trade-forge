from flask import Flask, flash, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import hashlib
import random
import string
import requests
from decimal import Decimal


cryptocurrency_ids = [328, 1, 1027,825,994]
API_KEY = '6db83039-54e6-48c2-986d-681f46586926'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

params = {
    'id': ','.join(map(str, cryptocurrency_ids)),
    'convert': 'USD'  # Convert prices to USD
}

# Headers with API key
headers = {
    'X-CMC_PRO_API_KEY': API_KEY
}

# Send GET request to the API
response = requests.get(url, params=params, headers=headers)

app = Flask(__name__, static_url_path='/static')
session_user_id = 0

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'tradeforge'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Return query results as dictionaries

mysql = MySQL(app)
app.secret_key = "123456"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')
    
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/buy/<crypto_id>', methods=['GET', 'POST'])
def buy(crypto_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT Cryptos.Name, Assets.Amount, Assets.CryptoId FROM Assets JOIN Cryptos ON Assets.CryptoId = Cryptos.ID WHERE Assets.UserId = %s",(session_user_id,))
    wallet = cur.fetchall()
    cur.close()

    tether_amount = 0
    is_new_crypto = True


    for crypto_data in wallet:
        # Check if CryptoId is 825
        if crypto_data['CryptoId'] == 825:
            # Extract the amount
            tether_amount = crypto_data['Amount']
            break  # Stop iterating once found

    for crypto_data in wallet:
        if int(crypto_data['CryptoId']) == int(crypto_id):
            is_new_crypto = False
            break  # Stop iterating once found

  
    
    amount = float(request.form.get('buyamount')) # Retrieving amount from form data

    tether_amount = float(tether_amount)

    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    crypto_data = data['data'][str(crypto_id)]
    crypto_price = float(crypto_data['quote']['USD']['price'])



    if amount*crypto_price <= tether_amount:
        tether_amount = tether_amount - amount*crypto_price

        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE assets SET Amount = %s WHERE UserId = %s AND CryptoId = %s", (tether_amount, session_user_id, 825))

        if is_new_crypto:
            cur.execute("INSERT INTO assets (UserId, CryptoId, Amount) VALUES (%s, %s, %s);", (session_user_id, crypto_id, amount))
        else:
            cur.execute("UPDATE assets SET Amount = Amount + %s WHERE UserId = %s AND CryptoId = %s", (amount, session_user_id, crypto_id))
            
        mysql.connection.commit()
        cur.close()
        error = "Successful."
        flash("ACTION COMPLETED!", "success")
        return redirect(url_for('sellbuy', crypto_id=crypto_id))
    else:
        error = "Error."
        flash("ACTION NOT COMPLETED! YOU DON'T HAVE ENOUGH TETHER", "error")
        return redirect(url_for('sellbuy', crypto_id=crypto_id))
        
    



                

  
    



@app.route('/wallet')
def wallet():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Cryptos.Name, Assets.Amount, Assets.CryptoId FROM Assets JOIN Cryptos ON Assets.CryptoId = Cryptos.ID WHERE Assets.UserId = %s",(session_user_id,))
    wallet = cur.fetchall()
    cur.close()
    # Make a GET request to the endpoint 
    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    total_wallet_value = calculate_total_wallet_value(wallet,data)

    return render_template('wallet.html', wallet = wallet, data = data, total_wallet_value = total_wallet_value)

@app.route('/logout')
def logout():
    update_session_user_id(-1)
    return redirect('/index')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/sellbuy<crypto_id>')
def sellbuy(crypto_id):

    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Cryptos")
    cryptos = cur.fetchall()
    cur.close()
    
    crypto_name = ""

    for crypto in cryptos:
        if str(crypto['Id']) == str(crypto_id):
            crypto_name = crypto['Name']
            break  # Once the correct name is found, you can exit the loop

    crypto_price = data['data']["%s" % (crypto_id,)]['quote']['USD']['price']



    return render_template('sellbuy.html', crypto_id = crypto_id, crypto_name = crypto_name, crypto_price = crypto_price)

@app.route('/market')
def market():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Cryptos")
    cryptos = cur.fetchall()
    cur.close()

    # Make a GET request to the endpoint
    response = requests.get(url, headers=headers, params=params)

    data = response.json()


    return render_template('market.html', cryptos=cryptos, data=data)


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
                update_session_user_id(user['Id'])

                return redirect("/main")
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

def update_session_user_id(new_user_id):
    global session_user_id
    session_user_id = new_user_id

def calculate_total_wallet_value(wallet_data, crypto_data):
    total_value = Decimal('0')
    
    for asset in wallet_data:
        crypto_id = str(asset['CryptoId'])
        amount = asset['Amount']
        
        if crypto_id in crypto_data['data']:
            price = crypto_data['data'][crypto_id]['quote']['USD']['price']
            total_value += Decimal(amount) * Decimal(price)
    
    return total_value

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