import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="",
    database = "School"
)

myCursor = db.cursor(buffered=True)

def admin_session():
    print("Admin Login successful\n")
    while True:
        #Admin Menu
        print("1. Register New Student")
        print("2. Register New Professor")
        print("3. Delete Existing Student")
        print("4. Delete Existing Professor")
        print("5. Logout")

        #User Input
        user_option = input(str("Option: "))
        if user_option == "1":
            #Prompt admin for student login details
            print("\nRegister New Student")
            username = input(str("Student Username: "))
            password = input(str("Student Password: "))
            #Insert student into the database
            query_values = (username, password)
            myCursor.execute("INSERT INTO users (username, password, accType) VALUES (%s, %s, 'student')", query_values)
            db.commit()
            print(username + " has been registered as a student")

        elif user_option == "2":
            print("\nRegister New Professor")
            username = input(str("Professor Username: "))
            password = input(str("Professor Password: "))
            query_values = (username, password)
            myCursor.execute("INSERT INTO users (username, password, accType) VALUES (%s, %s, 'professor')", query_values)
            db.commit()
            print(username + " has been registered as a professor")


        elif user_option == "3":
            print("\nDelete Existing Student")
            username = input(str("Student Username: "))
            query_values = (username, "student")
            myCursor.execute("DELETE FROM users WHERE username = %s AND accType = %s", query_values)
            db.commit()
            #Checking if any rows were affected
            if myCursor.rowcount < 1:
                print("user not found")
            else:
                print(username + " has been removed from the system")

        elif user_option == "4":
            print("\nDelete Existing Professor")
            username = input(str("Professor Username: "))
            query_values = (username, "professor")
            myCursor.execute("DELETE FROM users WHERE username = %s AND accType = %s", query_values)
            db.commit()
            if myCursor.rowcount < 1:
                print("user not found")
            else:
                print(username + " has been removed from the system")

        elif user_option == "5":
            print("Logging out\n")
            break
        
        else:
            print("Invalid Option")


#Function for authenticating an admin login
def admin_login():
    #Prompt user for username and password
    print("Admin Login\n")
    username = input(str("Username: "))
    password = input(str("Password: "))

    #Check if the login details are correct
    if username == "admin":
        if password == "adminpassword":
            #If the login details are valid, then the user will gain access to the admin session
            admin_session()
        else:
            print("Password Incorrect")
    else:
        print("User not recognized")



def main():
    
    while True:
        #Main menu
        print("Welcome to the School Management System!\n")
        print("1. Login as Admin")
        print("2. Login as Student")
        print("3. Login as Professor")

        #User Input
        user_option = input(str("Option: "))
        if user_option == "1":
            admin_login()
        elif user_option == "2":
            print("Student Login")
        elif user_option == "3":
            print("Professor Login")
        else:
            print("Invalid Option")

main()
