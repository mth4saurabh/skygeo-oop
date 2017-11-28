import sys
sys.path.append("..")

from nose.tools import *
from bank.operations import *


class TestBankAccount(object):
    """Tests related to Bank Account base class, using initial_balance to
    keep track of the opening balance
    """

    initial_balance = 200.0

    def setup(self):
        self.account = BankAccount("test", "test@test.com", self.initial_balance)

    def teardown(self):
        print "Nothing to do here!"

    def test_balance(self):
        """Check if account balace was set properly"""
        assert self.account.balance == self.initial_balance

    def test_deposit(self):
        """Check if deposit to the account increments the balance correctly"""
        self.account.deposit(20.0)
        assert self.account.balance == self.initial_balance+20.0

    @raises(ValueError)
    def test_invalid_deposit(self):
        """Check that one can make deposits in negaitve amount, raise proper error"""
        self.account.deposit(-100.0)
        assert self.account.balance == self.initial_balance

    def test_withdrawal(self):
        """Check if withdrawal made to the account decrements the balance correctly"""
        self.account.withdraw(20.0)
        assert self.account.balance == self.initial_balance-20.0

    @raises(ValueError)
    def test_invalid_withdrawal(self):
        """Withdrawl with the amount leading to insufficinet funds can not be allowed.
        Check if balance remains the same, raise proper error"""
        self.account.withdraw(110.0)
        assert self.account.balance == self.initial_balance

    def test_min_balance(self):
        """Check weather class variable was set correctly and accessible"""
        assert self.account.minimum_balance == 100.0

    def test_min_balance_change(self):
        """Test classmethod which can change minimum balance for a class of accounts,
        for consistency once tested revert to the original amount"""
        BankAccount.set_minimum_balance(80.0)
        assert self.account.minimum_balance == 80.0
        BankAccount.set_minimum_balance(100.0)

    @raises(NotImplementedError)
    def test_ol_transaction(self):
        self.account.process_ol_transaction(110.0)
        assert self.account.balance == self.initial_balance

    def test_transfer(self):
        """Test valid transfer between two accounts, transaction fees should be deducted from
        the sender."""
        receiver = BankAccount("test2", "test2@test.com", 120.0)
        self.account.transfer(receiver, 20.0)
        assert self.account.balance == self.initial_balance-22.0
        assert receiver.balance == 140.0

    @raises(ValueError)
    def test_invalid_transfer(self):
        """Test invalid transfer between two accounts, check that balance of both the account
        remain same"""
        receiver = BankAccount("test2", "test2@test.com", 120.0)
        self.account.transfer(receiver, 100.0)
        assert self.account.balance == self.initial_balance
        assert receiver.balance == 120.0


class TestSavingsAccount(TestBankAccount):

    initial_balance = 120.0

    def setup(self):
        self.account = SavingsAccount("test", "test@test.com", self.initial_balance)

    def test_min_balance_change(self):
        SavingsAccount.set_minimum_balance(80.0)
        assert self.account.minimum_balance == 80.0


class TestCurrentAccount(TestBankAccount):

    initial_balance = 180.0

    def setup(self):
        self.account = CurrentAccount("test", "test@test.com", self.initial_balance)

    def test_min_balance(self):
        assert self.account.minimum_balance == 80.0

    def test_ol_transaction(self):
        """We only allow online transaction for current account, check that on valid
        transaction we deduct the correct amount along with the fees"""
        self.account.process_ol_transaction(20.0)
        assert self.account.balance == self.initial_balance-22.0

    @raises(ValueError)
    def test_failed_ol_transaction(self):
        """On invlaid online transaction balance must remain the same"""
        self.account.process_ol_transaction(100.0)
        assert self.account.balance == self.initial_balance