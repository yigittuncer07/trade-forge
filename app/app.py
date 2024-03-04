from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/signin.html')
def signin():
    return render_template('signin.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)