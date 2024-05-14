import sys
import json
from pathlib import Path
import matplotlib.pyplot as plt
from bb import *
import networkx as nx
if (args_count := len(sys.argv)) > 2:
    print(f"One argument expected, got {args_count - 1}")
    raise SystemExit(2)
elif args_count < 2:
    print("You must specify the target directory")
    raise SystemExit(2)


f=open(sys.argv[1])
data = json.load(f)
ops={"Gt":">", "Lt":"<","Eq":"==","NotEq":"!=","GtE":">=","LtE":"<=","Add":"+" , "Sub":"-", "Mult":"*"}
size=0
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
def buildcfg(node,size):
    if node["_type"]=="Assign":
        stmt=""
        for x in node["targets"]:
            stmt+=val(x)+"="
        s=stmt+val(node["value"])
        # size=size+1
        bb=BasicBlock(s)
        leader2IndicesMap.append(bb)
        bb2typeMap[bb]="Assign"
    elif node["_type"]=="If":
        cond=val(node["test"])
        # size+=1
        bb=BasicBlock(cond)
        leader2IndicesMap.append(bb)
        bb2typeMap[bb]="Cond"
        for x in node["body"]:
            buildcfg(x)
        for x in node["orelse"]:
            buildcfg(x)




startBB = BasicBlock('START')
endBB = BasicBlock('END')

leader2IndicesMap = [startBB]
bb2typeMap = {startBB: 0}
for l in data["body"]:
    buildcfg(l,size)

cfg=ControlFlowGraph()
for leader in leader2IndicesMap:
    cfg.add_node(leader)
x=len(leader2IndicesMap)
# l=leader2IndicesMap.keys()
for i in range(x-1):
    if bb2typeMap[leader2IndicesMap[i]]!="Cond":
            cfg.add_edge(leader2IndicesMap[i], leader2IndicesMap[i+1], label='Cond_True', color='green')
pos = nx.spring_layout(cfg.nxgraph)
nx.draw(cfg.nxgraph, pos, with_labels=True, font_weight='bold', node_size=700, node_color="skyblue")
plt.savefig("filename.png")
plt.show()
