import sqlite3

# Connect to SQLite database (if it doesn't exist, it will be created)
conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS stock (
    item_id INTEGER PRIMARY KEY ,
    item_name TEXT NOT NULL,
    quantity INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS buyers (
    buyer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_name TEXT NOT NULL,
    item_purchased TEXT NOT NULL,
    quantity_purchased INTEGER NOT NULL,
    purchase_date TEXT NOT NULL
)
''')
conn.commit()

# CRUD operations for stock
def add_stock_item():
    times=int(input("How many items do you want to enter : "))
    for i in range(times):
        item_id=int(input("Enter item id : "))
        item_name = input("Enter item name: ")
        quantity = int(input("Enter quantity: "))
        cursor.execute('INSERT INTO stock (item_id, item_name, quantity) VALUES (?, ?, ?)', (item_id, item_name, quantity))
        conn.commit()
    print("Stock item added successfully.")


    
def view_stock():
    cursor.execute('SELECT * FROM stock')
    for row in cursor.fetchall():
        print(row)

def view_buyers():
    cursor.execute('SELECT * FROM buyers')
    for row in cursor.fetchall():
        print(row)

def update_stock_item():
    item_id = int(input("Enter item ID to update: "))
    new_quantity = int(input("Enter new quantity: "))
    cursor.execute('UPDATE stock SET quantity = ? WHERE item_id = ?', (new_quantity, item_id))
    conn.commit()
    print("Stock item updated successfully.")

def delete_stock_item():
    item_id = int(input("Enter item ID to delete: "))
    cursor.execute('DELETE FROM stock WHERE item_id = ?', (item_id,))
    conn.commit()
    print("Stock item deleted successfully.")

# Function to record a purchase and update stock
def record_purchase():
    buyer_name = input("Enter buyer's name: ")
    item_name = input("Enter item purchased: ").lower()  # Convert input to lower case
    quantity_purchased = int(input("Enter quantity purchased: "))
    purchase_date = input("Enter purchase date (YYYY-MM-DD): ")
    
    # Convert stored item names to lower case before comparison
    cursor.execute('SELECT item_id, quantity FROM stock WHERE lower(item_name) = ?', (item_name,))
    item = cursor.fetchone()
    
    if item and item[1] >= quantity_purchased:
        new_quantity = item[1] - quantity_purchased
        cursor.execute('UPDATE stock SET quantity = ? WHERE item_id = ?', (new_quantity, item[0]))
        cursor.execute('INSERT INTO buyers (buyer_name, item_purchased, quantity_purchased, purchase_date) VALUES (?, ?, ?, ?)',
                       (buyer_name, item_name, quantity_purchased, purchase_date))
        conn.commit()
        print("Purchase recorded successfully.")
    else:
        print("Purchase failed: Item not found or insufficient quantity.")

# Menu-based interface
while True:
    print("\nWarehouse Management System")
    print("1. View Stock")
    print("2. Add Stock Item")
    print("3. Update Stock Item")
    print("4. Delete Stock Item")
    print("5. Record Purchase")
    print("6. View Sales history")
    print("7. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        view_stock()
    elif choice == '2':
        add_stock_item()
    elif choice == '3':
        update_stock_item()
    elif choice == '4':
        delete_stock_item()
    elif choice == '5':
        record_purchase()
    elif choice == '6':
        view_buyers()
    elif choice == '7':
        print("Thanks for using the system")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the connection
conn.close()
