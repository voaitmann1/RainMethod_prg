import copy
import numpy as np
from MyLib1 import *

class WorkStack:
    def __init__(self):
        self.data=[]
        self.dataNs=[]
    #
    def getC(self):
        Q=self.getL()
        return self.data[Q-0-1]
    #
    def getCN(self):
        Q=self.getL()
        return self.dataNs[Q-0-1]
    #
    def getB(self):
        Q=self.getL()
        return self.data[Q-1-1]
    #
    def getBN(self):
        Q=self.getL()
        return self.dataNs[Q-1-1]
    #
    def getA(self):
        Q=self.getL()
        return self.data[Q-2-1]
    #
    def getAN(self):
        Q=self.getL()
        return self.dataNs[Q-2-1]
    #
    #def ShiftToStackExcludingB(self):#B=С
    #    self.data[Q-1-1]=copy.deepcopy(self.data[Q-0-1])
    #   self.dataNs[Q-1-1]=copy.deepcopy(self.dataNs[Q-0-1])
    ##
    def excludeB(self):
        Q=self.getL()
        if Q>2:
            del self.data[Q-1-1]
            del self.dataNs[Q-1-1]
        #
    #
    def setC(self, C, CN):
        Q=self.getL()
        if Q>3:
            self.data[Q-1]=C
            self.dataNs[Q-1]=CN
        #
    #
    def setB(self, B, BN):
        Q=self.getL()
        if Q>3:
            self.data[Q-1-1]=B
            self.dataNs[Q-1-1]=BN
        #
    #
    def setA(self, A, AN):
        Q=self.getL()
        if Q>3:
            self.data[Q-2-1]=A
            self.dataNs[Q-2-1]=AN
        #
    #
    def add(self, val, valN):
        self.data.append(val)
        self.dataNs.append(valN)
    #
    def getL(self):
        return len(self.data)
    #
    def cutLast(self):
        L=self.getL()
        del self.data[L-1]
        del self.dataNs[L-1]
    #
    def show(self):
        stackL=len(self.data)
        if stackL>0:
            for i in range(1,stackL-3+1):
                print("val (in stack N "+str(i)+") = "+str(self.data[i-1])+"(in ini data N "+str(self.dataNs[i-1])+")")
            #
            if stackL>=3:
                i=stackL-2
                print("A= (in stack N "+str(i)+")= "+str(self.data[i-1])+"(in ini data N "+str(self.dataNs[i-1])+")")
                i=stackL-1
                print("B= (in stack N "+str(i)+")= "+str(self.data[i-1])+"(in ini data N "+str(self.dataNs[i-1])+")")
                i=stackL-0
                print("C= (in stack N "+str(i)+")= "+str(self.data[i-1])+"(in ini data N "+str(self.dataNs[i-1])+")")
            #
        #
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
        if self.GetA()<self.B:
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
print("reading data")
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
    for countIniDataN in range(1, 3+1):
        x=iniData[countIniDataN-1]
        aStack.add(x, countIniDataN)
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
        dBC=aStack.getB()-aStack.getC()
        dAB=aStack.getA()-aStack.getB()
        if abs(dBC)>=abs(dAB):
            caseCycleNotUnCompleted=True
            Ampl=abs(dAB)
            med= (aStack.getA() + aStack.getB())/2
            singleCycle=SingleCycle()
            singleCycle.A=aStack.getA()
            singleCycle.AN=aStack.getAN()
            singleCycle.B=aStack.getB()
            singleCycle.BN=aStack.getBN()
            singleCycle.C=aStack.getC()
            singleCycle.detectionNN=aStack.getCN()
            #
            fullCycles.append(singleCycle)
            #
            aStack.excludeB()
            #
            if aStack.getL()<=2:
                countIniDataN+=1
                x=iniData[countIniDataN-1]
                aStack.add(x, countIniDataN)
            #else NOp
            print("Cycle  full detected abs(dBC)>=abs(dAB): "+str(dBC)+">"+str(dAB)+" Ampl="+str(dAB)+"="+str(fullCycles[len(fullCycles)-1].Range())+" med val = "+str(med)+"="+str(fullCycles[len(fullCycles)-1].Mean())) 
        else:
            caseCycleNotUnCompleted=False
            #aStack.shiftFromCToStack()
            #countIniDataN++
            #aStack.CN=countIniDataN
            #aStack.C=inidata[countIniDataN-1]
            print("It is not full cycle")
            countIniDataN+=1
            x=iniData[countIniDataN-1]
            aStack.add(x, countIniDataN)
        #
        #countIniDataN+=1
        #aStack.CN=countIniDataN
        #print("IniDaata cur N = "+str(countIniDataN)+" ciur ini data val = "+str(iniData[countIniDataN-1]))
        #aStack.C=iniData[countIniDataN-1]
        #print("Value "+str(aStack.C)+" N "+str(aStack.CN)+" is added from ini data to work stack")
        #
        print("Now stack is")
        aStack.show()
    #while
#if work
        
        
        
      
        

