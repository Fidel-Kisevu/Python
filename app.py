# Import necessary modules and functions from Flask and MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL  # Flask extension to simplify MySQL integration
import MySQLdb.cursors  # Cursors provide ways to interact with database query results

# Initialize a Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'  # The hostname or IP address of your MySQL server
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'pyproject'  # The name of the database you want to use

# Initialize MySQL connection with the Flask app
mysql = MySQL(app)

# Route for the home page
@app.route("/")
def home():
    # Render the 'home.html' template when a user visits the home page
    return render_template("home.html")

# Route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":  # Check if the form is submitted via POST
        # Get the username and password from the form
        username = request.form["username"]
        password = request.form["password"]
        
        # Create a cursor to execute MySQL queries
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Execute a SELECT query to check if a user with the provided username exists
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        # Fetch one record (if found)
        account = cursor.fetchone()
        
        # Check if the account exists
        if account:
            # Verify if the provided password matches the stored password
            if account['password'] == password:
                # Redirect the user to the home page if login is successful
                return redirect(url_for("home"))
            else:
                # Flash a message if the password is incorrect
                flash("Incorrect password. Please try again.")
                return redirect(url_for("login"))
        else:
            # Flash a message if the username does not exist
            flash("Username does not exist. Please sign up.")
            return redirect(url_for("login"))
    
    # If the request method is GET (i.e., the user is just visiting the page), render the login page
    return render_template("login.html")

# Route for the sign-up page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":  # Check if the form is submitted via POST
        # Get the username and password from the form
        username = request.form["username"]
        password = request.form["password"]
        
        # Create a cursor to execute MySQL queries
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        account = cursor.fetchone()

        if account:
            # Flash a message if the username is already taken
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for("signup"))
        else:
            try:
                # Execute an INSERT query to add the new user to the database
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                # Commit the transaction to save the new user in the database
                mysql.connection.commit()
                # Redirect the user to the login page after successful sign-up
                return redirect(url_for("login"))
            except MySQLdb.IntegrityError as e:
                # Handle other possible integrity errors
                flash(f"An error occurred: {e}")
                return redirect(url_for("signup"))
    
    # If the request method is GET (i.e., the user is just visiting the page), render the sign-up page
    return render_template("signup.html")

# Run the application if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for easier debugging during development
