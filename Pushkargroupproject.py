import sqlite3
conn = sqlite3.connect("railway.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS trains (train_no INTEGER PRIMARY KEY, train_name TEXT, starting_st TEXT, destination_st TEXT, departure TEXT, arrival TEXT)")
# Define a function to print the database
def print_db():
    cur.execute("SELECT * FROM trains")
    row = cur.fetchone()
    while row is not None:
        print(row)
        row = cur.fetchone()
    print()
    
# Define a function to enter data into the table
def enter_data():
    n = int(input("How many trains do you want to enter? "))
    for i in range(n):
        train_no = int(input("Enter the train number: "))
        train_name = input("Enter the train name: ")
        starting_st = input("Enter the Starting station: ")
        destination_st = input("Enter the destination station: ")
        departure = input("Enter the departure time: ")
        arrival = input("Enter the arrival time: ")
        cur.execute("INSERT INTO trains VALUES (?, ?, ?, ?, ?, ?)", (train_no, train_name, starting_st, destination_st, departure, arrival))
    conn.commit()
# Define a function to update or delete
def update_or_delete():

    choice = input("Do you want to update or delete a record? (U/D) ")

    if choice == "U":
        train_no = int(input("Enter the train number you want to update: "))
        cur.execute("SELECT * FROM trains WHERE train_no = ?", (train_no,))
        row = cur.fetchone()

        if row:
            print("The current details of the train are:")
            print("Train No\tTrain Name\t\t\tStarting_st\t\tDestination_st\t\tDeparture_time\t\tArrival_time")
            print(row[0], "\t\t", row[1], "\t\t", row[2], "\t\t", row[3], "\t\t", row[4], "\t\t", row[5])
            print()

            column = input("Which column do you want to update? (train_name, starting_st, destination_st, departure, arrival) ")

            if column in ["train_name", "starting_st", "destination_st", "departure", "arrival"]:
                new_value = input(f"Enter the new value for {column}: ")
                cur.execute(f"UPDATE trains SET {column} = ? WHERE train_no = ?", (new_value, train_no))
                conn.commit()
                print(f"The record of train number {train_no} has been updated successfully.")
            else:
                print("Invalid column. Please enter one of the following: train_name, starting_st, destination_st, departure, arrival.")
        else:
            print(f"There is no record of train number {train_no} in the database.")
    elif choice == "D":
        train_no = int(input("Enter the train number you want to delete: "))
        cur.execute("SELECT * FROM trains WHERE train_no = ?", (train_no,))
        row = cur.fetchone()
        if row:
            print("The current details of the train are:")
            print("Train No\tTrain Name\t\t\tStarting_st\t\tDestination_st\t\tDeparture_time\t\tArrival_time")
            print(row[0], "\t\t", row[1], "\t\t", row[2], "\t\t", row[3], "\t\t", row[4], "\t\t", row[5])
            print()
            confirm = input(f"Are you sure you want to delete the record of train number {train_no}? (Y/N) ")

            if confirm == "Y":
                cur.execute("DELETE FROM trains WHERE train_no = ?", (train_no,))
                conn.commit()
                print(f"The record of train number {train_no} has been deleted successfully.")
        
            elif confirm == "N":
                print("The deletion has been cancelled.")
            else:
                print("Invalid choice. Please enter Y or N.")
        else:
            print(f"There is no record of train number {train_no} in the database.")
    else:
        print("Invalid choice. Please enter U or D.")

while True:
    print("1.Enter data into table")
    print("2.Print database")
    print("3.To update or delete a record")
    print("Enter Q to Quit")
    choice = input("Enter your choice ")

    if choice == "1":
        enter_data()
    elif choice == "2":
        print_db()
    elif choice == "3":
        update_or_delete()
    elif choice == "q"or"Q":
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3 OR Q to quit")

conn.close()
#END




