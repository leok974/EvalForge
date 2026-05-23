def calculate_discount(amount, status):
    if status == 'premium':
        if amount > 1000:
            return amount * 0.20
        elif amount > 400:
            return amount * 0.15
        else:
            return amount * 0.10
    return 0

if __name__ == "__main__":
    # Question: What is the discount for amount=500 and status='premium'?
    print(calculate_discount(500, 'premium'))
