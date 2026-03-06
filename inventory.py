from tabulate import tabulate

# Class definition
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost
    
    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.product} ({self.code}) Country: {self.country} Cost: {self.cost} Qty: {self.quantity}"

# Empty shoe list
shoe_list = []

# Opens and reads data from inventory.txt
def read_shoes_data():
    try:
        shoe_list.clear()
        with open("inventory.txt", "r") as f:
            next(f)
            for line in f:
                data = line.strip().split(',')
                if len(data) == 5:
                    new_shoe = Shoe(data[0], data[1], data[2], float(data[3]), int(data[4]))
                    shoe_list.append(new_shoe)
            print("Data loaded")
    except FileNotFoundError:
        print("Error")

# Allows the user to add add shoe data
def capture_shoes():
    country = input("Enter country: ")
    code = input("Enter shoe code: ")
    product = input("Enter product: ")

    while True:
        try: 
            cost = float(input("Enter cost: "))
            quantity = int(input("Enter quantity: "))
            new_shoe = Shoe(country, code, product, cost, quantity)
            shoe_list.append(new_shoe)
            print("Successfull")
            break
        except ValueError:
            print("Error")

# Prints the inventory.txt data in a table format
def view_all():
    if not shoe_list:
        print("Error")
        return
    table = [[s.country, s.code, s.product, s.cost, s.quantity] for s in shoe_list]
    print("\n" + tabulate(table, headers=["Country", "Code", "Product", "Cost", "Quantity"], tablefmt="grid"))

# Identfies show with the lowest quantity and allows user update stock level
def re_stock():
    if not shoe_list:
        print("Inventory empty")
        return
    low_shoe = min(shoe_list, key=lambda x: x.quantity)
    print(f"{low_shoe.product} ({low_shoe.code}) {low_shoe.quantity}")
    choice = input("(yes/no): ").lower()
    if choice == 'yes':
        try:
            additional_qty = int(input("Enter amount: "))
            low_shoe.quantity += additional_qty
            with open("inventory.txt", "w") as f:
                f.write("Country,Code,Product,Cost,Quantity\n")
                for s in shoe_list:
                    f.write(f"{s.country},{s.code},{s.product},{s.cost},{s.quantity}\n")
        except ValueError:
            print("Invalid input")

# Allows user to search for shoes by there code
def search_shoe():
    code = input()
    for shoe in shoe_list:
        if shoe.code == code:
            print(shoe)
            return shoe
    print("Error")

# Formula for calculting shoe value
def value_per_item():
    for s in shoe_list:
        value = s.cost * s.quantity
        print(f"{s.product}: {value:,.2f}")

# Displays show on sale based on quantity
def highest_qty():
    if not shoe_list:
        return
    top_shoe = max(shoe_list, key=lambda x: x.quantity)
    print(f"ON SALE! {top_shoe.product} {top_shoe.code} - Qty: {top_shoe.quantity}")

# menu logic
read_shoes_data()

while True:
    print("1. View Inventory")
    print("2. Add Shoes")
    print("3. Restock shoes")
    print("4. Search Shoes")
    print("5. View Values")
    print("6. Sale")
    print("0. Exit")

    choice = input()
    if choice == "1": view_all()
    elif choice == "2": capture_shoes()
    elif choice == "3": re_stock()
    elif choice == "4": search_shoe()
    elif choice == "5": value_per_item()
    elif choice == "6": highest_qty()
    elif choice == "0": 
        print("Goodbye!")
        break
    else:
        print("Error")