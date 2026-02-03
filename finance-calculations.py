import math

# Asks the user if they have a bond or investment
choice = input("Investment - to calculate the amount of interest you'll earn on your investment\n" "Bond - to calculate the amount you'll have to pay on a home loan\n" "Enter either 'investment' or 'bond' from the menu above to proceed: ").lower()

#Ask user to input details
if choice == "investment":
    deposit = float(input("Enter the amount of money you are depositing: "))
    rate = float(input("Enter the interest rate: "))
    years = int(input("Enter the number of years you plan to invest: "))
    type = input("Do you want simple or compound interest? ").lower()

# Formula for interest
    r = rate / 100
    if type == "simple":
        total = deposit * (1 + r * years)
        print(f"The total amount after {years} simple interest is: {total:.2f}")
    elif type == "compound":
        total = deposit * math.pow((1 + r), years)
        print(f"The total amount after {years} years with compound interest is: {total:.2f}")
    else:
        print("Invalid")

# Ask user to input details
elif choice == "bond":
    value = float(input("Enter present value of house: "))
    rate = float(input("Enter yearly interest rate: "))
    months = int(input("Enter number of months to repay: "))

# Formula for bond
    i = (rate / 100) / 12
    repay = (i * value) / (1 - (1 + i)**(-months))
    print(f"The amount you will have to repay each month is: {repay:.2f}")

# Displays error message if invalid input entered
else:
    print("Invalid entry")
