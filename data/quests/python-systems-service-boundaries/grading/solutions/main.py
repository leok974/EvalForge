class PaymentService:
    def process(self, amount):
        if amount < 0: raise ValueError('Negative')
        return True