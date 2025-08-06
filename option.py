#Option

class Option:
    
    def __init__(self, name, expiration, strike, premium):
        self.name = name
        self.expiration = expiration
        self.strike = strike
        self.premium = premium
        self.projection = 0
        self.date = 0
        self.score = 0
        self.type = 'idk'
        
    def __init__(self, name, expiration, strike, premium, projection, date, score, type1):
        self.name = name
        self.expiration = expiration
        self.strike = strike
        self.premium = premium
        self.projection = projection
        self.date = date
        self.score = score
        self.type = type1

    def getName():
        return self.name

    def getType():
        return self.type

    def getExpiration():
        return self.expiration

    def getStrike():
        return self.strike

    def getPremium():
        return self.premium

    def getProjection():
        return self.projection
    
    def getDate():
        return self.date

    def setPremium( premium ):
        self.premium = premium
        print(str(self.name) + " premium set to " + self.premium)

    def setProjection( projection ):
        self.projection = projection
        print(str(self.name) + " projection set to " + self.projection)
        
    def setDate( date ):
        self.delta = date
        print(str(self.name) + " date set to " + self.date)

    def getScore():
        return self.score
        
    def getType():
        if(self.type == 'call'):
            return 'call'
        elif(self.type == 'put'):
            return 'put'
        else:
            print("type error, learn how to fucking spell 'call or put' dumbass")
            return 0
        
    
