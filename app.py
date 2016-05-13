from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    """
    home: returns the home page
    
    Returns:
        the home page
    """
    return ""

@app.route('/login')
def login_page():
    """
    login_page: returns the login page

    Returns:
        the login page
    """
    return ""

@app.route('/login', methods = ['GET', 'POST'])
def login_check():
    """
    login_check: returns the check page for login
    
    Returns:
        the approporiate page
    """
    return ""

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, debug = True)
