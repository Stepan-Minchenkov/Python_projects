checks_positives = [-20, -11.99, -7, 121, -5, -0.85, 40]
checks_negatives = [-20, -11.99, -7, 121, -5, -0.85, 40, -300]


def login():
    """
    pure function to return logon name of user
    output -- username
    """
    user = input("Please enter your user name: ")
    return user


def login_check(func):
    """
    decorator for adding logic check to any function
    """
    def inner(*args, **kwargs):
        user_name = login()
        if user_name != 'админ':
            print("Access denied")
            return 100
        value = func(*args, **kwargs)
        return value
    return inner


@login_check
def account(expenses: list):
    """
    input -- list of sums which were spent/obtained (debit/credit)
    output -- the final summary of money on the account
    """
    final_account = sum(expenses)
    if final_account < 0:
        print(f"You are in the red!! Your balance is: {final_account}. "
              f"Please put money on your account to avoid setting a fine upon you!")
    elif final_account > 0:
        print("You are in the green. Everything is good.")
    return sum(expenses)


account(checks_positives)
account(checks_negatives)
