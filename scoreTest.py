
current = 225.12
#ppd = [0.18, 0.24, 0.3, 0.27, 0, 0, 0, 0]
ppd = [0.68, 0.98, 1.41, 2.16, 3, 5.25, 0, 0]
ppd = [1.19, 1.73, 2.52, 4.06, 6, 14.63, 33.48, 0]
strikes = [280, 260, 245, 230, 220, 200, 180, 140]
for i in range(0, 8):

    projection = 150
    rawRisk = 1 - ((current - strikes[i]) / current)
    riskScore = 1 - 5 * ((current - strikes[i]) / current) - 3 * (( projection - strikes[i]) / projection)
    print("--------------------| STRIKE " + str(strikes[i]) + " |--------------------")
    print("rawRisk = " + str(rawRisk))
    print("riskScore = " + str(riskScore))

    score = ppd[i] * riskScore

    print("score = " + str(score))
    print("")
    
