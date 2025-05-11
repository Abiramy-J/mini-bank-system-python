# ==== File Constants ====
ADMIN_FILE = "admin.txt"  #store admin id and password
CUSTOMER_FILE = "customers.txt"  #store customers personal details
USER_FILE = "users.txt" #store customer ID , password, name and Nic
ACCOUNT_FILE = "bank_acc.txt"  # store customers id, Acc number and Current balance
TRANSACTION_FILE = "transactions.txt" # to store acc number, type(deposit or withdraw), amount
ID_COUNTER_FILE = "id_counter.txt" # to generate unique customer id
ACC_COUNTER_FILE = "acc_counter.txt" # to generate unique account number
DELETE_CUSTOMER_FILE = "delete_cust.txt" # to store deleted customer details

def admin_signup():
    while True:
        print("--- Admin Sign Up ---")
        user_id = input("Create admin user ID: ")
        while True:
            print("Password must be 6 to 12 digits")
            password = input("Create a strong password: ")
            if password.isdigit() and 6 <= len(password) <= 12:
                break
            else:
                print("password should be in 6 to 12 digits")
        try:
            with open("admin.txt", "r") as file:
                for line in file:
                    existing_user = line.strip().split(",")[0]
                    if existing_user == user_id:
                        print("⚠️This ID already exists. Try another.\n")
                        break
                else:
                    with open("admin.txt", "a")as f:
                        f.write(f"{user_id},{password}\n")
                    print("✅Admin created successfully!Now you can login...")
                    break
        except FileNotFoundError:
            with open("admin.txt", "a") as file:
                file.write(f"{user_id},{password}\n")
            print("✅Admin created successfully!Now you can login...")
            break

def admin_login():
    print("--- Admin Login ---")

    try:
        with open("admin.txt", "r") as file:
            lines = file.readlines()
            if not lines:  # file is empty
                print("No admin found. Redirecting to signup...")
                admin_signup()
                return False
    except FileNotFoundError:
        print("Admin file not found. Redirecting to signup...")
        admin_signup()
        return False

    user_id = input("Enter admin ID: ")
    password = input("Enter password: ")

    for line in lines:
        existing_user, existing_pass = line.strip().split(",")
        if user_id == existing_user and password == existing_pass:
            print("✅ Login successful!")
            return True
        
    print("Invalid credentials. Try again ")
    return False
#generate unique customer ID
def generate_customer_id():
    try:
        with open("id_counter.txt", "r") as f:
            content=f.read().strip()
            if content:
                last_id = int(content)
            else:
                last_id=100
    except FileNotFoundError:
        last_id = 100
    new_id = f"cust{last_id}"
    with open("id_counter.txt", "w") as f:
        f.write(str(last_id + 1))
    return new_id
#generate unique account number
def generate_account_number():
    try:
        with open("acc_counter.txt", "r") as f:
            content = f.read().strip()
            if content:
                last_acc = int(content)
            else:
                last_acc = 1000
    except FileNotFoundError:
        last_acc = 1000
    new_acc = f"ACC{last_acc}"
    with open("acc_counter.txt", "w") as f:
        f.write(str(last_acc + 1))
    return new_acc

#generate unique customer password
def generate_password(customer_id):
    return customer_id + "123"

accounts = {}  #global dictionary to store all account data
def create_customer_account():
    print("=== Create Customer Account ===")
    name = input("Enter name: ")
    while True:
        age = input("Enter age:" )
        if age.isdigit() and 18 <= int(age) <= 100:
            break
        else:
            print("⚠️Enter must be between 18 and 100 ")
    while True:
        nic = input("Enter NIC number: ").strip()
        if (nic.isdigit() and len(nic) == 12) or (len(nic) == 10 and nic[:-1].isdigit() and nic[-1].upper() == 'V'):
            break
        else:
            print("⚠️Invalid NIC. Enter either 12-digit NIC or 9 digits followed by 'V'.")

    address = input("Enter address: ")
    while True:
        email = input("Enter your email: ")
        if "@" in email and email.endswith(".com"):
            break
        else:
            print("⚠️Invalid email. It must contain '@' and end with '.com'. Please try again.")

    while True:
        mobile_no = input("Enter Mobile number: ")
        if mobile_no.isdigit() and len(mobile_no)==10 and (mobile_no.startswith("07") or mobile_no.startswith("021")) :
            break
        else:
            print("⚠️Enter valid 10 digit mobile number that start with '077' or '021'!")
    while True:
        try:
            initial_balance = float(input("Enter initial balance: "))
            if initial_balance >= 500:
                break
            else:
                print("Balance must be at least Rs.500 ")
        except ValueError:
            print("Error⚠️: Please enter a valid number.")

    customer_id = generate_customer_id()
    account_number = generate_account_number()
    password = generate_password(customer_id)
    #store the details in the global accounts dictionary
    accounts[account_number]={
        "name" : name,
        "customer_id": customer_id,
        "password": password,
        "balance": initial_balance,
        "transaction":[f"+{initial_balance}"]
    }
    with open("users.txt", "a") as f:
        f.write(f"{customer_id},{password},{name},{nic}\n")

    with open("customers.txt", "a") as f:
        f.write(f"{customer_id},{name},{age},{nic},{address},{email},{mobile_no},{account_number}\n")

    with open("bank_acc.txt", "a") as f:
        f.write(f"{account_number},{customer_id},{initial_balance}\n")

    print("✅Customer created successfully!")
    print(f"customer name :{name}")
    print(f"Customer ID: {customer_id}")
    print(f"Account Number: {account_number}")
    print(f"Password: {password}")

# === Update customer details ===
def update_customer_details():
    print("--- Update Customer Details ---")
    customer_id = input("Enter the Customer ID to update: ")
    updated_lines = []
    found = False
    try:
        with open("customers.txt", "r") as f:
            lines = f.readlines()
        for line in lines:
            parts = line.strip().split(",")
            if parts[0] == customer_id:
                found = True
                print("Current details:")
                print(f"Name: {parts[1]}, Age: {parts[2]}, NIC: {parts[3]}, Address: {parts[4]}, Email: {parts[5]} , Mobile number: {parts[6]}, Account no: {parts[7]}")
                print("Leave a blank to keep the current value.\n")
                name = input("Enter new name: ") or parts[1]
                while True:
                    age = input("Enter new age:") or parts[2]
                    if age.isdigit() and 18 <= int(age) <= 100:
                        break
                    else:
                        print("⚠️Enter must be between 18 and 100 ")
                while True:
                    nic = input("Enter NIC number: ").strip() or parts[3]
                    if (nic.isdigit() and len(nic) == 12) or (len(nic) == 10 and nic[:-1].isdigit() and nic[-1].upper() == 'V'):
                        break
                    else:
                        print("⚠️Invalid NIC. Enter either 12-digit NIC or 9 digits followed by 'V'.")

                address = input("Enter address: ") or parts[4]
                while True:
                    email = input("Enter your email: ") or parts[5]
                    if "@" in email and email.endswith(".com"):
                        break
                    else:
                        print("⚠️Invalid email. It must contain '@' and end with '.com'. Please try again.")

                while True:
                    mobile_no = input("Enter Mobile number: ") or parts[6]
                    if mobile_no.isdigit() and len(mobile_no)==10 and (mobile_no.startswith("07") or mobile_no.startswith("021")):
                        break
                    else:
                        print("⚠️Enter valid 10 digit mobile number that start with '077' or '021'!")
                updated_line = f"{customer_id},{name},{age},{nic},{address},{email},{mobile_no},{get_account_number(customer_id)}"
                updated_lines.append(updated_line + "\n")
            else:
                updated_lines.append(line)
        if found:
            with open("customers.txt", "w") as f:
                f.writelines(updated_lines)
            print("✅Customer details updated successfully!")
        else:
            print("Customer ID not found.")
    except FileNotFoundError:
        print("Customer records not found.")
def delete_line_from_line(filename,keyword):
    try:
        with open(filename,"r")as file:
            lines=file.readlines()
        with open(filename,"w")as file:
            found=False
            for line in lines:
                if keyword  not in line:
                    file.write(line)
                else:
                    found=True
        return found
    except FileNotFoundError:
        print(f"{filename}file not found⚠️")
        return False
def delete_customer_account():
    print("====Delete Customer Account===")
    customer_id=input("Enter the Customer ID to delete: ")
    
    try:
        with open("customers.txt","r")as file:
            lines=file.readlines()
            for line in lines:
                if customer_id in line:
                    with open("delete_cust.txt","a")as backup:
                        backup.write(line)
                    break
    except FileNotFoundError:
        print("customers.txt file not found")

    # delete the customer from other files
    found=delete_line_from_line("customers.txt",customer_id)
    delete_line_from_line("bank_acc.txt",customer_id)
    delete_line_from_line("users.txt",customer_id)
    delete_line_from_line("transactions.txt",customer_id)

    if found:
        print("✅customer account deleted successfully!")
    else:
        print("⚠️customer id not found")


def view_all_customers():
    print("==== All Customer Details ===")
    try:
        with open("customers.txt","r")as file:
            lines=file.readlines()
            if not lines:
                    print("No customer records found")
                    return
            #header
            print(f"{'cust ID':<10}{'Name':<25}{'Age':<5}{'Nic':<15}{'Address':<25}{'Email':<35}{'Mobile_No':<12}{'Acc No':<10}")
            print("_"*140)
            #customer rows
            for line in lines:
                parts=line.strip().split(",")
                print(f"{parts[0]:<10}{parts[1]:<25}{parts[2]:<5}{parts[3]:<15}{parts[4]:<25}{parts[5]:<35}{parts[6]:<12}{parts[7]:<10}")
    except FileNotFoundError:
        print("Customer records file not found.")

def customer_login():
    customer_id = input("Enter your ID: ")
    customer_password = input("Enter password: ")
    try:
        with open("users.txt", "r") as file:
            for line in file:
                existing_id = line.strip().split(",")[0]
                existing_password=line.strip().split(",")[1]
                if existing_id == customer_id and existing_password == customer_password:
                    print("Login successful, Welcome🙏!")
                    customer_menu(customer_id) #call menu if login successful
                    return
        print("Invalid customer ID or password.Try again.\n")
    except FileNotFoundError:
        print("Error: Users file not found.")
def get_account_number(customer_id):
    try:
        with open("customers.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == customer_id:
                    return data[-1]  #return acc number

    except FileNotFoundError:
        print("Error: 'customers.txt' file not found.")
    return None


def deposit(customer_id):
    print("=== Deposit Money ===")
#get account number associated with customer id
    account_number = get_account_number(customer_id)
    if not account_number:
        print("Account not found.")
        return

    try:
        #Ask for deposit amount
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    updated_lines = []  # to store updated content of bank_acc.txt
    found = False  #to check if account was found

    # Read and update the account balance in bank_acc.txt
    try:
        with open("bank_acc.txt", "r") as f:
            for line in f:
                acc_no, cid, balance = line.strip().split(",")
                if acc_no == account_number and cid == customer_id:
                    found = True
                    # Update balance by adding the deposit amount
                    balance = float(balance) + amount
                    updated_lines.append(f"{acc_no},{cid},{balance}\n")  # Update the line
                else:
                    updated_lines.append(line)  #Keep the other lines unchanged
    except FileNotFoundError:
        print("Bank account file not found.")
        return

    if not found:
        print("Account not found.")
        return

    #updated data back to bank_acc.txt
    with open("bank_acc.txt", "w") as f:
        f.writelines(updated_lines)

    # add transaction to the transaction history
    with open("transactions.txt", "a") as f:
        f.write(f"{customer_id},Deposit,{amount}\n")

    print(f"Successfully deposited ✅")


def withdraw(customer_id):
    print("=== Withdraw Money ===")

    # get account number associated with customer_id
    account_number = get_account_number(customer_id)
    if not account_number:
        print("Account not found.")
        return

    try:
        #ask for withdrawal amount
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    updated_lines = []  # to store updated content of bank_acc.txt
    found = False  # to check if account was found
    sufficient_balance = False # to check if there is enough balance

    #read and update the account balance in bank_acc.txt
    try:
        with open("bank_acc.txt", "r") as f:
            for line in f:
                acc_no, cid, balance = line.strip().split(",")
                if acc_no == account_number and cid == customer_id:
                    found = True
                    balance = float(balance)
                    if balance >= amount:
                        #Update balance by subtracting the withdrawal amount
                        balance -= amount
                        sufficient_balance = True
                        updated_lines.append(f"{acc_no},{cid},{balance}\n")  #update the line
                    else:
                        print("Insufficient balance.")
                        return
                else:
                    updated_lines.append(line)  #keep the other lines unchanged
    except FileNotFoundError:
        print("Bank account file not found.")
        return

    if not found:
        print("Account not found.")
        return

    if sufficient_balance:
        #update data back to bank_acc.txt
        with open("bank_acc.txt", "w") as f:
            f.writelines(updated_lines)

        #save the transaction to the transaction history
        with open("transactions.txt", "a") as f:
            f.write(f"{customer_id},Withdraw,{amount}\n")

        print(f"Successfully withdrew.✅")


def view_transaction_summary(customer_id):
    print("=== Transaction Summary ===")

     #get the account number of the customer(step01)
    account_number = get_account_number(customer_id)
    if not account_number:
        print("Account number not found.")
        return

    #get the initial balance from bank_acc.txt(step02)
    try:
        with open("bank_acc.txt", "r") as f:
            for line in f:
                acc_no, cid, bal = line.strip().split(",")
                if acc_no == account_number and cid == customer_id:
                    current_balance = float(bal)
                    break
            else:
                print("Account not found in bank file.")
                return
    except FileNotFoundError:
        print("bank_acc.txt file not found.")
        return

    #read the transactions and apply them in order to get a running balance(step03)
    transactions_dict = {}  # create an empty dictionary

    #read file and fill the dictionary
    try:
        with open("transactions.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                cid = parts[0]  # customer_id from file
                action = parts[1]
                amount = float(parts[2])

            #Store in dictionary 
                if cid not in transactions_dict:
                    transactions_dict[cid] = []
                transactions_dict[cid].append((action, amount))

    except FileNotFoundError:
        print("Transaction file not found.")
        return

    #get transactions for this customer from the dictionary
    transactions = transactions_dict.get(customer_id, [])

    if not transactions:
        print("No transactions found.")
        print(f"Current Balance: Rs.{current_balance:.2f}")
        return
        # Step to calculate initial balance
    initial_balance = current_balance
    for action, amount in transactions[::-1]:
        if action == "Deposit":
            initial_balance -= amount
        elif action == "Withdraw":
            initial_balance += amount
    #reverse calculate from current balance (last transaction to first)
    #transactions = transactions[::-1]  # reverse the list to go backwards
    balances = []
    bal = initial_balance

    for action, amount in transactions:
        if action == "Deposit":
            bal += amount
        elif action == "Withdraw":
            bal -= amount
        balances.append((action,amount,bal))

    #balances = balances[::-1]  #put them back in correct order

    print(f"{'Account No.':<15}{'Type':<10}{'Amount':<10}{'Balance':<10}")
    print("-" * 70)
    print(f"{account_number:<15}{'Initial':<10}{'':<10}Rs.{initial_balance:<9.2f}")

    for action, amount, bal_after in balances:
        print(f"{account_number:<15}{action:<10}Rs.{amount:<9.2f}Rs.{bal_after:<9.2f}")

    print("-" * 70)
    print(f"Final Balance: Rs.{current_balance:.2f}")


def check_balance(customer_id):
    account_number=get_account_number(customer_id)
    if not account_number:
        print("Account number is not found")
        return
    balance=None
    try:
        with open("bank_acc.txt","r")as file:
            for line in file:
                acc_no,cid,bal=line.strip().split(",")
                if acc_no==account_number and cid==customer_id:
                    balance=float(bal)
                    break
    except FileNotFoundError:
        print("bank_acc.txt file not found")
    if balance is None:
        print("could not receive balance")
        return
    print(f"your current balance is : Rs{balance}")
def change_customer_password():
    # Ask for customer ID and current password
    customer_ID = input("Enter your customer ID: ").strip()
    customer_password = input("Enter your current password: ").strip()

    try:
        #Open the file and read all lines into a list
        with open("users.txt", "r") as file:
            lines = file.readlines()

        #Loop through each line with index to find the matching customer
        for index, line in enumerate(lines):
            parts = line.strip().split(",")  #split each line into fields
            if parts[0] == customer_ID and parts[1] == customer_password:
                #found the user, now ask for new password in a loop
                while True:
                    print("\nNew password must be exactly 8 characters and include at least 1 number.")
                    new_password = input("Enter your new password: ").strip()
                    confirm_password = input("Re-enter your new password: ").strip()

                    #Validate password length
                    if len(new_password) != 8:
                        print("❌Password must be exactly 8 characters.")
                        continue

                    #Check for at least one number
                    if not any(char.isdigit() for char in new_password):
                        print("❌Password must include at least one number.")
                        continue

                    #check if both passwords match
                    if new_password != confirm_password:
                        print("❌Passwords do not match!")
                        continue

                    #update the password only (index 1 is password)
                    parts[1] = new_password
                    lines[index] = ",".join(parts) + "\n"  # Rebuild the line

                    #Write updated data back to the file
                    with open("users.txt", "w") as file:
                        file.writelines(lines)

                    print("✅ Password updated successfully! 👍")
                    return  #Exit after successful update

        #If no match is found after checking all lines
        print("❌Customer ID or password is incorrect.")

    except FileNotFoundError:
        print("❌users.txt file not found.")
        
def main_menu():
    print("===*WELCOME!🙏*===")
    while True:
        print("=====Mini Bank Application=====")
        print("1.Admin Login")
        print("2.Customers Login")
        print("3.Exit")
        choice = input("Enter your Choice:")

        if choice == "1":
            if admin_login():
                admin_menu()
        elif choice == "2":
            customer_login()
        elif choice == "3":
            print("Main menu closed. See you again! 😊")
            break
        else:
            print("Invalid choice.Try Again!")
def admin_menu():
    while True:
        print("-==Admin Menu==-")
        print("1.Create Admin")
        print("2.Create customer")
        print("3.View all customers")
        print("4.Update customer")
        print("5.Delete customer account")
        print("6.Change customer password")
        print("7.Log out")
        choice = input("Enter your choice in Admin Menu:")

        if choice == "1":
            admin_signup()
        elif choice == "2":
            create_customer_account()
        elif choice == "3":
            view_all_customers()
        elif choice=="4":
            update_customer_details()
        elif choice=="5":
            delete_customer_account()
        elif choice == "6":
            change_customer_password()
        elif choice == "7":
            print("👋 Admin logged out successfully. See you soon!")
            break
        else:
            print("Invalid choice.try again!")

def customer_menu(customer_id):
    while True:
        print("=== Customer Menu ===")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5.Change password")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            deposit(customer_id)
        elif choice == "2":
            withdraw(customer_id)
        elif choice == "3":
            check_balance(customer_id)
        elif choice == "4":
            view_transaction_summary(customer_id)
        elif choice == "5":
            change_customer_password()
        elif choice == "6":
            print(" Thank you for banking with us🏦,Have a great day! 😊")
            break
        else:
            print("Invalid choice. Please try again.")




main_menu()               