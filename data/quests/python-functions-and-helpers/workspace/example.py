def calculate_tax(amount):
    return amount * 0.08

def format_currency(amount):
    return f"${amount:.2f}"

if __name__ == '__main__':
    price = 100.0
    tax = calculate_tax(price)
    print(f"Total: {format_currency(price + tax)}")
