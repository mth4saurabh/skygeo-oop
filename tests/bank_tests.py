import sys
sys.path.append("..")

from nose.tools import *
from bank.operations import *


class TestBankAccount(object):

    initial_balance = 200.0

    def setup(self):
        self.account = BankAccount("test", "test@test.com", self.initial_balance)

    def teardown(self):
        print "Nothing to do here!"

    def test_balance(self):
        assert self.account.balance == self.initial_balance

    def test_deposit(self):
        self.account.deposit(20.0)
        assert self.account.balance == self.initial_balance+20.0

    @raises(ValueError)
    def test_invalid_deposit(self):
        self.account.deposit(-100.0)
        assert self.account.balance == self.initial_balance

    def test_withdrawal(self):
        self.account.withdraw(20.0)
        assert self.account.balance == self.initial_balance-20.0

    @raises(ValueError)
    def test_invalid_withdrawal(self):
        self.account.withdraw(110.0)
        assert self.account.balance == self.initial_balance

    def test_min_balance(self):
        assert self.account.minimum_balance == 100.0

    def test_min_balance_change(self):
        BankAccount.set_minimum_balance(80.0)
        assert self.account.minimum_balance == 80.0
        BankAccount.set_minimum_balance(100.0)

    @raises(NotImplementedError)
    def test_ol_transaction(self):
        self.account.process_ol_transaction(110.0)
        assert self.account.balance == self.initial_balance

    def test_transfer(self):
        receiver = BankAccount("test2", "test2@test.com", 120.0)
        self.account.transfer(receiver, 20.0)
        assert self.account.balance == self.initial_balance-22.0
        assert receiver.balance == 140.0

    @raises(ValueError)
    def test_invalid_transfer(self):
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
        self.account.process_ol_transaction(20.0)
        assert self.account.balance == self.initial_balance-22.0

    @raises(ValueError)
    def test_failed_ol_transaction(self):
        self.account.process_ol_transaction(100.0)
        assert self.account.balance == self.initial_balance