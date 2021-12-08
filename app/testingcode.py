def add(x, y):
    c = x + y
    return c


def subst(x, y):
    c = x - y
    return c


def multi(x, y):
    c = x * y
    return c


def div(x, y):
    if y == 0:
        raise ValueError("Can not divide by Zero")
    elif x == 0:
        raise ValueError("If Zero divide by any number then output is Zero ")
    return x / y


def comput_hcf(x, y):
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small + 1):
        if (x % i == 0) and (y % i == 0):
            hcf = i
            return hcf


def prime(x, y):
    if x > 1 and y > 1:
        for i in range(2, x):
            if (x % i) == 0:
                print(x, "is not Prime Number")
                break
            else:
                print(x, "is Prime Number")

        for i in range(2, y):
            if (y % i) == 0:
                print(y, "is not Prime Number")
                break
            else:
                print(y, "is Prime Number")
    else:
        print(x, y, "is not a prime number")