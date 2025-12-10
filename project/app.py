from typing import TYPE_CHECKING
from flask import Flask, redirect, render_template, flash, request, session, abort
from flask_session import Session
from werkzeug.security import check_password_hash
from decorators import login_required
from account_libraries import AccountLibraries, LibraryType
from account_libraries_services import AccountLibrariesServices
from bank_account import BankAccount, AccountType
from bank_account_services import BankAccountServices
from transactions import TransactionType
from transaction_services import TransactionServices
from user_services import UserServices
from db import get_db_connection
from validation_error import ValidationError, require_field


if TYPE_CHECKING:
    from bank_account import BankAccount
# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response) -> None:
    """Ensure responses aren't cached by the browser """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Displays user's account libraries.
    Allows user to create new account""" 
    db = get_db_connection()
    
    # User wants to open new account
    if request.method == "POST":      
        return render_template("open_account.html")
    
    # User loaded page
    user_id = session["user_id"]
    # Load users accounts
    checking_library:AccountLibraries = AccountLibrariesServices.load_from_library(user_id, LibraryType.CHECKING, db)
    savings_library: AccountLibraries = AccountLibrariesServices.load_from_library(user_id, LibraryType.SAVINGS, db)

    # TODO: Add total balances to accounts
    db.close()

    return render_template("index.html", checking_library=checking_library, savings_library=savings_library)

@app.route("/view_account", methods=["GET", "POST"])
@login_required
def view_account():
    """Displays a specific account"""
    account_id = request.args.get("account_id")
    if not account_id:
        return redirect("/")
    
    try:
        bank_account = BankAccountServices.get_account_for_user(int(account_id), session["user_id"])
    except ValueError: # Ensures the account exists
        return abort(404)
    except PermissionError: # Ensure the account belongs to the logged-in user
        return abort(403)
    return render_template("view_account.html", bank_account=bank_account)

@app.route("/view_profile", methods=["GET"])
@login_required
def view_profile():
    """Displays user's profile information"""
    user_id = session["user_id"]
    db = get_db_connection()
    user = UserServices.get_user_by_id(user_id, db)
    db.close()
    if user is None:
        return abort(404)
    return render_template("view_profile.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    db = get_db_connection()
    # User submitted form
    if request.method == "POST":
        try:
            username = require_field(request.form.get("username"), "username")
            password = require_field(request.form.get("password"), "password")
        
            # Query database for username
            user = UserServices.get_user_by_username(username, db) 

            # Ensure username exists and password is
            if not user or not check_password_hash(user.password_hash, password):
                return "Invalid username or password", 403
            
            # Remember which user has logged in
            session["user_id"] = user.id
            # Redirect user to home page
            return redirect("/")
        except ValidationError as e:
            flash(str(e), "error")
            return render_template("login.html"), 400
    db.close()
    # User loaded login page
    return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    db = get_db_connection()
    # User submitted form
    if request.method == "POST":
        try:
            # Get user information from form and create user object
            first_name = require_field(request.form.get("first_name"), "first_name")
            last_name = require_field(request.form.get("last_name"), "last_name")
            username = require_field(request.form.get("username"), "username") 
            password = require_field(request.form.get("password"), "password")
            confirmation = require_field(request.form.get("confirmation"), "confirmation")
            date_of_birth = require_field(request.form.get("date_of_birth"), "date_of_birth")

            if password != confirmation:
                raise ValidationError("Password and confirmation password are not the same.")
            
            # Create new user and add to database
            user = UserServices.register_new_user(first_name, last_name, username, date_of_birth, password, db) 
           
            # Create default checking and savings libraries for user 
            AccountLibrariesServices.create_default_libraries(user.id, db) 
    
            # Log the user in
            session["user_id"] = user.id 
            db.close()
            return redirect("/")
        
        except ValidationError as e:
            flash(str(e), "error")
            return render_template("register.html"), 400
    # User loaded quote page
    return render_template("register.html")

@app.route("/open_account", methods=["GET", "POST"])
@login_required
def open_account():
    """Opens a new Checking or Savings Account and adds it to the user's account library"""
    # Validate account type
    account_type = request.args.get("type") # 'checking' or 'savings'
    if not account_type:
        return redirect("/")
    
    # Map account type to library type
    account_type = AccountType.CHECKING if account_type== 'checking' else AccountType.SAVINGS
    library_type = LibraryType.CHECKING if account_type == AccountType.CHECKING else LibraryType.SAVINGS
    
    user_id = session["user_id"]

    # User submitted a new account
    if request.method == "POST":
        try:
            nickname = require_field(request.form.get("nickname"), "nickname")
            initial_deposit = require_field(request.form.get("initial_deposit"), "initial_deposit")
            debit_card = require_field(request.form.get("debit_card"), "debit_card")

            # Create new bank account
            bank_account = BankAccount(
                id=None,
                user_id=user_id,
                account_type=account_type,
                balance=float(initial_deposit), 
                nickname=nickname, 
                debit_card=debit_card 
            )

            # Save bank account to database
            bank_account.save_bank_account(get_db_connection())

            # Get library instance
            library = AccountLibrariesServices.load_from_library(user_id, library_type, get_db_connection())

            # Save account to library in database
            AccountLibrariesServices.add_account_to_library(library.id, bank_account.id, get_db_connection()) 

            # Add account to user's library instance
            library.add_account(bank_account.account_number, bank_account)
        
            return redirect("/")
        except ValidationError as e:
            flash(str(e), "error")
            return render_template("open_account.html", account_type=account_type), 400
    
    # User loaded account open page
    return render_template("open_account.html", account_type=account_type)

@app.route("/move_money", methods=["GET", "POST"])
@login_required
def move_money():
    """Moves money from one account to another within the user's account libraries"""
    user_id = session["user_id"]
    db = get_db_connection()

    # Combine all user's accounts
    checking_library = AccountLibrariesServices.load_from_library(user_id, LibraryType.CHECKING, db)
    savings_library = AccountLibrariesServices.load_from_library(user_id, LibraryType.SAVINGS, db)
    # accounts = {Key: account_number,  Value: BankAccount instances}
    all_accounts = list(checking_library.accounts.values()) + list(savings_library.accounts.values())

    # Ensure user has at least two accounts to transfer between
    if len(all_accounts) < 2:
        flash("Need at least two accounts to transfer money between", "error")
        return redirect("/")
    
    # User submitted move money form
    if request.method == "POST":
        try: 
            # Get id of accounts and amount info from form
            from_account_id = require_field(request.form.get("from_account"), "from_account")
            to_account_id = require_field(request.form.get("to_account"), "to_account")
            amount = require_field(request.form.get("amount"), "amount")

            # Ensure accounts belong to user
            from_account: BankAccount = BankAccountServices.get_account_for_user(int(from_account_id), session["user_id"])
            to_account: BankAccount = BankAccountServices.get_account_for_user(int(to_account_id), session["user_id"])

            # Ensure source account has sufficient funds
            if from_account.balance < float(amount):
                raise ValidationError("Do not possess sufficient funds for this transfer")
            
            # Perform the money transfer
            from_account.balance -= float(amount)
            to_account.balance += float(amount)

            # Save updated accounts to database
            BankAccountServices.update_account_balance(from_account.id, from_account.balance, db)
            BankAccountServices.update_account_balance(to_account.id, to_account.balance, db)

            # Update transactions table
            TransactionServices.record_transaction(from_account.id, to_account.id, float(amount), TransactionType.TRANSFER, db)
            
            db.close()

            # Transfer successful
            return redirect("/")
        except ValidationError as e:
            flash(str(e), "error")
            # Transfer failed
            return redirect("/move_money"), 400
        
    # User loaded move money page
    db.close()
    return render_template("move_money.html", all_accounts=all_accounts)
    
# Run the application if executed directly
if __name__ == "__main__":
    app.run(debug=True)
