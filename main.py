import subprocess
import os
import scipy
from scipy import stats
import numpy as np
import random

TempStart = 10000.0

data = open("data", "r+")

rawdata = data.readlines()
rawdata = map(lambda x: x.split(), rawdata)
rawdata = filter(lambda x: len(x) == 4, rawdata)
rawdata = np.array(rawdata)

numDPoints = len(rawdata)

ICList = []
ISCList = []
i = 0
while i < len(rawdata):
    if random.randint(0,1) == 0:
        ICList += [rawdata[i-1]]
    else:
        ISCList += [rawdata[i-1]]
    i += 1

ICList = np.array(ICList)
ISCList = np.array(ISCList)

ICDeltaG = np.array(ICList[:,2], float)
ICNRRates = np.array(ICList[:,1], float)
ISCDeltaG = np.array(ISCList[:,3], float)
ISCNRRates = np.array(ISCList[:,1], float)
ICslope, ICintercept, ICr_value, ICp_value, ICsted_err = stats.linregress(ICDeltaG,ICNRRates)
ISCslope, ISCintercept, ISCr_value, ISCp_value, ISCsted_err = stats.linregress(ICDeltaG,ICNRRates)
FracISC = len(ISCList)/(len(ICList)+len(ISCList))
Objective = ICr_value**2 * (1 - FracISC) + ISCr_value**2 * FracISC
BestPart = [ICList, ISCList, Objective]
CurrentPart = [ICList, ISCList, Objective]
Temp = TempStart

for i in range(1, 500000):
    Indexswitch = random.randint(0, numDPoints)
    #print len(CurrentPart[0])

    if Indexswitch < len(CurrentPart[0]):
        TestISCList = np.append(CurrentPart[1], [CurrentPart[0][Indexswitch]], axis = 0)
        TestICList = np.delete(CurrentPart[0], Indexswitch, axis = 0)
    else:
        TestICList = np.append(CurrentPart[0], [CurrentPart[1][Indexswitch-len(CurrentPart[0])-1]], axis = 0)
        TestISCList = np.delete(CurrentPart[1], Indexswitch-len(CurrentPart[0])-1, axis = 0)
    TestICDeltaG = np.array(TestICList[:,2], float)
    TestICNRRates = np.array(TestICList[:,1], float)
    TestISCDeltaG = np.array(TestISCList[:,3], float)
    TestISCNRRates = np.array(TestISCList[:,1], float)

    ICslope, ICintercept, ICr_value, ICp_value, ICsted_err = stats.linregress(TestICDeltaG,TestICNRRates)
    ISCslope, ISCintercept, ISCr_value, ISCp_value, ISCsted_err = stats.linregress(TestISCDeltaG,TestISCNRRates)

    FracISC = 1.0*len(TestISCList)/(len(TestICList)+len(TestISCList))
    Objective = ICr_value**2 * (1 - FracISC) + ISCr_value**2 * FracISC
    #print "Test evaluates as: " + str(Objective)
    #print "Best partition has a value of: " + str(BestPart[2])

    if Objective > BestPart[2]:
        BestPart = [TestICList, TestISCList, Objective]

    if Objective > CurrentPart[2]:
        CurrentPart = [TestICList, TestISCList, Objective]
    elif random.random() < np.exp((Objective-CurrentPart[2])/Temp):
        CurrentPart = [TestICList, TestISCList, Objective]
#    Temp = TempStart*np.exp(-i/2)
    Temp = (TempStart)/(i)

print BestPart
output = open("Best.out", "w")
output.write(str(BestPart))









