# Bomanis Bank

### Video Demo: https://youtu.be/8grji7qOIQU

# **Description**:

Bomanis Bank is a web-based banking simulation that allows users to create and manage multiple bank accounts, transfer funds, and view account details in a simple, secure interface.
Users are able to create bank accounts to hold a cash balance. Transfer money from accounts. As well as view a portfolio of their owned accounts. In the future, I would like to add functions that will enable users to deposit and withdraw money to and from their accounts. As well as more interaction within the website itself. For example, using Javascript to show pop up messages on the screen when a users submits a form or clicks on a button.

# **Planning**

During the planning phase of Bomanis Bank, I began by identifying the main problems my website would solve and the functionality I wanted to provide. My inspiration came from real online banking platforms I personally use. Once I had an idea with what I wanted, I then moved onto the Database: bomanis_vault.py. This helped me visualize what kind tables I would need and how they would interact with each other. I designed my database schema on paper using Crow’s Foot notation, which helped me visualize the relationships between users, accounts, and transactions. Once finalized, I implemented the schema in SQLite and integrated it with Flask in app.py. In app.py are the necessary route functions/html files my website needed. Using Object-Oriented Programming, I modeled key real-world entities such as User, BankAccount, and AccountLibrary, along with corresponding service classes for database operations. Bootstrap provided the visual structure, and a JavaScript module (scripts.js) is in development for greater interactivity. In the future I hope to come back to Bomanis Bank and leave a more complete and satisfactory product.

# **Requirments**

The minimal requirments for running Bomanis Bank are Flask, a web framework, which includes Werkzueg, and Jinja2. As well as Flask-Session in order to store a users session in memory.

# **Installation**

pip install Flask Flask-Session
How to run:
flask run

# **Usage Instructions**

## Registration

To use Bomanis Bank, you will first have to register an account. You should see a register tab at the top right of the login screen. You will need to provide simple information including your first and last name, a UNIQUE username, a password along with confirmation and then finally your date of birth. Once registered you will be logged into your account.

## Accounts

Once logged in, displayed on the Accounts screen will be your portfolio of bank accounts, if any. You will have the option to open however many checking and or savings accounts you would like. A created account will be shown on the 'Accounts' home page of Bomanis Bank. You will be able to view an accounts details if you click on the accounts card.

## Account Creation

If you choose to create an account you will be asked to provide the account a nickname, an intial deposit-not exceeded $5000.00-and if you would like to have a debit card attached to the account.

## Move Money

If you would like to move money from an existing Bomanis Bank account to another, you may do so by using the Move Money tab at the top of the screen. You will be asked with drop down menus to select a 'From' and 'To' account along with an amount of money to move.

## Profile

You may view your registered accounts details, including your username, Full name, Date of Birth, and date registered with the profile tab at the top of the screen.

## Logout

Finally if you click on the Logout tab at the top right of the screen you will be returned back to the Log In screen. with your information cleared from the session.

## Future Features

My idea of an improved Bomanis Bank web application would be to provide a user the functionality of:

Deposit and withdrawal

Delete or close accounts

Real-time alerts with JavaScript

Improved UI using dynamic modals and animations

# **Files**

## app.py

app.py is where I configure my application using Flask.
All of the routes of Bomanis Bank are found here, including: the main index, view account, view profile, login, logout, register, open account, and move money.

## user.py

user.py is the blueprint of what a Bomanis Bank user should be.

## user_services.py

user_Services.py contains all of the utlities for user registration, login, and user retrieval

## account_libraries.py

account_librarires.py acts as the blueprint for an account library. It is the domain layer for managing account libraries. It also contains the LibraryType class which defines the types of an account library.

## account_libraries_services.py

account_libraries_services.py provides utilites such as: creating, loading and managing account libraries in the database.

## bank_acccount.py

bank_account.py is a blueprint of what a Bomanis Bank bank account should be.

## bank_account_services.py

bank_account_services.py acts as the service layer for bank account operations.

## transactions.py

transactions.py contains the class TransactionType which defines the types of transactions availible in Bomanis Bank

## transactions_services.py

transactions_services.py handles the service layer, including database interactions.

## scripts.js

scripts.js is unfinished. In the future I would like to have the Bomanis Bank website be more interactive. For example, when a user creates an account, an 'account succesfully created' type message would show up on the screen.

## bomanis_vault.db

bomanis_vault.db is where all of the data is stored. It is stored as a relational databse. Containing data such as users, account libraries, bank accounts, and transaction history. \

## **templates**

The templates folder contains all of the html templates, for each route in Bomanis Bank. All of the templates extend layout.html, which is where the href Bootsrap Links are located.

# **Acknowledgements**

Thank you to ChatGPT for creating the logo image of Bomanis Bank.
