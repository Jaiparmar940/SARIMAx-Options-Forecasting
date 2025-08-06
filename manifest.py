#manifest  
from stock import Stock

class Manifest:

    def getList():

        sList = []
            
        s1 = Stock("AAPL")
        sList.append(s1)
            
        s2 = Stock("MSFT")
        sList.append(s2)
            
        s3 = Stock("WMT")
        sList.append(s3)
            
        s4 = Stock("FAS")
        sList.append(s4)
            
        s5 = Stock("JNJ")
        sList.append(s5)
            
        s6 = Stock("TSLA")
        sList.append(s6)
            
        s7 = Stock("JPM")
        sList.append(s7)
            
        s8 = Stock("C")
        sList.append(s8)
            
        s9 = Stock("MCD")
        sList.append(s9)
            
        s10 = Stock("PG")
        sList.append(s10)

        return sList

    def getList2():

        sList = []
            
        s1 = Stock("SNDL")
        sList.append(s1)
            
        s2 = Stock("NVDA")
        sList.append(s2)
            
        s3 = Stock("KLA")
        sList.append(s3)
            
        s4 = Stock("RAIN")
        sList.append(s4)
            
        s5 = Stock("SDA")
        sList.append(s5)
            
        s6 = Stock("ARVL")
        sList.append(s6)
            
        s7 = Stock("RGTI")
        sList.append(s7)
            
        s8 = Stock("BIOC")
        sList.append(s8)
            
        s9 = Stock("NCPL")
        sList.append(s9)
            
        s10 = Stock("RXT")
        sList.append(s10)

        return sList
