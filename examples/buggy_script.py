# A buggy Python script with various issues
import random, os, sys
import time 
from datetime import datetime,timedelta

class userAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
        self.transaction_history = []
        
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(('deposit', amount, datetime.now()))
            return True
        return False
    
    def withdraw(self, amount):
        # Bug: No check if amount is positive
        if self.balance >= amount:
            self.balance -= amount
            self.transaction_history.append(('withdraw', amount, datetime.now()))
            return True
        return False
        
    def get_balance(self):
        return self.balance
    
    # Bug: Function is not implemented
    def get_transaction_history(self):
        pass
    
# Global variable
accounts = {}

def create_account(name, initial_balance=0):
    if name in accounts:
        print(f"Error: Account {name} already exists")
        return None
    
    # Bug: No validation on initial_balance
    new_account = userAccount(name, initial_balance)
    accounts[name] = new_account
    return new_account

def calculate_interest(principal, rate, time):
    # Bug: No type checking or validation
    return principal * rate * time

def process_transaction(account_name, transaction_type, amount):
    # Bug: Missing account existence check
    account = accounts[account_name]
    
    if transaction_type == 'deposit':
        result = account.deposit(amount)
    elif transaction_type == 'withdraw':
        result = account.withdraw(amount)
    else:
        # Bug: Return value is inconsistent with other branches
        print(f"Unknown transaction type: {transaction_type}")
    
    # Bug: 'result' might not be defined in all code paths
    return result

def generate_report(account_name):
    # Bug: No error handling if account doesn't exist
    account = accounts.get(account_name)
    
    print(f"Account Report for {account.name}")
    print(f"Current Balance: ${account.balance}")
    
    # Bug: This will cause an error if transaction_history is empty
    last_transaction = account.transaction_history[-1]
    print(f"Last Transaction: {last_transaction[0]} of ${last_transaction[1]} on {last_transaction[2]}")
    
    # Bug: Undefined variable
    print(f"Account age: {account_age} days")
    
    return True

def transfer_funds(from_account, to_account, amount):
    # Bug: No check if accounts exist
    # Bug: No check if amount is positive
    if accounts[from_account].withdraw(amount):
        accounts[to_account].deposit(amount)
        return True
    else:
        return False

# Main program
if __name__ == "__main__":
    # Create some accounts
    create_account("Alice", 1000)
    create_account("Bob", 500)
    create_account("Charlie", -50)  # Bug: Negative initial balance
    
    # Perform some transactions
    process_transaction("Alice", "deposit", 200)
    process_transaction("Bob", "withdraw", 100)
    
    # Bug: This will cause KeyError
    process_transaction("Dave", "deposit", 300)
    
    # Generate a report
    generate_report("Alice")
    
    # Calculate interest
    # Bug: Time should be in years, not as a string
    interest = calculate_interest(1000, 0.05, "1 year")
    print(f"Interest earned: ${interest}")
    
    # Bug: Unused import
    random_number = random.randint(1, 10)