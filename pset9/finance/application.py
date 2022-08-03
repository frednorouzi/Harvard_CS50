import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

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
    # Query from stock table into a list
    rows = db.execute("""
    SELECT symbol, SUM(shares) as TotalShares FROM stocks
    WHERE user_id = :user_id
    GROUP BY symbol
    HAVING TotalShares > 0
    """, user_id=session["user_id"])
    # Define empty list
    items = []
    # Initial balance variable in order to show user total cash balance
    balance = 0
    # Retrieve data and add into a list
    for row in rows:
        stock = lookup(row["symbol"])
        items.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": row["TotalShares"],
            "price": usd(stock["price"]),
            "total": usd(stock["price"] * row["TotalShares"])
        })
        # Total cost of stocks
        balance += stock["price"] * row["TotalShares"]
        # Query on users table to find current user cash
    cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])[0]["cash"]
    # Total user cash balance
    balance += cash

    return render_template("index.html", items=items, cash=usd(cash), balance=usd(balance))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Submitting a form via POST
    if request.method == "POST":
        # Get user input
        symbol = request.form.get("symbol").upper()
        # Returning data via lookup function
        stock = lookup(symbol)
        # Check user input validity
        if not symbol:
            return apology("Must provide valid symbol", 400)
        elif not stock:
            return apology("Must provide valid symbol", 400)

        try:
            # Get integer shares data by user input
            shares = int(request.form.get("shares"))
        except:
            return apology("Must provide integer number", 400)

        # Check positive number of shares by user input
        if shares < 1:
            return apology("shares must be a positive integer", 400)

        # Query on users table to retrieve user cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        total_price = stock["price"] * shares
        # Check for available cash to buy stock
        if cash < total_price:
            return apology("Insufficient cash!", 400)
        else:
            # Update user cash and insert new data into portfolio after buying stock
            db.execute("UPDATE users set cash = ? WHERE id = ?", cash - total_price, session["user_id"])

            db.execute("""INSERT INTO stocks (user_id, name, price, shares, symbol)
                        VALUES (:user_id, :name, :price, :shares, :symbol)""",
                       user_id=session["user_id"],
                       name=stock["name"],
                       price=stock["price"],
                       shares=shares,
                       symbol=symbol.upper()
                       )
         # Return to the portfolio page
        flash("Bought successful!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Query of transaction
    rows = db.execute("""
    SELECT symbol, shares, price, time
    FROM stocks
    WHERE user_id=:user_id
    """, user_id=session["user_id"])
    # Iterate over the transaction rows in order to change price format to us dollar
    for i in range(len(rows)):
        rows[i]["price"] = usd(rows[i]["price"])

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        # Check user input validity
        if not symbol:
            return apology("Invalid symbol!")
        stock = lookup(symbol)

        if not stock:
            return apology("Invalid symbol!")
        return render_template("qouted.html", stock=stock, usd=usd)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username was defined
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif len(rows) != 0:
            return apology("Username already exists", 400)

        # Ensure password was created
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was entered
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords doesn't match", 400)

        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                       username=request.form.get("username"),
                       hash=generate_password_hash(request.form.get("password")))

            # Redirect user to home page
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        if not symbol:
            return apology("Must provide valid symbol", 400)
        elif not stock:
            return apology("Must provide valid symbol", 400)

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Must provide integer number", 400)

        if shares < 1:
            return apology("shares must be a positive integer", 400)

        rows = db.execute("""
        SELECT symbol, SUM(shares) as TotalShares
        FROM stocks
        WHERE user_id=:user_id
        GROUP BY symbol
        HAVING TotalShares > 0
        """, user_id=session["user_id"])

        for row in rows:
            if row["symbol"] == symbol:
                if shares > row["TotalShares"]:
                    return apology("More than existing shares!")

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        total_price = stock["price"] * shares

        db.execute("UPDATE users set cash = ? WHERE id = ?", cash + total_price, session["user_id"])

        db.execute("""INSERT INTO stocks (user_id, name, price, shares, symbol)
            VALUES (:user_id, :name, :price, :shares, :symbol)""",
                   user_id=session["user_id"],
                   name=stock["name"],
                   price=stock["price"],
                   shares=-1 * shares,
                   symbol=symbol.upper()
                   )

        flash("Sold successful!")
        return redirect("/")
    else:
        rows = db.execute("""
        SELECT symbol FROM stocks
        WHERE user_id=:user_id
        GROUP BY symbol
        HAVING SUM(shares) > 0;
        """, user_id=session["user_id"])
        return render_template("sell.html", symbols=[row["symbol"] for row in rows])


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add cash to your account"""
    if request.method == "POST":
        db.execute(""" UPDATE users
        SET cash = cash + :pay
        WHERE id=:user_id
        """, pay=request.form.get("cash"),
                   user_id=session["user_id"])
        flash("Adding Cash done!")
        return redirect("/")

    else:
        return render_template("addcash.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
