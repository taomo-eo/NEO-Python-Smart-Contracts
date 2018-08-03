"""
Example addresses
AdbSfjRBY3MyAqbvmTussSpNpR5SQda3XA
ANiU2cwRnWes9udGdUEKfWb6ba4wd5v8A3
AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y
AZ9Bmz6qmboZ4ry1z8p2KF3ftyA2ckJAym
"""

from boa.interop.Neo.Storage import Get,Put,Delete,GetContext

def Main(operation, addr, value):


    if not is_valid_addr(addr):
        return False

    context = GetContext()

    if operation == 'add':
        balance = Get(context, addr)
        new_balance = balance + value
        Put(context, addr, new_balance)
        return new_balance

    elif operation == 'remove':
        balance = Get(context, addr)
        Put(context, addr, balance - value)
        return balance - value

    elif operation == 'balance':
        return Get(context, addr)

    return False

def is_valid_addr(addr):

    if len(addr) == 20:
        return True
    return False
