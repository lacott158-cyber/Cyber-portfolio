import sqlite3

def connect_db():
    return sqlite3.connect('ebookstore.db')
#Table logic
def init_db():
    try:
        with sqlite3.connect('ebookstore.db') as db:
            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS author(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
                )
            """)

            cursor.execute("""CREATE TABLE IF NOT EXISTS book(
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authorID INTEGER,
                qty INTEGER,
                FOREIGN KEY (authorID) REFERENCES author(id)
                )
            """)

            authors = [
                (1290, 'Charles Dickens', 'England'),
                (8937, 'J.K. Rowling', 'England'),
                (2356, 'C.S. Lewis', 'Ireland'),
                (6380, 'J.R.R. Tolkien', 'South Africa'),
                (5620, 'Lewis Carroll', 'England')
            ]
            cursor.executemany("INSERT OR IGNORE INTO author VALUES(?,?,?)", authors)

            books = [
                (3001, 'A Tale of Two Cities', 1290, 30),
                (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
                (3003, 'The Lion, the Witch and the Wardrobe', 2356, 25),
                (3004, 'The Lord of the Rings', 6380, 37),
                (3005, "Alice’s Adventures in Wonderland", 5620, 12)
            ]
            cursor.executemany("INSERT OR IGNORE INTO book VALUES(?,?,?,?)", books)
            db.commit()
    except sqlite3.Error as e:
        print(f"error: {e}")

def validate_id(id_val):
    if id_val.isdigit() and len(id_val) == 4:
        return int(id_val)
    raise ValueError("Error")

#Functiion to allow users to add books to the database
def enter_book():
    try:
        b_id = validate_id(input("Book ID (4 digits): "))
        title = input("Book Title: ")
        a_id = validate_id(input("Author ID (4 digits): "))
        qty = int(input("Enter Book Quantity: "))

        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO book (id, title, authorID, qty) VALUES (?,?,?,?)", 
                           (b_id, title, a_id, qty))
            db.commit()
            print(f"\n'{title}' added successfully!")

    except ValueError:
        print("Invalid input. Please ensure IDs are 4 digits and quantity is a number.")
    except sqlite3.IntegrityError:
        print(f"Error: A book with ID {b_id} already exists.")
    except Exception as e:
        print(f"Error: {e}")

#Function to allow users to update a books details in the database
def update_book():
    try:
        b_id = validate_id(input("Enter: "))

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT book.title, author.name, author.country, book.qty, author.id 
                           FROM book INNER JOIN author ON book.authorID = author.id 
                           WHERE book.id = ?'''(b_id,))
            result = cursor.fetchone()

            if not result:
                print("Error")
                return
            title, a_name, a_country, qty, a_id = result
            print(f"\nEditing: {title} by {a_name} ({a_country})")
            
            print("What would you like to update?")
            print("1. Quantity (Default)\n2. Title\n3. Author Details")
            choice = input("Select option: ")

            if choice == '2':
                new_title = input(f"Enter [{title}]: ") or title
                cursor.execute("UPDATE book SET title = ? WHERE id = ?", (new_title, b_id))
            elif choice == '3':
                new_name = input(f"Enter [{a_name}]: ") or a_name
                new_country = input(f"Enter [{a_country}]: ") or a_country
                cursor.execute("UPDATE author SET name = ?, country = ? WHERE id = ?", (new_name, new_country, a_id))
            else:
                new_qty = input(f"Enter [{qty}]: ")
                new_qty = int(new_qty) if new_qty else qty
                cursor.execute("UPDATE book SET qty = ? WHERE id = ?", (new_qty, b_id))
            conn.commit
            print("Update successful!")
    except Exception as e:
        print(f"error: {e}")

#Function to allow users to remove books from the database
def delete_book():
    try:
        b_id = validate_id(input("Enter: "))
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM book WHERE id = ?", (b_id,))
            conn.commit
            if cursor.rowcount > 0:
                print("Deleted")
            else:
                print("Error")
    except Exception as e:
        print(f"Error {e}")

#Function to allow users to search the database
def search_books():
    term = input("Enter ID or Title to search: ")
    
    with connect_db() as conn:
        cursor = conn.cursor()
        if term.isdigit():
            query = "SELECT * FROM book WHERE id = ? OR title LIKE ?"
            cursor.execute(query, (int(term), f"%{term}%"))
        else:
            query = "SELECT * FROM book WHERE title LIKE ?"
            cursor.execute(query, (f"%{term}%",))
        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("No matching books found.")

def view_all_details():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT book.title, author.name, author.country 
                          FROM book INNER JOIN author ON book.authorID = author.id''')
        rows = cursor.fetchall()
        if rows:
            titles, names, countries = zip(*rows)
            print("\nDetails " + "-" * 42)
            for t, n, c in zip(titles, names, countries):
                print(f"Book Title: {t}")
                print(f"Name: {n}")
                print(f"Country: {c}")
                print("-" * 50)
        else:
            print("Out of stock")

#Main menu logic
def main():
    init_db()
    while True:
        print("Menu")
        print("1: Enter Book")
        print("2: Update Book")
        print("3: Delete Book")
        print("4: Search Books")
        print("5: View Book details")
        print("0: Exit")
        choice = input("Select: ")

        if choice == '1': enter_book()
        elif choice == '2': update_book()
        elif choice == '3': delete_book()
        elif choice == '4': search_books()
        elif choice == '5': view_all_details()
        elif choice == '0': 
            print("Goodbye!")
            break
        else:
            print("Error")

#Closes database
if __name__ == "__main__":
    main()