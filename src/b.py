import sys
import json
from pathlib import Path

assign=[]
branch=[]
loop=[]
blocks={}
if (args_count := len(sys.argv)) > 2:
    print(f"One argument expected, got {args_count - 1}")
    raise SystemExit(2)
elif args_count < 2:
    print("You must specify the target directory")
    raise SystemExit(2)


f=open(sys.argv[1])
data = json.load(f)

ops={"Gt":">", "Lt":"<","Eq":"==","NotEq":"!=","GtE":">=","LtE":"<=","Add":"+" , "Sub":"-", "Mult":"*"}

def val(value):
    if (value!=None):
        if(value["_type"]=="Constant"):
            return str(value["value"])
        elif value["_type"]=="Name":
            return value["id"]
        elif value["_type"]=="BinOp":
            op=ops[value["op"]["_type"]]
            left=val(value["left"])
            right=val(value["right"])
            return '('+left+op+right+')'
        elif value["_type"]=="Compare":
            left=val(value["left"])
            right=val(value["comparators"][0])
            op=ops[value["ops"][0]["_type"]]
            return left + op+right
        
def extract(node):
    if node["_type"]=="Assign":
        stmt=""
        for x in node["targets"]:
            stmt+=val(x)+"="
        assign.append(stmt+val(node["value"]))
        s=stmt+val(node["value"])
        blocks[s]="Assign"
    elif node["_type"]=="If":
        cond=val(node["test"])
        branch.append(cond)
        blocks[cond]="branch"
        for x in node["body"]:
            extract(x)
        for x in node["orelse"]:
            extract(x)

for l in data["body"]:
    extract(l)
print("Assignment Statement")
for a in assign:
    print(a)
print("\nBranch Conditions")
for a in branch:
        print(a)
print(blocks)