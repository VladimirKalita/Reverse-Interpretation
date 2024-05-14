import copy
import math
import sys
from typing import overload

from lattice import *
from tac import *
PINF="+inf"
NINF="-inf"
'''
    Class for interval domain
'''
class IntervalDomain(Lattice):
    
    '''Initialize abstract value'''
    def __init__(self, data):
        self.left=data[0]
        self.right=data[1]
        self.isdim=0
    
    # def __init__(self,l,r):
    #     self.left=l    
    #     self.right=r
    '''To display abstract values'''
    def __str__(self):
        return (f"[{self.left},{self.right}]")

    '''To check whether abstract value is bot or not'''
    def isBot(self):
        pass

    '''To check whether abstract value is Top or not'''
    def isTop(self):
        pass

    '''Implement the meet operator'''
    def meet(self, other):
        pass

    '''Implement the join operator'''
    def join(self, other):
        pass

    '''partial order with the other abstract value'''
    def __le__(self, other):
        pass

    '''equality check with other abstract value'''
    def __eq__(self, other):
        pass

    '''
        Add here required abstract transformers
    '''
    pass

class IntervalTransferFunction(TransferFunction):
    def __init__(self):
        pass

    def transferFunction(self, currBBIN, currBB,i):
        '''
            Transfer function for basic block 'currBB'
            args: In val for currBB, currBB
            Returns newly calculated values in a form of list

            This is the transfer function you write for Abstract Interpretation.
        '''
        #implement your transfer function here
        # print(currBBIN['a'],type(currBBIN))
        ret=currBBIN.copy()
        ret1=None
        instrlist=currBB.instrlist
        for inst in instrlist:
            # if inst.tar==None:
            if isinstance(inst,tac):
                a1=inst.arg1
                b1=inst.arg2
                print(a1,"aa",b1,type(a1),type(b1))
                # inst.print_3ac()
                print("isint1:",a1,inst.isint1)
                print("isint2:",b1,inst.isint2)
                if isinstance(a1,int)==False and inst.arg1!="NT":
                    a1=ret[inst.arg1]
                if isinstance(b1,int)==False and inst.op!=None:
                    b1=ret[inst.arg2]
                # print(a1,type(a1))
                # print(b1,type(b1))
                print(inst.tar)
                if inst.tar==None:
                    print("hekk")
                    if inst.type=="assume":
                        temp=ret.copy()
                        tmp=[]
                        if inst.op=="Gt":
                            if isinstance(inst.arg2,int):
                                for ids in temp[inst.arg1]:
                                    if ids.right<=inst.arg2:
                                        continue
                                    if ids.left<=inst.arg2:
                                        tmp.append(IntervalDomain([inst.arg2+1,ids.right]))
                                    else:
                                        tmp.append(ids)
                        elif inst.op=="GtE":
                            if isinstance(inst.arg2,int):
                                for ids in temp[inst.arg1]:
                                    if ids.right<inst.arg2:
                                        continue
                                    if ids.left<inst.arg2:
                                        tmp.append(IntervalDomain([inst.arg2,ids.right]))
                                    else:
                                        tmp.append(ids)
                        elif inst.op=="Lt":
                            if isinstance(inst.arg2,int):
                                for ids in temp[inst.arg1]:
                                    if ids.left>=inst.arg2:
                                        continue
                                    if ids.right>=inst.arg2:
                                        tmp.append(IntervalDomain([ids.left,inst.arg2-1]))
                                    else:
                                        tmp.append(ids)
                        elif inst.op=="LtE":
                            if isinstance(inst.arg2,int):
                                for ids in temp[inst.arg1]:
                                    if ids.left>inst.arg2:
                                        continue
                                    if ids.right>inst.arg2:
                                        tmp.append(IntervalDomain([ids.left,inst.arg2]))
                                    else:
                                        tmp.append(ids)
                            
                        ret[inst.arg1]=tmp
                    elif inst.op == "Eq":
                        ret1=ret.copy()
                        ret[inst.arg1]=[IntervalDomain([b1,b1])]
                        ret1[inst.arg1]=[IntervalDomain([ret1[inst.arg1].left,b1-1]),IntervalDomain(b1+1,[ret1[inst.arg1].right])]
                    elif inst.op == "Gt":
                        ret1=ret.copy()
                        if (isinstance(a1,int) and isinstance(b1,int)):
                            if(a1>b1):
                                for a,b in ret.items():
                                    ret1[a]=[]
                            else:
                                for a,b in ret.items():
                                    ret[a]=[]
                        # elif !isinstance(a1,int) and !isinstance(b1,int):
                        #     temp=[]
                        #     for ids in ret[inst.arg1]:
                        #         for bd in ret[inst.arg2]:
                        #             if ids.right<=bd.left:
                        #                 continue
                        #             if ids.left>bd.right:
                        #                 temp.append(ids)
                        #             else:
                        #                 temp.append(ids)
                        else:
                            temp=[]
                            for ids in ret[inst.arg1]:
                                print(ids,b1,ret)
                                if ids.right==NINF or ids.right<=b1 :
                                    continue
                                if ids.left==PINF or  ids.left>b1 :
                                    temp.append(ids)
                                else :
                                    # print('dd')
                                    temp.append(IntervalDomain([b1+1,ids.right]))
                            # print("PP",temp)
                            ret[inst.arg1]=temp
                            # print(ret)
                            temp1=[]
                            # print(ret1)
                            for ids in ret1[inst.arg1]:
                                if ids.left==PINF or ids.left>=b1 :
                                    continue
                                if ids.right==NINF or  ids.right<b1 :
                                    temp1.append(ids)
                                else :
                                    # print('dd')
                                    temp1.append(IntervalDomain([ids.left,b1]))
                            # print(" dds",temp1)
                            ret1[inst.arg1]=temp1
                    elif inst.op == "Lt":
                        ret1=ret.copy()
                        if (isinstance(a1,int) and isinstance(b1,int)):
                            if(a1<b1):
                                for a,b in ret.items():
                                    ret1[a]=[]
                            else:
                                for a,b in ret.items():
                                    ret[a]=[]
                        else:
                            temp=[]
                            for ids in ret[inst.arg1]:
                                print(ids,b1,ret)
                                if ids.left==PINF or ids.left>=b1 :
                                    continue
                                if ids.right==NINF or  ids.right<b1 :
                                    temp.append(ids)
                                else :
                                    # print('dd')
                                    temp.append(IntervalDomain([ids.left,b1-1]))
                            # print("PP",temp)
                            ret[inst.arg1]=temp
                            # print(ret)
                            temp1=[]
                            # print(ret1)
                            for ids in ret1[inst.arg1]:
                                if ids.right==NINF or ids.right<b1 :
                                    continue
                                if ids.left==PINF or ids.left>=b1 :
                                    temp1.append(ids)
                                else :
                                    temp1.append(IntervalDomain([b1,ids.right]))
                            # print(" dds",temp1)
                            ret1[inst.arg1]=temp1
                            # print(ret[inst.arg1],"  dd",ret1)
                    elif inst.op == "LtE":
                        ret1=ret.copy()
                        if (isinstance(a1,int) and isinstance(b1,int)):
                            if(a1<=b1):
                                for a,b in ret.items():
                                    ret1[a]=[]
                            else:
                                for a,b in ret.items():
                                    ret[a]=[]
                        elif isinstance(b1,int):
                            temp=[]
                            for ids in ret[inst.arg1]:
                                print(ids,b1,ret)
                                if ids.left==PINF or ids.left>b1 :
                                    continue
                                if ids.right==NINF or  ids.right<=b1 :
                                    temp.append(ids)
                                else :
                                    # print('dd')
                                    temp.append(IntervalDomain([ids.left,b1]))
                            # print("PP",temp)
                            ret[inst.arg1]=temp
                            # print(ret)
                            temp1=[]
                            # print(ret1)
                            for ids in ret1[inst.arg1]:
                                if ids.right==NINF or ids.right<=b1 :
                                    continue
                                if ids.left==PINF or ids.left>b1 :
                                    temp1.append(ids)
                                else :
                                    temp1.append(IntervalDomain([b1+1,ids.right]))
                            # print(" dds",temp1)
                            ret1[inst.arg1]=temp1
                        
                        else:
                            temp=[]
                            for ids in ret[inst.arg1]:
                                for id in ret[inst.arg2]:
                                    print(ids,b1,ret)
                                    if ids.left==PINF or ids.left>id.right :
                                        continue
                                    if ids.right==NINF or  ids.right<=id.left :
                                        temp.append(ids)
                                    else :
                                        # print('dd')
                                        temp.append(IntervalDomain([ids.left,id.left]))
                            # print("PP",temp)
                            ret[inst.arg1]=temp
                            # print(ret)
                            temp1=[]
                            # print(ret1)
                            for ids in ret1[inst.arg1]:
                                if ids.right==NINF or ids.right<=id.left:
                                    continue
                                if ids.left==PINF or ids.left>id.left :
                                    temp1.append(ids)
                                else :
                                    temp1.append(IntervalDomain([id.left+1,ids.right]))
                            # print(" dds",temp1)
                            ret1[inst.arg1]=temp1
                            # print(ret[inst.arg1],"  dd",ret1)
                    elif inst.op == None:
                        print("True or flase",inst.arg1)
                        if inst.arg1=="NT":
                            ret1=ret.copy()
                        elif(inst.arg1):
                            print("true11")
                            ret1=ret.copy()
                            for a,b in ret.items():
                                ret1[a]=[]
                        else:
                            print("False11")
                            ret1=ret.copy()
                            for a,b in ret.items():
                                ret[a]=[]

                elif inst.op=="Add":
                    print("adddding",a1,type(a1),b1,type(b1))
                    temp1=[]
                    if isinstance(b1,int):
                        for ids in a1:
                            temp1.append(IntervalDomain([ids.left+b1,ids.right+b1]))
                    else:
                        for ids in a1:
                            for id in b1:
                                intdom=IntervalDomain([ids.left+id.left,ids.right+id.right])
                                if intdom not in temp1:
                                    temp1.append(intdom)
                    print(a1,type(a1),b1,type(b1)) 
                    ret[inst.tar]=temp1
                    for x in temp1:
                        print("valll",x)
                elif inst.op=="Sub":
                    print(a1,type(a1),b1,type(b1))
                    temp=[]
                    if isinstance(b1,int):
                        for ids in a1:
                            temp.append(IntervalDomain([ids.left-b1,ids.right-b1]))
                    print(a1,type(temp),b1,type(b1))

                    ret[inst.tar]=temp
                    for x in temp:
                        print("vlll",x)
                elif inst.op==None:
                    if isinstance(a1,int):
                        temp=[]
                        temp.append(IntervalDomain([a1,a1]))
                        ret[inst.tar]=temp
                    else:
                        ret[inst.tar]=a1.copy()   
                # elif inst.op == "Eq":
                #     ret[f"cond{i}"]=(a1==b1)
                # elif inst.op == "Gt":
                #     ret[f"cond{i}"]=(a1>b1)
                # elif inst.op == "Lt":
                #     ret[f'cond{i}']=(a1<b1)
        
        outVal = []
        outVal.append(ret)
        print(ret1,"helllo")
        if ret1!=None:
            print(ret1,"helllo")
            outVal.append(ret1)
        return outVal

class ForwardAnalysis():
    def __init__(self):
        self.transferFunctionInstance = IntervalTransferFunction()
        self.type = "IntervalTF"

    '''
        This function is to initialize in of the basic block currBB
        Returns a dictinary {varName -> abstractValues}
        isStartNode is a flag for stating whether currBB is start basic block or not
    '''
    def initialize(self, currBB, isStartNode):
        val = {}
        #Your additional initialisation code if any
        if isStartNode:
            val['a']=[IntervalDomain([0,1000])]
            val['i']=[IntervalDomain([-1000,1000])]
            val['j']=[IntervalDomain([-1000,1000])]
            val['k']=[IntervalDomain([0,1000])]
        return val

    #just a dummy equallity check function for dictionary
    def isEqual(self, dA, dB):
        for i in dA.keys():
            if i not in dB.keys():
                return False
            if dA[i] != dB[i]:
                return False
        return True

    '''
        Define the meet operation
        Returns a dictinary {varName -> abstractValues}
    '''
    def meet(self, predList):
        assert isinstance(predList, list)
        meetVal = {}
        if len(predList)==1:
            return predList[0].copy()
        # minl=10000
        # maxr=-1000
        meetVal=predList[0].copy()
        minl={}
        maxr={}
        for i in range(len(predList[0])):
            minl[i]=10000
            maxr[i]=-10000
        temp=[]
        for pred in predList:
            
            for i,(x,y) in enumerate(pred.items()):
                print("mmmmeet",i,x,y)
                if x=='b':
                    for id in y:
                        minl[i]=min(minl[i],id.left)
                        maxr[i]=max(maxr[i],id.right)
                    print("meettt",minl[i],maxr[i])
                    meetVal[x]=[IntervalDomain([minl[i],maxr[i]])]
                    for dd in meetVal[x]:
                        print("after meet",i,x,dd)    
                elif x=='a':
                    if temp==[]:
                        temp=y.copy()
                    else:
                        print("non-empty")
                        tmp=[]
                        temp.sort(key=lambda x:x.left)
                        y.sort(key=lambda x:x.left)
                        
                        i1,i2=0,0
                        len1,len2=len(temp),len(y)

                        while(i1<len1 and i2<len2):
                            ind1,ind2=temp[i1],y[i2]
                            print("nonemo",ind1," kk",ind2)
                            if ind1.right>=ind2.left and ind2.right>=ind1.left:
                                print("nonemo1",ind1," kk",ind2)
                                intdom=IntervalDomain([max(ind1.left,ind2.left),min(ind1.right,ind2.right)])
                                if intdom not in tmp:
                                    tmp.append(intdom)
                                
                                if ind1.right < ind2.right:
                                    i1+=1
                                    # ind2.left=ind1.right+1
                                else:
                                    i2+=1
                                    # ind1.right=ind2.right+1
                            else:
                                if ind1.left<ind2.left:
                                    print("nonemo2",ind1," kk",ind2)
                                    if ind1 not in tmp:
                                        tmp.append(ind1)
                                    i1+=1
                                else:
                                    print("nonemo3",ind1," kk",ind2)
                                    if ind2 not in tmp:
                                        tmp.append(ind2)
                                    i2+=1
                        tmp.sort(key=lambda x:x.left)
                        tmpe=tmp.copy()
                        for i3 in range(i1,len(temp),1):
                            inddom=temp[i3]
                            flagg=0
                            for tm in tmp:
                                if tm.right<inddom.left or tm.left>inddom.right:
                                    continue
                                # elif tm.left>=inddom.right and tm.right<=inddom.left:
                                    # flagg=1
                                else:
                                    flagg=1
                            if flagg==0:
                                tmpe.append(inddom)
                    
                        for i3 in range(i2,len(y),1):
                            inddom=y[i3]
                            flagg=0
                            for tm in tmp:
                                if tm.right<inddom.left or tm.left>inddom.right:
                                    continue
                                # elif tm.left>=inddom.right and tm.right<=inddom.left:
                                    # flagg=1
                                else:
                                    flagg=1
                            if flagg==0:
                                tmpe.append(inddom)
                        tmp=tmpe

                                    
                        # tmp.extend(temp[i1:])
                        # tmp.extend(y[i2:])
                        # for ids in temp:
                        #     print("nonemp",ids)
                        #     for id in y:
                        #         print("noemp",id)
                        #         if abs(id.left-ids.left)<=1:
                        #             print("noemp1",ids)
                        #             lf=max(id.left,ids.left)
                        #             # if abs(ids.right-id.right)<=1:
                        #             rf=min(id.right,ids.right)
                        #             if lf<=rf:
                        #                 intdom=(IntervalDomain([lf,rf]))
                        #                 if intdom not in tmp:
                        #                     tmp.append(intdom)
                        #         elif abs(ids.right-id.right)<=1:
                        #             print("noemp2",ids)
                        #             rf=min(id.right,ids.right)
                        #             lf=max(id.left,ids.left)
                        #             if lf<=rf:
                        #                 intdom=(IntervalDomain([lf,rf]))
                        #                 if intdom not in tmp:
                        #                     tmp.append(intdom)
                        #         elif ids.left<id.left:
                        #             print("noemp3",ids)
                        #             if ids.right>id.right:
                        #                 if id not in tmp:
                        #                     tmp.append(id)
                        #             elif ids.right>=id.left:
                        #                 intdom=(IntervalDomain([id.left,ids.right]))
                        #                 if intdom not in tmp:
                        #                     tmp.append(intdom)
                        #             else:
                        #                 if ids not in tmp:
                        #                     tmp.append(ids)
                        #                 # if id not in tmp:
                        #                     # tmp.append(id)
                        #         elif id.left<ids.left:
                        #             if id.right>ids.right:
                        #                 if ids not in tmp:
                        #                     tmp.append(ids)
                        #             elif id.right>=ids.left:
                        #                 intdom=(IntervalDomain([ids.left,id.right]))
                        #                 if intdom not in tmp:
                        #                     tmp.append(intdom)
                        #             else:
                        #                 # if id not in tmp:
                        #                     # tmp.append(id)
                        #                 if ids not in tmp:
                        #                     tmp.append(ids)
                            # if ids not in tmp and len(y)==0:
                            #     tmp.append(ids)
                        temp=tmp.copy()
                    meetVal[x]=temp
                    for ii in temp:
                        print("mmeett3",i,x,ii)
                # if x in meetVal.keys():
                    # lf=min()
                #     # pass
                #     meetVal[x].extend(y.copy())
                #     sortedl=sorted(meetVal[x].copy(), key=lambda x:(x.left,x.right))
                #     for k in sortedl:
                #         print("kkkkkkk",k)
                #     srt=[]
                #     for k in meetVal[x]:
                #         print("kkkkkk==ppp=k",k) 
                    
                #     for j in range(0,len(sortedl),2):
                #         print(j,"llllll")
                #         if j+1<len(sortedl):
                #             if sortedl[j].left==sortedl[j+1].left:
                #                 continue
                #             # elif sortedl[j].
                #             else:
                #                 srt.append(sortedl[j])
                #         else:
                #             srt.append(sortedl[j])
                #     if len(sortedl)%2==0:
                #         srt.append(sortedl[-1])
                #     meetVal[x]=srt
                #     for k in meetVal[x]:
                #         print("kkkkkk===k",k) 
                    
                #     # meetVal[a]=max(meetVal[a],b)
                # else:
        
                #     meetVal[x]=y.copy()
                
        return meetVal

class BackwardAnalysis():
    def __init__(self):
        self.transferFunctionInstance = IntervalTransferFunction()
        self.type = "IntervalTF"

    '''
        This function is to initialize in of the basic block currBB
        Returns a dictinary {varName -> abstractValues}
        isStartNode is a flag for stating whether currBB is start basic block or not
    '''

    def initialize(self, currBB, isStartNode):
        val = {}
        #Your additional initialisation code if any
        if currBB.name=="Termibation":
            val['a']=[IntervalDomain([0,100])]
        return val

    #just a dummy equality check function for dictionary
    def isEqual(self, dA, dB):
        for i in dA.keys():
            if i not in dB.keys():
                return False
            if dA[i] != dB[i]:
                return False
        return True

    '''
        Define the meet operation
        Returns a dictinary {varName -> abstractValues}
    '''
    def meet(self, predList):
        assert isinstance(predList, list)
        meetVal = {}
        if len(predList)==1:
            return predList[0].copy()
        minl=10000
        maxr=-1000
        for pred in predList:
            
            for i,(x,y) in enumerate(pred.items()):
                
                for id in y:
                    minl=min(minl,id.left)
                    maxr=max(maxr,id.right)
                # if x in meetVal.keys():
                    # lf=min()
                #     # pass
                #     meetVal[x].extend(y.copy())
                #     sortedl=sorted(meetVal[x].copy(), key=lambda x:(x.left,x.right))
                #     for k in sortedl:
                #         print("kkkkkkk",k)
                #     srt=[]
                #     for k in meetVal[x]:
                #         print("kkkkkk==ppp=k",k) 
                    
                #     for j in range(0,len(sortedl),2):
                #         print(j,"llllll")
                #         if j+1<len(sortedl):
                #             if sortedl[j].left==sortedl[j+1].left:
                #                 continue
                #             # elif sortedl[j].
                #             else:
                #                 srt.append(sortedl[j])
                #         else:
                #             srt.append(sortedl[j])
                #     if len(sortedl)%2==0:
                #         srt.append(sortedl[-1])
                #     meetVal[x]=srt
                #     for k in meetVal[x]:
                #         print("kkkkkk===k",k) 
                    
                #     # meetVal[a]=max(meetVal[a],b)
                # else:
        
                #     meetVal[x]=y.copy()
                meetVal[x]=[IntervalDomain([minl,maxr])]
        
        return meetVal
# def analyzeUsingAI(irHandler):
#     '''
#         get the cfg outof IR
#         each basic block consists of single statement
#     '''
#     # call worklist and get the in/out values of each basic block
#     abstractInterpreter = AI.AbstractInterpreter(irHandler)
#     bbIn, bbOut = abstractInterpreter.worklistAlgorithm(irHandler.cfg)

#     #implement your analysis according to the questions on each basic blocks
#     pass