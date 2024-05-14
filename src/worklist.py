from queue import Queue
import sys

from lattice import *
from AI import *
from bb import *


class WorkList():
    '''
        initialize the worklist with the basic blocks list
    '''
    def __init__(self, BBList):
        self.worklist = Queue(maxsize = 0)
        for i in BBList:
            if i.name == "END": continue
            self.worklist.put(i)

    def enQueue(self, obj):
        if not isinstance(obj, BasicBlock):
            raise ValueError("Enqueue Basic Block only")
        if self.worklist.full():
            print("Worklist is full")
            raise ValueError("Worklist is full")
        self.worklist.put(obj)

    def deQueue(self):
        if self.worklist.empty():
            print("Worklist is empty")
            return None
        obj = self.worklist.get()
        return obj

    def isEmpty(self):
        return self.worklist.empty()

    def getSize(self):
        return self.worklist.qsize()


class AbstractInterpreter():
    def __init__(self, cfg):
        # super().__init__(irHandler)
        self.pc = 0
        self.controlFlowGraph = cfg
        self.workList = WorkList(self.controlFlowGraph.nodes())
        self.analysis = ForwardAnalysis()

    #just a dummy equallity check function
    def isDifferent(self, dA, dB):
        for i in dA.keys():
            if i not in dB.keys():
                return True
            if len(dA[i])!=len(dB[i]):
                return True
            for j in range(len(dA[i])):
                if dA[i][j].left != dB[i][j].left:
                    return True
                if dA[i][j].right != dB[i][j].right:
                    return True
        return False


    def isChanged(self, newOut, oldOut):
        '''
            return True if newOut is different than their older values(oldOut)
            before calling to the TransferFunction
        '''
        assert isinstance(newOut, list)
        assert isinstance(oldOut, list)
        if len(newOut) != len(oldOut):
            return True
        flag = False
        for i in range(len(newOut)):
            flag = (flag or self.isDifferent(newOut[i], oldOut[i]))

        return flag


    def worklistAlgorithm(self, cfg):
        '''
            This is the main worklist algorithm.
            Initializing the worklist with the basic block list
            It is an map from name of the BB to the in and out info of program states
        '''
        # print(type(cfg.nodes()))
        BBlist = cfg.nodes()
        bbIn = {}
        bbOut = {}

        '''
            initialise in/out of entry/exit point
        '''
        fr=0
        isdec={}

        for i in BBlist:
            t=False
            if fr==0:
                t=True
                fr=1
            print(fr,t,i)
            bbIn[i.name] = self.analysis.initialize(i,t)
            print(bbIn[i.name],"bbint")
            bbOut[i.name] = []
            isdec[i.name]=0
        cnt=0
        print(self.workList.getSize(),"size")
        bol=0
        iter=0

        while not self.workList.isEmpty():
            iter+=1
            currBB = self.workList.deQueue()
            print(0,currBB)
            oldOut = bbOut[currBB.name]
            # for tt in oldOut:
                # print("old1",tt)
                # print("old``",tt['a'])
                # for t in tt['a']: 
                    # print("old",t)
            # print(oldOut,101)
            predList = [p for p in cfg.predecessors(currBB)]
            # print(predList,0)
            # cumulate the out of the pred list
            inlist = []
            for pred in predList:
                print(pred,"a",currBB.name)
                label = cfg.get_edge_label(pred, currBB)
                if bbOut[pred.name]:
                    if label != 'False':
                        # See CFGBuilder function we have
                        # cfg.add_edge(node, thenBB, label='Cond_True', color='green')
                        # and 
                        # cfg.add_edge(node, thenBB, label='Cond_False', color='red')
                        inlist.append(bbOut[pred.name][0])
                    else:
                        assert len(bbOut[pred.name]) > 1
                        inlist.append(bbOut[pred.name][1])
                        print("done",bbOut[pred.name][1])
            print(inlist,"inslist")
            # calling meet operation over inlist
            if inlist:
                for x in inlist:
                    for y,z in x.items():
                        for k in z:
                            print("inllll",y,k)
                currInVal = self.analysis.meet(inlist)
                assert isinstance(currInVal, dict)
                #assign the returned value to the in of currBB
                bbIn[currBB.name] = currInVal

                for x in bbIn[currBB.name]['a']:
                    print("currinbb",currBB.name,x)
            
            #calling transfer function
            tf = self.analysis.transferFunctionInstance
            # print(bbIn[currBB.name], currBB)
            currBBOutVal = tf.transferFunction(bbIn[currBB.name], currBB,cnt)
            '''
                1) return value should be a list
                2) len(currBBOutVal) at most be 2
                3) if len(currBBOutVal) == 2, then
                        currBBOutVal[0] -> for true branch
                        currBBOutVal[1] -> for false branch
            '''
            assert isinstance(currBBOutVal, list)
            print(currBBOutVal,10)
            bbOut[currBB.name] = currBBOutVal
            cnt+=1

            for tt in currBBOutVal:
                print("new1",tt)
                # print("new``",tt['b'])
                # for t in tt['b']: 
                #     print("new",t)
                tmep=[]
                rej=[]
                emp=0
                for t in tt['a']:
                    
                    print("new a ",t)
                    for x in oldOut:
                        emp=1
                        for xy in x['a']:
                            print("old a",xy,abs(t.left-xy.left),t.right-xy.right)
                            emp=2
                            if abs(t.left-xy.left)==1 and t.right==xy.right:
                                print("case1",t)
                                isdec[currBB.name]+=1
                                if isdec[currBB.name]==100 and currBB.name=="Termination":
                                    print("rejected",t)
                                    rej.append(t)
                                    if t in tmep:
                                        tmep.remove(t)
                                    continue
                                print(currBB.name,"aappnd",isdec[currBB.name])
                                if isdec[currBB.name]<100 and t not in tmep and t not in rej:
                                    tmep.append(t)
                                    print(currBB.name,"appnd",t)
                            elif abs(t.right-xy.right)==1 and t.left==xy.left:
                                print("case2",t)
                                isdec[currBB.name]+=1
                                if isdec[currBB.name]<100 and t not in tmep and t not in rej:
                                    tmep.append(t)
                                    print(currBB.name,"appnd",t)
                                    
                            else:
                                print("case3",t)
                                # isdec[currBB.name]=0
                                if t not in tmep and t not in rej:
                                    tmep.append(t)
                                    print(currBB.name,"appnd",t)
                if emp==2 and currBB.name=="Termination":
                    print("here",isdec)
                    tt['a']=tmep
            print("isdeccc",isdec[currBB.name],currBB.name)
            if isdec[currBB.name]>=100:
                print("termini")
                print(bbOut[currBB.name])
                for t in bbOut[currBB.name]:
                    for x in t['a']:
                        print("termin",x)
                # temp=[]
                if currBB.name=="Termination":
                    print("points")
                    break

                    
            if self.isChanged(   bbOut[currBB.name], oldOut):
                # if currBB.type=="while":
                #     print("wheel",currBB.instrlist[0].arg1)
                #     fla=False
                #     if len(oldOut)==0:
                #         fla=True
                #     elif len(currBBOutVal[0]['b'])!=len(oldOut[0]['b']) or len(currBBOutVal[1]['b'])!=len(oldOut[1]['b']):
                #         fla=True
                #     else:
                #         for j in range(2):
                #             for i in range(len(currBBOutVal[j]['b'])):
                #                 if currBBOutVal[j]['b'][i].left!=oldOut[j]['b'][i].left or currBBOutVal[j]['b'][i].right!=oldOut[j]['b'][i].right:
                #                     fla=True
                #     if fla==False:
                #         print("whele done")
                #         continue
                nextBBList = cfg.successors(currBB)
                # print("succ",nextBBList)
                for ind,i in enumerate(nextBBList):
                #     if len(currBBOutVal)==0:
                #         continue
                #     if len(currBBOutVal[ind])==0:
                #         continue
                #     if len(currBBOutVal[ind]['b'])==0:
                #         continue
                    # if currBBOutVal[ind]['b']==oldOut[ind]['b']:
                        # continue
                    print("succ",i)
                    
                    # if i.name=="Termibation":
                        # if bol==1:
                            # continue
                        # else:
                            # bol=1
                            # print("doneww",i)
                            # self.workList.enQueue(i)
                    # else:
                        # bol=1
                        # print("doneww",i)
                    self.workList.enQueue(i)
            # if len(bbIn[currBB.name]['b'])!=0:
            #     print(bbIn[currBB.name]['b'][0],"curinn endd")
            # if len(bbOut[currBB.name][0]['b'])>0:
            #     print(bbOut[currBB.name][0]['b'][0],"currout endd")
            # if len(bbOut[currBB.name][0]['b'])==2:
            #     print(bbOut[currBB.name][0]['b'][1],"currout endd")
            # if len(bbOut[currBB.name])==2 and len(bbOut[currBB.name][1]['b'])>0:
            #     print(bbOut[currBB.name][1]['b'][0],"curout endd")

        print("Worklist empty",iter)
        return bbIn, bbOut