# Author: Phu Manh Nguyen
# Date: 12/17/2022

class Tax:
    def __init__(self, name, tax_amount):
        self.name = name
        self.__tax_amount = tax_amount

    def get_tax_amount(self):
        return self.__tax_amount

    def __str__(self) -> str:
        return f"The tax amount is ${self.get_tax_amount()}"
