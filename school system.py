import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="",
    database = "School"
)

myCursor = db.cursor(buffered=True)

"""
Student login session
This function takes in one string parameter representing the users username
Students will be able to check their attendance status and download it as a text file
"""
def student_session(username):
    print("\nStudent Login Successful")

    username = (str(username),)
    #query the database and store into records
    myCursor.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
    records = myCursor.fetchall()

    while True:
        #Student Menu
        print("\n1. View Attendance Status")
        print("2. Download Attendance Status")
        print("3. Logout")

        user_option = input(str("Option: "))

        if user_option == "1":
            print("Viewing Attendance Status")
            #Print each record in records
            for record in records:
                print(record)

        elif user_option == "2":
            print("Downloading attendance")
            #Write the records into a text file
            for record in records:
                with open("D:\Desktop\student_attendance.txt", "w") as f:
                    f.write(str(records)+"\n")
                f.close()
            print("All records downloaded")

        elif user_option == "3":
            print("Logging out")
            break
        else:
            print("Invalid Option")


"""
Professor login session
Professors will be able to mark and check students' attendance status
"""
def prof_session():
    print("\nProfessor Login Successful")
    while True:
        #Professor Menu
        print("\n1. Mark Student Attendance")
        print("2. View Attendance")
        print("3. Logout")

        user_option = input(str("Option: "))
        if(user_option == "1"):
            print("\nMark Student Attendance")
            #Query the database for the username of all students
            myCursor.execute("SELECT username FROM users WHERE accType = 'student'")
            #Fetch all the records that are returned from the query above
            records = myCursor.fetchall()
            #Prompt user for the date
            date = input(str("Date : DD/MM/YYYY: "))

            #Since each record is returned as a tuple, we want to remove the extra characters
            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",","")
                record = str(record).replace("(", "")
                record = str(record).replace(")","")

                #The three possible status: absent, present or late
                status = input(str("Status for " + str(record) + " (A/P/L): "))
                query_values = (str(record), date, status)
                myCursor.execute("INSERT INTO attendance (username, date, status) VALUES (%s, %s, %s)", query_values)
                db.commit()
                print(record + " Marked as " + status)

        elif(user_option == "2"):
            print("\nViewing Attendance")
            #query the database for the username, date and status for each entry
            myCursor.execute("SELECT username, date, status FROM attendance")
            #fetch all the records that are returned from the query above
            records = myCursor.fetchall()
            #printing the records
            for record in records:
                print(record)

        elif(user_option == "3"):
            print("Logging out\n")
            break
        else:
            print("Invalid Option")

def admin_session():
    print("\nAdmin Login Successful")
    while True:
        #Admin Menu
        print("\n1. Register New Student")
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

def prof_login():
    #Prompt user for login details
    print("Professor Login\n")
    username = input(str("Username: "))
    password = input(str("Password: "))

    #Check login details
    query_values = (username, password)
    myCursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND accType = 'professor'", query_values)
    if myCursor.rowcount < 1:
        print("Incorrect login details")
    else:
        prof_session()


def student_login():
    print("Student login\n")
    username = input(str("Username: "))
    password = input(str("Password: "))

    #Check logind etails
    query_values = (username, password)
    myCursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND accType = 'student'", query_values)
    if myCursor.rowcount < 1:
        print("Incorrect login details")
    else:
        #Login is successful and we call the student_session method that takes in a string parameter representing the username
        student_session(username)

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
            student_login()
        elif user_option == "3":
            prof_login()
        else:
            print("Invalid Option")

main()
