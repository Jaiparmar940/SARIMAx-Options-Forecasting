#stock
class Stock:
    
    def __init__(self, name ):
        self.name = name
        self.price = 0
        self.shares = 0

    def getPrice(self):
        return self.price

    def getShares(self):
        return self.shares

    def getName(self):
        return self.name

    def setPrice(self, price):
        self.price = price
        print(str(self.name) + " price updated: " + str(price))

    def setShares(self, shares):
        self.shares = shares
        print(str(self.name) + " shares updated: " + str(shares))
