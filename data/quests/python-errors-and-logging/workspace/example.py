def safe_divide(a, b):
    try:
        print(a / b)
    except ZeroDivisionError:
        print("ERROR: DIVISOR_ZERO")

if __name__ == '__main__':
    safe_divide(10, 0)
    safe_divide(10, 2)
