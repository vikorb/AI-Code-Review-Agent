"""
Banking System - A clean Python script demonstrating best practices
with proper error handling, documentation, and organization.
"""

import logging
from datetime import datetime
from typing import List, Tuple, Dict, Optional, Union, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TransactionError(Exception):
    """Custom exception for transaction-related errors."""
    pass


class UserAccount:
    """
    Represents a user's bank account with balance and transaction tracking.
    
    Attributes:
        name (str): The account holder's name
        balance (float): Current account balance
        transaction_history (List): Record of all transactions
        created_at (datetime): When the account was created
    """
    
    def __init__(self, name: str, balance: float = 0) -> None:
        """
        Initialize a new user account.
        
        Args:
            name: The account holder's name
            balance: Initial account balance (default 0)
            
        Raises:
            ValueError: If initial balance is negative
        """
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
            
        self.name = name
        self.balance = balance
        self.transaction_history: List[Tuple[str, float, datetime]] = []
        self.created_at = datetime.now()
    
    def deposit(self, amount: float) -> bool:
        """
        Deposit funds into the account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            bool: True if deposit was successful
            
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
            
        self.balance += amount
        self.transaction_history.append(('deposit', amount, datetime.now()))
        logger.info(f"Deposited ${amount:.2f} to {self.name}'s account")
        return True
    
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw funds from the account if sufficient balance exists.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            bool: True if withdrawal was successful
            
        Raises:
            ValueError: If amount is not positive
            TransactionError: If insufficient funds
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
            
        if self.balance < amount:
            raise TransactionError("Insufficient funds")
            
        self.balance -= amount
        self.transaction_history.append(('withdraw', amount, datetime.now()))
        logger.info(f"Withdrew ${amount:.2f} from {self.name}'s account")
        return True
    
    def get_balance(self) -> float:
        """Get the current account balance."""
        return self.balance
    
    def get_transaction_history(self) -> List[Tuple[str, float, datetime]]:
        """Get the complete transaction history."""
        return self.transaction_history
    
    def get_account_age_days(self) -> int:
        """Calculate the account age in days."""
        delta = datetime.now() - self.created_at
        return delta.days


class BankingSystem:
    """
    Main banking system that manages multiple user accounts.
    
    This class provides methods for account creation, transactions,
    and reporting.
    """
    
    def __init__(self) -> None:
        """Initialize the banking system with an empty accounts dictionary."""
        self.accounts: Dict[str, UserAccount] = {}
    
    def create_account(self, name: str, initial_balance: float = 0) -> Optional[UserAccount]:
        """
        Create a new user account.
        
        Args:
            name: Account holder's name
            initial_balance: Starting balance (default 0)
            
        Returns:
            UserAccount or None if account creation failed
            
        Raises:
            ValueError: If initial balance is negative
        """
        if name in self.accounts:
            logger.warning(f"Account '{name}' already exists")
            return None
        
        try:
            new_account = UserAccount(name, initial_balance)
            self.accounts[name] = new_account
            logger.info(f"Created new account for {name}")
            return new_account
        except ValueError as e:
            logger.error(f"Failed to create account: {e}")
            raise
    
    def get_account(self, name: str) -> UserAccount:
        """
        Retrieve an account by name.
        
        Args:
            name: Account holder's name
            
        Returns:
            UserAccount
            
        Raises:
            KeyError: If account doesn't exist
        """
        if name not in self.accounts:
            logger.error(f"Account '{name}' not found")
            raise KeyError(f"Account '{name}' does not exist")
            
        return self.accounts[name]
    
    def process_transaction(
        self, account_name: str, transaction_type: str, amount: float
    ) -> bool:
        """
        Process a deposit or withdrawal transaction.
        
        Args:
            account_name: Account holder's name
            transaction_type: Either 'deposit' or 'withdraw'
            amount: Amount to deposit or withdraw
            
        Returns:
            bool: True if transaction was successful
            
        Raises:
            KeyError: If account doesn't exist
            ValueError: If transaction type is invalid
            TransactionError: If transaction fails
        """
        try:
            account = self.get_account(account_name)
            
            if transaction_type == 'deposit':
                return account.deposit(amount)
            elif transaction_type == 'withdraw':
                return account.withdraw(amount)
            else:
                logger.error(f"Invalid transaction type: {transaction_type}")
                raise ValueError(f"Unknown transaction type: {transaction_type}")
                
        except (KeyError, ValueError, TransactionError) as e:
            logger.error(f"Transaction failed: {e}")
            raise
    
    def transfer_funds(self, from_account: str, to_account: str, amount: float) -> bool:
        """
        Transfer funds between two accounts.
        
        Args:
            from_account: Source account name
            to_account: Destination account name
            amount: Amount to transfer
            
        Returns:
            bool: True if transfer was successful
            
        Raises:
            Various exceptions based on errors in withdrawal or deposit
        """
        try:
            # Get accounts (will raise KeyError if not found)
            source = self.get_account(from_account)
            destination = self.get_account(to_account)
            
            # Perform withdrawal (will raise TransactionError if insufficient funds)
            source.withdraw(amount)
            
            # Perform deposit
            destination.deposit(amount)
            
            logger.info(f"Transferred ${amount:.2f} from {from_account} to {to_account}")
            return True
            
        except Exception as e:
            logger.error(f"Transfer failed: {e}")
            raise
    
    def generate_account_report(self, account_name: str) -> Dict[str, Any]:
        """
        Generate a comprehensive report for an account.
        
        Args:
            account_name: Account holder's name
            
        Returns:
            Dict containing account information
            
        Raises:
            KeyError: If account doesn't exist
        """
        account = self.get_account(account_name)
        
        report = {
            "name": account.name,
            "balance": account.balance,
            "created_at": account.created_at,
            "account_age_days": account.get_account_age_days(),
            "transaction_count": len(account.transaction_history)
        }
        
        # Add last transaction if available
        if account.transaction_history:
            last_tx = account.transaction_history[-1]
            report["last_transaction"] = {
                "type": last_tx[0],
                "amount": last_tx[1],
                "timestamp": last_tx[2]
            }
        
        return report
    
    def calculate_interest(
        self, account_name: str, rate: float, time_years: float
    ) -> float:
        """
        Calculate simple interest for an account.
        
        Args:
            account_name: Account holder's name
            rate: Annual interest rate (decimal)
            time_years: Time period in years
            
        Returns:
            float: Interest amount
            
        Raises:
            KeyError: If account doesn't exist
            ValueError: If rate or time is negative
        """
        if rate < 0:
            raise ValueError("Interest rate cannot be negative")
            
        if time_years < 0:
            raise ValueError("Time period cannot be negative")
            
        account = self.get_account(account_name)
        principal = account.get_balance()
        
        interest = principal * rate * time_years
        logger.info(
            f"Calculated interest for {account_name}: "
            f"${interest:.2f} (${principal:.2f} at {rate:.1%} for {time_years} years)"
        )
        
        return interest


def main() -> None:
    """Main function demonstrating the banking system."""
    # Create a banking system
    bank = BankingSystem()
    
    try:
        # Create accounts
        bank.create_account("Alice", 1000)
        bank.create_account("Bob", 500)
        
        # Perform transactions
        bank.process_transaction("Alice", "deposit", 200)
        bank.process_transaction("Bob", "withdraw", 100)
        
        # Transfer funds
        bank.transfer_funds("Alice", "Bob", 300)
        
        # Calculate interest
        interest = bank.calculate_interest("Alice", 0.05, 1)
        print(f"Alice's interest: ${interest:.2f}")
        
        # Generate and print reports
        for name in ["Alice", "Bob"]:
            report = bank.generate_account_report(name)
            print(f"\nAccount Report for {name}:")
            print(f"Current Balance: ${report['balance']:.2f}")
            print(f"Account Age: {report['account_age_days']} days")
            print(f"Transactions: {report['transaction_count']}")
            
            if "last_transaction" in report:
                last_tx = report["last_transaction"]
                print(
                    f"Last Transaction: {last_tx['type']} of "
                    f"${last_tx['amount']:.2f} on {last_tx['timestamp']}"
                )
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()