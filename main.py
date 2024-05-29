import sqlite3
conn = sqlite3.connect("computer_department.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS management (
    user_id TEXT UNIQUE,
    computer_id INTEGER,
    starting_time TEXT,
    end_time TEXT,
    FOREIGN KEY (computer_id) REFERENCES computer_information (computer_id)
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS computer_information (
    computer_id INTEGER PRIMARY KEY,
    computer_status TEXT
)""")

def input_data_management():
    user_id = input("Enter the user id: ")
    computer_id = int(input("Enter the computer id: "))
    starting_time = input("Enter the starting time: ")
    end_time = input("Enter the end time: ")
    cur.execute("SELECT computer_status FROM computer_information WHERE computer_id = ?", (computer_id,))
    result = cur.fetchone()
    if result is None:
        print("Invalid computer id.")
        return
    elif result[0] == "unavailable":
        print("The computer is unavailable.")
        return
    try:
        cur.execute("INSERT INTO management VALUES (?, ?, ?, ?)", (user_id, computer_id, starting_time, end_time))
        conn.commit()
        print("Data inserted successfully.")
    except sqlite3.IntegrityError:
        print("User id already exists.")

def print_data_management():
    cur.execute("SELECT * FROM management")
    data = cur.fetchall()
    print("user_id\tcomputer_id\tstarting_time\tend_time")
    print("-" * 40)
    for row in data:
        print("\t".join(map(str, row)))

def update_data_management():
    user_id = input("Enter the user id: ")
    computer_id = int(input("Enter the computer id: "))
    cur.execute("SELECT * FROM management WHERE user_id = ? AND computer_id = ?", (user_id, computer_id))
    result = cur.fetchone()
    if result is None:
        print("No record found.")
        return
    new_starting_time = input("Enter the new starting time: ")
    new_end_time = input("Enter the new end time: ")
    cur.execute("UPDATE management SET starting_time = ?, end_time = ? WHERE user_id = ? AND computer_id = ?", (new_starting_time, new_end_time, user_id, computer_id))
    conn.commit()
    print("Data updated successfully.")

def delete_data_management():
    user_id = input("Enter the user id: ")
    computer_id = int(input("Enter the computer id: "))
    cur.execute("SELECT * FROM management WHERE user_id = ? AND computer_id = ?", (user_id, computer_id))
    result = cur.fetchone()
    if result is None:
        print("No record found.")
        return
    choice = input("Are you sure you want to delete this record? (y/n): ")
    if choice.lower() == "y":
        cur.execute("DELETE FROM management WHERE user_id = ? AND computer_id = ?", (user_id, computer_id))
        conn.commit()
        print("Data deleted successfully.")
    else:
        print("Operation cancelled.")

def input_data_computer():
    computer_id = int(input("Enter the computer id: "))
    computer_status = input("Enter the computer status: ")
    if computer_status not in ["available", "unavailable"]:
        print("Invalid computer status.")
        return
    try:
        cur.execute("INSERT INTO computer_information VALUES (?, ?)", (computer_id, computer_status))
        conn.commit()
        print("Data inserted successfully.")
    except sqlite3.IntegrityError:
        print("Computer id already exists.")

def print_data_computer():
    cur.execute("SELECT * FROM computer_information")
    data = cur.fetchall()
    print("computer_id\tcomputer_status")
    print("-" * 25)
    for row in data:
        print("\t".join(map(str, row)))

def update_data_computer():
    computer_id = int(input("Enter the computer id: "))
    cur.execute("SELECT * FROM computer_information WHERE computer_id = ?", (computer_id,))
    result = cur.fetchone()
    if result is None:
        print("No record found.")
        return
    new_computer_status = input("Enter the new computer status: ")
    if new_computer_status not in ["available", "unavailable"]:
        print("Invalid computer status.")
        return
    cur.execute("UPDATE computer_information SET computer_status = ? WHERE computer_id = ?", (new_computer_status, computer_id))
    conn.commit()
    print("Data updated successfully.")

def delete_data_computer():
    computer_id = int(input("Enter the computer id: "))
    cur.execute("SELECT * FROM computer_information WHERE computer_id = ?", (computer_id,))
    result = cur.fetchone()
    if result is None:
        print("No record found.")
        return
    choice = input("Are you sure you want to delete this record? (y/n): ")
    if choice.lower() == "y":
        cur.execute("DELETE FROM computer_information WHERE computer_id = ?", (computer_id,))
        conn.commit()
        print("Data deleted successfully.")
    else:
        print("Operation cancelled.")

def display_menu():
    print("Welcome to the computer department management system.")
    print("Please choose an option:")
    print("1. Input data into management table")
    print("2. Print data from management table")
    print("3. Update data in management table")
    print("4. Delete data from management table")
    print("5. Input data into computer_information table")
    print("6. Print data from computer_information table")
    print("7. Update data in computer_information table")
    print("8. Delete data from computer_information table")
    print("9. Exit")

display_menu()
choice = int(input("Enter your choice: "))
while True:
    if choice == 1:
        input_data_management()
    elif choice == 2:
        print_data_management()
    elif choice == 3:
        update_data_management()
    elif choice == 4:
        delete_data_management()
    elif choice == 5:
        print(["available", "unavailable"],"Enter data according to this only")
        input_data_computer()
    elif choice == 6:
        print_data_computer()
    elif choice == 7:
        update_data_computer()
    elif choice == 8:
        delete_data_computer()
    elif choice == 9:
        break
    else:
        print("Invalid choice.")
    display_menu()
    choice = int(input("Enter your choice: "))

conn.close()
print("Thank you for using the system.")
