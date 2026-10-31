import json
import os
from datetime import datetime

ACCOUNTS_FILE = "accounts.json"
TRANSACTIONS_FILE = "transactions.json"


def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        accounts = {
            "100001": {
                "name": "Priya",
                "pin": "1234",
                "balance": 10000.0,
                "status": "Active"
            },
            "100002": {
                "name": "Rahul",
                "pin": "5678",
                "balance": 15000.0,
                "status": "Active"
            }
        }
        save_accounts(accounts)
        return accounts

    try:
        with open(ACCOUNTS_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(accounts, file, indent=4)


def load_transactions():
    if not os.path.exists(TRANSACTIONS_FILE):
        return {}

    try:
        with open(TRANSACTIONS_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, "w") as file:
        json.dump(transactions, file, indent=4)


class ATM:

    def __init__(self):
        self.accounts = load_accounts()
        self.transactions = load_transactions()
        self.current_account = None

    def pause(self):
        input("\nPress Enter to continue...")

    def add_transaction(self, transaction_type, amount):
        account_no = self.current_account

        if account_no not in self.transactions:
            self.transactions[account_no] = []

        transaction = {
            "type": transaction_type,
            "amount": amount,
            "balance": self.accounts[account_no]["balance"],
            "date": datetime.now().strftime("%d-%m-%Y"),
            "time": datetime.now().strftime("%H:%M:%S")
        }

        self.transactions[account_no].append(transaction)
        save_transactions(self.transactions)

    def login(self):
        print("\n================================")
        print("       WELCOME TO PYTHON ATM")
        print("================================")

        account_no = input("Enter Account Number: ").strip()

        if account_no not in self.accounts:
            print("Account not found.")
            return False

        account = self.accounts[account_no]

        if account["status"] != "Active":
            print("Account is blocked.")
            return False

        for attempt in range(3):
            pin = input("Enter 4-digit PIN: ").strip()

            if pin == account["pin"]:
                self.current_account = account_no
                print("\nLogin Successful!")
                print("Welcome", account["name"])
                self.pause()
                return True

            print("Incorrect PIN.")
            print("Attempts remaining:", 2 - attempt)

        account["status"] = "Blocked"
        save_accounts(self.accounts)

        print("Account blocked after 3 incorrect attempts.")
        return False

    def check_balance(self):
        account = self.accounts[self.current_account]

        print("\n========== BALANCE ==========")
        print("Account:", self.current_account)
        print("Name:", account["name"])
        print("Balance: Rs.", account["balance"])

        self.pause()

    def withdraw(self):
        account = self.accounts[self.current_account]

        print("\n========== WITHDRAW MONEY ==========")

        try:
            amount = float(input("Enter amount: Rs."))

            if amount <= 0:
                print("Invalid amount.")

            elif amount % 100 != 0:
                print("Amount must be a multiple of 100.")

            elif amount > 20000:
                print("Maximum withdrawal limit is Rs.20000.")

            elif amount > account["balance"]:
                print("Insufficient balance.")

            else:
                account["balance"] -= amount
                save_accounts(self.accounts)

                self.add_transaction("Withdrawal", amount)

                print("Withdrawal successful!")
                print("Withdrawn:", amount)
                print("Remaining balance:", account["balance"])

        except ValueError:
            print("Please enter a valid amount.")

        self.pause()

    def deposit(self):
        account = self.accounts[self.current_account]

        print("\n========== DEPOSIT MONEY ==========")

        try:
            amount = float(input("Enter amount: Rs."))

            if amount <= 0:
                print("Invalid amount.")

            elif amount > 50000:
                print("Maximum deposit limit is Rs.50000.")

            else:
                account["balance"] += amount
                save_accounts(self.accounts)

                self.add_transaction("Deposit", amount)

                print("Deposit successful!")
                print("Deposited:", amount)
                print("New balance:", account["balance"])

        except ValueError:
            print("Please enter a valid amount.")

        self.pause()

    def mini_statement(self):
        print("\n========== MINI STATEMENT ==========")

        history = self.transactions.get(self.current_account, [])

        if not history:
            print("No transactions found.")
        else:
            for item in history[-10:]:
                print("--------------------------------")
                print("Date:", item["date"])
                print("Time:", item["time"])
                print("Type:", item["type"])
                print("Amount:", item["amount"])
                print("Balance:", item["balance"])

        self.pause()

    def change_pin(self):
        account = self.accounts[self.current_account]

        print("\n========== CHANGE PIN ==========")

        old_pin = input("Enter old PIN: ").strip()

        if old_pin != account["pin"]:
            print("Incorrect old PIN.")
            self.pause()
            return

        new_pin = input("Enter new 4-digit PIN: ").strip()

        if not new_pin.isdigit() or len(new_pin) != 4:
            print("PIN must contain exactly 4 digits.")
            self.pause()
            return

        if new_pin == old_pin:
            print("New PIN must be different.")
            self.pause()
            return

        confirm_pin = input("Confirm new PIN: ").strip()

        if new_pin != confirm_pin:
            print("PIN does not match.")
            self.pause()
            return

        account["pin"] = new_pin
        save_accounts(self.accounts)

        print("PIN changed successfully!")
        self.pause()

    def account_details(self):
        account = self.accounts[self.current_account]

        print("\n========== ACCOUNT DETAILS ==========")
        print("Account Number:", self.current_account)
        print("Account Holder:", account["name"])
        print("Account Status:", account["status"])
        print("Balance:", account["balance"])

        self.pause()

    def receipt(self):
        account = self.accounts[self.current_account]

        print("\n========== ATM RECEIPT ==========")
        print("PYTHON ATM BANK")
        print("Account:", self.current_account)
        print("Name:", account["name"])
        print("Date:", datetime.now().strftime("%d-%m-%Y"))
        print("Time:", datetime.now().strftime("%H:%M:%S"))
        print("Balance:", account["balance"])
        print("Thank you for banking with us!")

        self.pause()

    def menu(self):
        while self.current_account:

            print("\n================================")
            print("          ATM MAIN MENU")
            print("================================")
            print("1. Check Balance")
            print("2. Withdraw Money")
            print("3. Deposit Money")
            print("4. Mini Statement")
            print("5. Change PIN")
            print("6. Account Details")
            print("7. Print Receipt")
            print("8. Logout")
            print("================================")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.check_balance()

            elif choice == "2":
                self.withdraw()

            elif choice == "3":
                self.deposit()

            elif choice == "4":
                self.mini_statement()

            elif choice == "5":
                self.change_pin()

            elif choice == "6":
                self.account_details()

            elif choice == "7":
                self.receipt()

            elif choice == "8":
                self.current_account = None
                print("Logout successful!")

            else:
                print("Invalid choice.")
                self.pause()

    def start(self):
        while True:

            if self.login():
                self.menu()

            print("\n1. Login Again")
            print("2. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "2":
                print("Thank you for using Python ATM!")
                break

            elif choice != "1":
                print("Invalid choice.")


if __name__ == "__main__":
    try:
        atm = ATM()
        atm.start()

    except KeyboardInterrupt:
        print("\nProgram stopped.")