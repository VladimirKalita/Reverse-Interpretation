import sys
import json
from pathlib import Path

if (args_count := len(sys.argv)) > 2:
    print(f"One argument expected, got {args_count - 1}")
    raise SystemExit(2)
elif args_count < 2:
    print("You must specify the target directory")
    raise SystemExit(2)


f=open(sys.argv[1])
data = json.load(f)
ops={"Gt":">", "Lt":"<","Eq":"==","NotEq":"!=","GtE":">=","LtE":"<=","Add":"+" , "Sub":"-", "Mult":"*"}


mem={}

def val(value):
    if (value!=None):
        if(value["_type"]=="Constant"):
            return (value["value"])
        elif value["_type"]=="Name":
            return mem[value["id"]]
        elif value["_type"]=="BinOp":
            op=value["op"]["_type"]
            left=val(value["left"])
            right=val(value["right"])
            if op=="Add":
                return (left+right)
            elif op=="Sub":
                return (left-right)
            elif op=="Mult":
                return (left*right)
        elif value["_type"]=="Compare":
            lhs=val(value["left"])
            rhs=val(value["comparators"][0])
            opr=value["ops"][0]["_type"]
            if opr=="Gt":
                return lhs>rhs
            elif opr=="Lt":
                return lhs<rhs
            elif opr=="Eq":
                return lhs==rhs
            elif opr=="GtE":
                return lhs>=rhs
            elif opr=="LtE":
                return lhs<=rhs
            elif opr=="NotEq":
                return lhs!=rhs
            else:
                return True            
        #     return left + op+right
def interp(node):
    if node["_type"] == "Assign":
        target = node["targets"][0]["id"]
        value = val(node["value"])
        mem[target] = value

    elif node["_type"]=="If":
        opr=node["test"]["ops"][0]["_type"]
        cond=val(node["test"])
        if cond==True:
            for x in node["body"]:
                interp(x)
        else:
            for x in node["orelse"]:
                interp(x)

for l in data["body"]:
    interp(l)
print(mem)                      