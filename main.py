import mysql.connector, time, os

# Setting up the connection to MySQL
connection = mysql.connector.connect(user = 'root', database = 'banking', password = 'Chad248!')

cursor = connection.cursor()


# All functions dealing with accounts
# ie; creation, viewing, modification, and deletion
def add_user():

    # Get user info
    name = input("Name: ")
    balance = 0
    password = input("Password: ")
    email = input("Email: ")
    PIN = input("PIN: ")

    # Create and execute the query into MySQL database
    cursor.execute(f"insert into banking.accounts (name, balance, password, email, PIN) values ('{name}', {balance}, '{password}', '{email}', {PIN})")

    connection.commit()
    
    print(f"Account with name {name} has been added.\n")

    input("Enter anything to continue: ")

    os.system("cls")

def view_account(myName, myPassword):

    # Check if command account that can see everything
    if myName.lower() == "command":
        print("\nEverything:")
        cursor.execute("select * from banking.accounts")
        for item in cursor:
            print()

            print(f"Name of account: {item[1]}")

            print(f"Password of account: {item[3]}")

            print(f"Email of account: {item[4]}")

            print(f"PIN of account: {item[5]}")
            
        print()
        input("Enter anything to continue: ")
        os.system("cls")
        return
    else:
        cursor.execute(f"select * from banking.accounts where name = '{myName}' and password = '{myPassword}'")

        for item in cursor:

            print()

            print(f"Name of account: {item[1]}")

            print(f"Password of account: {item[3]}")

            print(f"Email of account: {item[4]}")

            print(f"PIN of account: {item[5]}")
            
            print()

        input("Enter anything to continue: ")
        os.system("cls")
        return
    
    print("No accounts available")

    input("Enter anything to continue: ")

    os.system("cls")

def mod_account(myName, myPassword):
    if myName == "command":
        print("This account cannot be modified")

        time.sleep(1)

        return

    cursor.execute(f"select id from banking.accounts where name = '{myName}' and password = '{myPassword}'")

    for item in cursor:
        iden = item[0]

    new_name = input("New account name: ")
    new_password = input("New account password: ")
    new_email = input("New account email: ")
    new_PIN = int(input("New account PIN: "))

    cursor.execute(f"update banking.accounts set name = '{new_name}', password = '{new_password}', email = '{new_email}', PIN = '{new_PIN}' where id = '{iden}'")

    connection.commit()

    print("Account modified\n")

    input("Enter anything to continue: ")

    os.system("cls")

def delete_account(myName, myPassword):
    if myName == "command":
        print("This account cannot be deleted")

        time.sleep(1)

        return


    name = myName

    delete = input("Are you sure you want to continue? ")

    if delete.lower()[0] == "y":
        cursor.execute(f"delete from banking.accounts where name = '{name}' and password = '{myPassword}'")

        connection.commit()

        print(f"Account with name {name} has been deleted.\n")

    input("Enter anything to continue: ")

    os.system("cls")

#############################################################################################

# All functions dealing with balance
# ie; checking, deposits, withdrawals
def check_balance(myName, myPassword):
    
    # Check if command account that can see everything
    if myName.lower() == "command":
        print("\nEverything:")
        cursor.execute("select * from banking.accounts")
        for item in cursor:
            print()

            print(f"Name of account: {item[1]}")

            print(f"Balance of account: ${item[2]}")
            
        print()
        input("Enter anything to continue: ")
        os.system("cls")
        return
    else:
        cursor.execute(f"select * from banking.accounts where name = '{myName}' and password = '{myPassword}'")

        for item in cursor:
            thing = item


        print()

        print(f"Name of account: {thing[1]}")

        print(f"Balance of account: ${thing[2]}")
            
        print()

        input("Enter anything to continue: ")
        os.system("cls")
        return
    
    print("No accounts available")

    input("Enter anything to continue: ")

    os.system("cls")

def deposit(myName, myPassword):
    if myName == "command":
        print("This account cannot be deposited to")

        time.sleep(1)

        return
    
    amount = float(input("Amount to deposit: "))

    cursor.execute(f"select balance from banking.accounts where name = '{myName}' and password = '{myPassword}'")

    for item in cursor:
        cur_bal = item[0]
    
    bal = amount + cur_bal

    cursor.execute(f"update banking.accounts set balance = {bal} where name = '{myName}' and password = '{myPassword}'")

    connection.commit()

    print("Money deposited\n")

    input("Enter anything to continue: ")

    os.system("cls")

def withdraw(myName, myPassword):
    if myName == "command":
        print("This account cannot be withdrawn from")

        time.sleep(1)

        return
    
    amount = float(input("Amount to withdraw: "))

    cursor.execute(f"select balance from banking.accounts where name = '{myName}' and password = '{myPassword}'")

    for item in cursor:
        cur_bal = item[0]
    
    bal = cur_bal - amount

    if bal < 0:
        print("Insufficient funds to withdraw that amount. Withdrawing all available funds\n")

        cursor.execute(f"update banking.accounts set balance = {0} where name = '{myName}' and password = '{myPassword}'")

        connection.commit()

        print(f"New balance: $0.00\n")

        input("Enter anything to continue: ")

        os.system("cls")
    else:
        print("Withdrawing funds")

        cursor.execute(f"update banking.accounts set balance = {bal} where name = '{myName}' and password = '{myPassword}'")

        connection.commit()

        print(f"New balance: ${bal}\n")

        input("Enter anything to continue: ")

        os.system("cls")

###########################################################################################3

# Some global variables for accessing a specific account after signing in
global user_name
user_name = "command"
global password

# Function that signs the user in if input given matches an existing account
def sign_in():
    global user_name
    global password

    name = input("Name of account: ")
    passw = input("Password: ")

    cursor.execute("select * from banking.accounts where name = %s and password = %s", (name, passw))
    if len(cursor.fetchall()) > 0:
        user_name = name
        password = passw
        return True
    elif name == "command":
        user_name = name
        password = passw
        return True
    else:
        print("Account doesn't exist")
        return False

os.system("cls")

# Main loop that repeats all the functions
while True:

    # First choices: signing in or creating an account
    print("1. Sign in\n2. Create account\n")
    choice1 = int(input("Choose (-1 to end program): "))

    os.system("cls")

    if choice1 == -1:
        break
    elif choice1 == 1:

        # Checking if signing in works
        if sign_in():

            # If signing in works, then options for manipulating account and balance of account
            while True:
                print("1. View account\n2. Modify account\n3. Delete account\n\n4. View balance\n5. Deposit money\n6. Withdraw money\n")
                choice2 = int(input("Choose (-1 to sign out): "))

                if choice2 == -1:
                    break
                elif choice2 == 1:
                    view_account(user_name, password)
                elif choice2 == 2:
                    mod_account(user_name, password)
                elif choice2 == 3:
                    delete_account(user_name, password)
                elif choice2 == 4:
                    check_balance(user_name, password)
                elif choice2 == 5:
                    deposit(user_name, password)
                elif choice2 == 6:
                    withdraw(user_name, password)
                else:
                    print("Invalid")
    
    # Choice for creating a new account
    elif choice1 == 2:
        add_user()

    # Catchall for any invalid input
    else:
        print("Invalid option")


# Finishing the program and closing the connection to MySQL
print("Done")

time.sleep(1)

os.system("cls")

cursor.close()

connection.close()