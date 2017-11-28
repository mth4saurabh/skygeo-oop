
class BankAccount(object):

    minimum_balance, transaction_fee = 100.0, 2.0

    def __init__(self, fullname, email, initial_balance):
        """Raise error if initial balance is insufficient"""
        if initial_balance < self.minimum_balance:
            raise ValueError('Account requires minimum balance of ${}' \
                .format(self.minimum_balance))
        self.fullname = fullname
        self.email = email
        self._balance = initial_balance
        
    def deposit(self, amount):
        """Make a deposit, amount needs to be greater than equal to zero"""
        if amount < 0:
            raise ValueError('Deposit amount can not be negative')
        self._balance += amount

    def withdraw(self, amount):
        """Make a withdrawal, show insufficient if funds are below minimum required balance"""
        if self._balance-amount < self.minimum_balance:
            raise ValueError('Insufficient funds, you can make maximum withdrawal of ${}' \
                .format(self._balance-self.minimum_balance))
        self._balance -= amount

    def process_ol_transaction(self, amount):
        raise NotImplementedError('Online transaction are only allowed for current account.')

    @classmethod
    def set_minimum_balance(cls, amount):
        """Set minimum balance for type on account"""
        cls.minimum_balance = amount

    @property
    def balance(self):
        """Check current balance of the account"""
        return self._balance


    """
    Overriding some useful dunder methods for our class
    """
    def __repr__(self):
        return "'{}'('{}','{}')".format(self.__class__.__name__, self.fullname, self.balance)
    def __str__(self):
        return 'Account Details:\n Name: {}\n Balance: {}\n'.format(self.fullname, self.balance)


class SavingsAccount(BankAccount):

    def __init__(self, fullname, email, initial_balance):
        super(SavingsAccount, self).__init__(fullname, email, initial_balance)


class CurrentAccount(BankAccount):
    minimum_balance = 80.0

    def __init__(self, fullname, email, initial_balance):
        super(CurrentAccount, self).__init__(fullname, email, initial_balance)

    def process_ol_transaction(self, amount):
        try:
            self.withdraw(amount+self.transaction_fee)
        except Exception:
            raise ValueError('Sorry, could not process the transaction. Please check your funds')