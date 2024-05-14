import sys
import json
import random
file_path = sys.argv[1]


# with open(file_path) as f:
#     data = json.load(f)

temp=1

class tac:
    def __init__(self):
        self.isint1=False
        self.isint2=False
        self.arg1=None
        self.arg2=None
        self.op=None
        self.tar=None
    def __init__(self,tar,a1,is1):
        self.tar=tar
        self.arg1=a1
        self.isint1=is1
    def __init__(self,tar,a1,a2,op,is1,is2):
        self.tar=tar
        self.arg1=a1
        self.isint1=is1
        self.isint2=is2
        self.arg2=a2
        self.op=op
        self.type=None
    
        
    def print_3ac(self):
        c1=False
        c2=False
        if isinstance(self.arg1,tac):
            self.arg1.print_3ac()
            c1=True
        if isinstance(self.arg2,tac):
            self.arg2.print_3ac()
            c2=True
        
        if c1:
            if c2:
                print(f'{self.tar}={self.arg1.tar}{self.op}{self.arg2.tar}')
            else:
                print(f'{self.tar}={self.arg1.tar}{self.op}{self.arg2}')
        else:
            if c2:
                print(f'{self.tar}={self.arg1}{self.op}{self.arg2.tar}')
            else:
                print(f'{self.tar}={self.arg1}{self.op}{self.arg2.tar}')


ir=[]

def val(value):
    if value is not None:
        if value["_type"] == "Constant":
            return str(value["value"])
        elif value["_type"] == "Name":
            return value["id"]
        elif value["_type"] == "BinOp":
            op = value["op"]["_type"]
            left = val(value["left"])
            right = val(value["right"])
            return f'({left}{op}{right})'
        elif value["_type"] == "Compare":
            left = val(value["left"])
            right = val(value["comparators"][0])
            op = value["ops"][0]["_type"]
            return f'{left}{op}{right}'
        
temp_var="var"

def find_tac(node,tar=None,is_tac=None):
    if node["_type"] == "Assign":
        tar=node["targets"][0]["id"]
        rhs=node["value"]
        a1=None
        a2=None
        op=None
        i1=False
        i2=False
        if rhs["_type"] == "Constant":
            a1=rhs["value"]
            i1=True
        elif rhs["_type"] == "Name":
            a1=rhs["id"]
        elif rhs["_type"] == "BinOp":
            op=rhs["op"]["_type"]
            global temp
            a1=find_tac(rhs["left"],f'tem_var{temp}')
            if isinstance(a1,int):
                i1=True
            a2=find_tac(rhs["right"])
            if isinstance(a2,int):
                i2=True
        elif rhs["_type"]=="Call":
            rl=rhs["args"][0]["value"]
            a1=random.randint(0,rl)
        tac1=tac(tar,a1,a2,op,i1,i2)
        return tac1
    elif node["_type"] == "BinOp":
        temp+=1
        i1=False
        i2=False
        op=node["op"]["_type"]
        a1=find_tac(node["left"],f'temp_var{temp}')
        if isinstance(a1,int):
            i1=True
        a2=find_tac(node["right"],f'temp_var{temp}')
        if isinstance(a2,int):
            i2=True
        return tac(tar,a1,a2,op,i1,i2)
    elif node["_type"] == "If":
        return find_tac(node["test"],"cond")
    elif node["_type"] == "Compare":
        op=node["ops"][0]["_type"]
        a1=find_tac(node["left"])
        a2=find_tac(node["comparators"][0])
        i1=False
        i2=False
        if isinstance(a1,int):
            i1=True
        if isinstance(a2,int):
            print(a2)
            i2=True
        return tac(tar,a1,a2,op,i1,i2)
    elif node["_type"] == "Constant":
        if(is_tac==True):
            # a1=None
            a2=None
            op=None
            i1=False
            i2=False
            tar=None
            a1=node["value"]
            # op=None

            return tac(tar,a1,a2,op,i1,i2)
        return node["value"] 
    elif node["_type"] == "Name":
        if(is_tac==True):
            a2=None
            op=None
            i1=False
            i2=False
            tar=None
            a1=node["id"]
            # op=None

            return tac(tar,a1,a2,op,i1,i2)
        return node["id"]

# for l in data["body"]:
#     temp=1
#     find_tac(l)