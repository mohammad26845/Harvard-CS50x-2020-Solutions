import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
# added
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get portfolio information from Table
    rows = db.execute("SELECT * FROM stocks WHERE user_id = :user", user=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]['cash']

    total = cash
    data_array = []

    for row in rows:

        temp_dict = {}
        # Get Stock info
        stock_info = lookup(row['symbol'])

        # Create new dict
        temp_dict["symbol"] = stock_info['symbol']
        temp_dict["name"] = stock_info['name']
        temp_dict["amount"] = row["amount"]
        temp_dict["price"] = stock_info['price']
        temp_dict["total"] = stock_info['price'] * row['amount']

        # calc sum of stock's price
        total += temp_dict["total"]

        # Change INT format To currency format
        temp_dict["price"] = "$ {:,.2f}".format(temp_dict["price"])
        temp_dict["total"] = "$ {:,.2f}".format(temp_dict["total"])

        # ADD dict to array list
        data_array.append(temp_dict)

    # Show index page
    return render_template("index.html", stock_data = data_array, total = "$ {:,.2f}".format(total) , cash = "$ {:,.2f}".format(cash))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Obtain the data for transaction
        amount = int(request.form.get("shares"))
        symbol = lookup(request.form.get("symbol"))

        # Control the stock symbol
        if not symbol:
            return apology("Could not find the stock")

        # Control the amount value
        if amount <= 0 :
            return apology("Enter the stock amount correctly")

        # Get price of symbol
        price = symbol['price']

        # get Remaining money of user
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user = session["user_id"])[0]['cash']

        # Calc Remaining money
        remaining_money = cash - price * float(amount)


        # Check current cash
        if remaining_money < 0:
            return apology("You don't have enough money for this transaction")


        # Check if user already has one or more stocks
        stock = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol",
                           user=session["user_id"],
                           symbol = symbol['symbol'])


        # Insert new row into STOCKS
        if not stock:
            db.execute("INSERT INTO stocks(user_id, symbol, amount, price) VALUES (:user, :symbol, :amount, :price)",
                       user=session["user_id"],
                       symbol = symbol['symbol'],
                       amount = amount,
                       price = symbol['price'])


        # update stock table
        else:
            sum_amount = amount + stock[0]['amount']

            db.execute("UPDATE stocks SET amount = :amount, price = :price WHERE user_id = :user AND symbol = :symbol",
                       user=session["user_id"],
                       symbol = symbol['symbol'],
                       amount = sum_amount,
                       price = symbol['price'])

        # Update Cash of user
        db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash = remaining_money, user = session["user_id"])


        # Update history table
        # set date string
        now = datetime.datetime.now()
        dstring = str(now.strftime("%Y-%m-%d %H:%M:%S"))

        db.execute("INSERT INTO transactions (user_id, symbol, amount, price, time) VALUES (:user, :symbol, :amount, :price, :n_time)",
                   user=session["user_id"],
                   symbol = symbol['symbol'],
                   amount = amount, price = symbol['price'],
                   n_time = dstring)

        # Redirect user to index page
        flash("Bought: ("+str(symbol['symbol'])+", $ "+str(amount * symbol['price'])+")")
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get portfolio information from Table
    rows = db.execute("SELECT * FROM transactions WHERE user_id = :user", user=session["user_id"])

    data_array = []
    for row in rows:

        temp_dict = {}

        # Create new dict
        temp_dict["symbol"] = row['symbol']
        temp_dict["amount"] = row["amount"]
        temp_dict["price"] = row['price']
        temp_dict["time"] = row['time']

        # Calc action
        if temp_dict["amount"] < 0:
            temp_dict["action"] = "SELL"
        else:
            temp_dict["action"] = "BUY"

        # Change INT format To currency format
        temp_dict["price"] = "$ {:,.2f}".format(temp_dict["price"])

        # ADD dict to array list
        data_array.append(temp_dict)

    return render_template("history.html", history_data = data_array)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username = request.form.get("username"))

        # Ensure username exists and password is correct
        if rows:
            # check hash password
            hash_pwd = check_password_hash(rows[0]["hash"], request.form.get("password"))
            # check input password
            if hash_pwd:
                # Create session Remember which user has logged in
                session["user_id"] = rows[0]["id"]

                # send msg (welcome back user)
                flash("Welcome back "+str(request.form.get("username")))
                # Redirect user to home page
                return redirect("/")

            else:
                flash("Invalid password")
                return render_template("login.html")
        else:
            flash("Invalid username and/or password")
            return render_template("login.html")


    # User reached route via GET
    else:
        # show login page
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST
    if request.method == "POST":

        # Check input symbol
        if request.form.get("symbol"):
            # Get symbol price
            stock = lookup(request.form.get("symbol"))

            if not stock:
                return apology("Could not find the stock")

            else:
                return render_template("quote.html", stock=stock)

        else:
            return apology("Must provide symbol name.")

    # User reached route via GET
    else:
        # return "not stock"
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # If receive POST method
    if request.method == "POST":

        username = request.form.get("username")
        # ensure username was submitted
        if not username:
            flash("Must provide username.")
            return render_template("register.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password.")
            return render_template("register.html", username = username)

        # ensure second password was submitted
        elif not request.form.get("cpassword"):
            flash("Must confirm password.")
            return render_template("register.html", username = username)

        # ensure passwords match
        elif request.form.get("password") != request.form.get("cpassword"):
            flash("Passwords must match")
            return render_template("register.html", username = username)

        # ensure username already exists
        elif db.execute("SELECT * FROM users WHERE username = :username", username=username):
            flash("Username already taken")
            return render_template("register.html")

        # Create new user
        else:
            # Create hash of the password
            hash_pwd = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

            # Add user to table
            db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)",
                       username = username,
                       hash=hash_pwd)

            # Read database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username = username)

            # Save user to session (Remember which user has logged in)
            session["user_id"] = rows[0]["id"]

            # Redirect to home page
            flash("Welcome "+str(username))
            return redirect("/")

    # If receive GET method
    else:
        # Show register page
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get and collect form informations
        amount = request.form.get("amount")
        symbol = request.form.get("symbol")
        get_symbol = lookup(symbol)


        # check input amount
        if not amount:
            return apology("Enter Shares correctly")

        elif int(amount) <= 0:
            return apology("volume must be integer greater than 0")

        # if error looking stock up
        elif not get_symbol:
            return apology("that stock symbol doesn't exist")

        else:

            # check if user already owns any stock in this company
            existing = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol",
                                  symbol = symbol,
                                  user = session["user_id"])

            if not existing:
                return apology("you don't own this stock")

            else:

                amount = int(amount)
                amount_before = existing[0]['amount']
                amount_after = amount_before - amount

                if amount_after < 0:
                    return apology('you cannot sell more shares than you own')

                elif amount_after == 0:
                    db.execute("DELETE FROM stocks WHERE user_id = :user AND symbol = :symbol",
                               symbol = symbol,
                               user = session["user_id"])

                else:
                    # Update stocks table
                    db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user AND symbol = :symbol",
                               symbol = symbol,
                               user = session["user_id"],
                               amount = amount_after)


                # Calc and Update user's cash
                cash = db.execute("SELECT cash FROM users WHERE id = :user",
                                  user = session["user_id"])[0]['cash']

                cash_after = cash + (get_symbol["price"] * float(amount))

                db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                           cash = cash_after,
                           user = session["user_id"])
                           

                # Update history table
                # set date string
                now = datetime.datetime.now()
                dstring = str(now.strftime("%Y-%m-%d %H:%M:%S"))

                db.execute("INSERT INTO transactions (user_id, symbol, amount, price, time) VALUES (:user, :symbol, :amount, :price, :n_time)",
                           user = session["user_id"],
                           symbol = symbol,
                           amount = -amount,
                           price = get_symbol["price"],
                           n_time = dstring)


                 # Redirect user to home page with success message
                flash("Sold: ("+str(get_symbol['symbol'])+", $ "+str(get_symbol["price"]*float(amount))+")")
                return redirect("/")

    # User reached route via GET
    else:

        # query database with the transactions history
        rows = db.execute("SELECT * FROM stocks WHERE user_id = :user", user=session["user_id"])

        data_array = []
        for row in rows:

            temp_dict = {}
            # Get Stock info
            stock_info = lookup(row['symbol'])

            # Create new dict
            temp_dict["symbol"] = row['symbol']
            temp_dict["amount"] = row["amount"]
            temp_dict["price"] = row['price']
            temp_dict["n_price"] = stock_info['price']

             # Change INT format To currency format
            temp_dict["price"] = "$ {:,.2f}".format(temp_dict["price"])
            temp_dict["n_price"] = "$ {:,.2f}".format(temp_dict["n_price"])

            # ADD dict to array list
            data_array.append(temp_dict)


        # Send a dictionary of stocks
        return render_template("sell.html", rows = data_array)


@app.route("/change_pass", methods=["GET", "POST"])
@login_required
def change_pass():
    """Change user password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure OLD password was submitted
        if not request.form.get("old_pass"):
            flash("Must provide Old password.")
            return render_template("change_pass.html")

        # ensure New password was submitted
        elif not request.form.get("new_pass"):
            flash("Must provide New password.")
            return render_template("change_pass.html")

        # ensure second password was submitted
        elif not request.form.get("cpassword"):
            flash("Must confirm password.")
            return render_template("change_pass.html")

        # ensure passwords match
        elif request.form.get("new_pass") != request.form.get("cpassword"):
            flash("Passwords must match")
            return render_template("change_pass.html")

        else:

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE id = :user_id",
                              user_id = session["user_id"])

            # check hash password
            hash_pwd = check_password_hash(rows[0]["hash"], request.form.get("old_pass"))

            # check input password
            if hash_pwd:

                # Create hash of the password
                hash_pwd = generate_password_hash(request.form.get("new_pass"), method = 'pbkdf2:sha256', salt_length = 8)

                # Update Hash of user password
                db.execute("UPDATE users SET hash = :hash_pwd WHERE id = :user",
                           hash_pwd = hash_pwd,
                           user = session["user_id"])

                flash("Your password was changed successfully.")
                return render_template("login.html")

            else:
                # Password Incorrect
                flash("Password Incorrect, Try again.")
                return render_template("change_pass.html")

    # User reached route via GET
    else:
        return render_template("change_pass.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
