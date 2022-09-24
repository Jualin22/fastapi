import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

# fixtures are functions that run before specific test cases
@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(2, 3, 5), (3, 3, 6), (4, 5, 9)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(9, 4) == 36


def test_divide():
    assert divide(8, 4) == 2


def test_bank_set_initial_amount(bank_account: BankAccount):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account: BankAccount):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account: BankAccount):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account: BankAccount):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account: BankAccount):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == round(55, 6)


@pytest.mark.parametrize("deposited, withdrew, expected", [(200, 100, 100), (500, 300, 200), (1600, 800, 800)])
def test_bank_transaction(zero_bank_account: BankAccount, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insuficcient_funds(bank_account: BankAccount):
    # Exception is expected
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(500)
