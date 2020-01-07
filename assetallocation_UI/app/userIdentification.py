from random import seed
from random import randint

"""
    This function returns a random integer between 0 and 10 to create the id 
    returns: random integer
"""
def randomIdentification():
    seed(1)
    value = randint(1, 10)
    return value


print(randomIdentification())
