import copy
import numpy as np
from MyLib1 import *

class WorkStack:
    def __init__(self):
        self.A=0
        self.B=0
        self.C=0
        self.D=0
        self.restVals=[]
        self.AN=0
        self.BN=0
        self.CN=0
        self.DN=0
        self.restNs=[]
        self.DIsVacant=True
    #
    #def ShiftToStack(self):
    #    self.restVals.append(self.A)
    #    self.restNs.append(self.AN)
    #    self.A=self.B
    #    self.AN=self.BN
    #    self.B=self.C
    #    self.BN=self.CN
    #    if not self.DIsVacant:
    #        self.C=self.D
    #        self.CN=self.DN
    #    #
    #    self.DIsVacant=True
    ##
    #def ShiftFromStack(self):
    #    self.D=self.C
    #    self.DN=self.CN
    #    self.C=self.B
    #    self.CN=self.BN
    #    self.B=self.A
    #    self.BN=self.AN
    #    LastStackNN=len(self.restVals)
    #    if LastStackNN>0:
    #        self.A=self.restVals[LastStackNN-1]
    #        self.AN=self.restNN[LastStackNN-1]
    #        del(self.restVals[LastStackNN-1])
    #        del(self.restNs[LastStackNN-1])
    #    #
    #
    def shiftFromCToStack(self):#was shiftFromBToStack
        self.restVals.append(self.A)
        self.restNs.append(self.AN)
        self.A=self.B
        self.AN=self.BN
        #
        self.B=self.C
        self.BN=self.CN
    #
    def shiftFromStackToB(self):
        self.B=self.A
        self.BN=self.AN
        LastStackNN=len(self.restVals)
        if LastStackNN>0:
            self.A=self.restVals[LastStackNN-1]
            self.AN=self.restNN[LastStackNN-1]
            del(self.restVals[LastStackNN-1])
            del(self.restNs[LastStackNN-1])
        #
    #
    def excludeB(self):
        self.B=self.C
        self.BN=self.CN
        #if not self.DIsVacant:
        #    self.C=self.D
        #    self.CN=self.DN
        #
    #
    def show(self):
        stackL=len(self.restVals)
        if stackL>0:
            print("rest")
            for i in range(stackL):
                print(str(i+1)+") "+str(self.restVals[i])+" (N"+str(self.restNs[i])+")")
            #
        #
        print("A="+str(self.A)+" (N"+str(self.AN)+")")
        print("B="+str(self.A)+" (N"+str(self.BN)+")")
        print("C="+str(self.A)+" (N"+str(self.CN)+")")
    #
            
#class WorkStack
#
class SingleCycle:
    def __init__(self):
        self.A=0
        self.B=0
        self.C=0
        self.detectionNN=0
    #
    def Range(self):
        return abs(self.A-self.B)
    #
    def Mean(self):
        return (self.A+self.B)/2
    #
    def GetMax(self):
        mn=0
        if self.A>self.B:
            mn=self.A
        else:
            mn=self.B
        #
    #
    def GetMin(self):
        mn=0
        if self.A<self.B:
            mn=self.A
        else:
            mn=self.B
        #
    #
#class SingleCycle    
#
                

iniData=[]
fullCycles=[]
#singleCycle=[]
with open("inidat.txt", "r") as file:
    line = file.readline()
    while line:
        print(line, end="")
        line = file.readline()
        if isNumber(line):
            num=float(line)
            iniData.append(num)
        #
    #
#
dataL=len(iniData)
countIniDataN=0
aStack=WorkStack()
#stk=[]
if dataL>4:
    for i in range(1, 3+1):
        x=iniData[i-1]
        #stk.append(x)
        if i==1:
            aStack.A=x
            aStack.AN=1
        elif i==2:
            aStack.B=x
            aStack.BN=2
        elif i==3:
            aStack.C=x
            aStack.CN=3
        #elif i==4:
        #    aStack.D=x
        #
    #
    print("\n")
    print("Initial stack is")
    aStack.show()
    countIniDataN=3
    while countIniDataN<dataL:
        #if countIniDataN==3:
        #    aStack.D=x
        #    countIniDataN=4
        #
        print("\n Current N="+str(countIniDataN))
        x=iniData[countIniDataN-1]
        dBC=aStack.B-aStack.C
        dAB=aStack.A-aStack.B
        if abs(dBC)>=abs(dAB):
            caseCycleNotUnCompleted=True
            Ampl=abs(dAB)
            med= (aStack.A + aStack.B)/2
            singleCycle=SingleCycle()
            singleCycle.A=aStack.A
            singleCycle.AN=aStack.AN
            singleCycle.B=aStack.B
            singleCycle.BN=aStack.BN
            singleCycle.C=aStack.C
            singleCycle.detectionNN=aStack.CN
            #
            fullCycles.append(singleCycle)
            #
            aStack.excludeB()
            #countIniDataN++
            #aStack.CN=countIniDataN
            #aStack.C=inidata[countIniDataN-1]
            #
            print("Cycle  full detected abs(dBC)>=abs(dAB): "+str(dBC)+">"+str(dAB)+" Ampl="+str(dAB)+"="+str(fullCycles[len(fullCycles)-1].Range())+" med val = "+str(med)+"="+str(fullCycles[len(fullCycles)-1].Mean())) 
        else:
            caseCycleNotUnCompleted=False
            aStack.shiftFromCToStack()
            #countIniDataN++
            #aStack.CN=countIniDataN
            #aStack.C=inidata[countIniDataN-1]
            print("It is not full cycle")
            
        #
        countIniDataN+=1
        aStack.CN=countIniDataN
        print("IniDaata cur N = "+str(countIniDataN)+" ciur ini data val = "+str(iniData[countIniDataN-1]))
        aStack.C=iniData[countIniDataN-1]
        print("Value "+str(aStack.C)+" N "+str(aStack.CN)+" is added from ini data to work stack")
        #
        print("Now stack is")
        aStack.show()
    #while
#if work
        
        
        
      
        

