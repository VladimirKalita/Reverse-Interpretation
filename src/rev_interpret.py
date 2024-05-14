import sys
import json
import matplotlib.pyplot as plt
import networkx as nx
from bb import ControlFlowGraph, BasicBlock
from tac import tac, find_tac
from AI import *
from worklist import *
from lattice import *
file_path = sys.argv[1]

with open(file_path) as f:
    data = json.load(f)

ops = {"Gt": ">", "Lt": "<", "Eq": "==", "NotEq": "!=", "GtE": ">=", "LtE": "<=", "Add": "+", "Sub": "-", "Mult": "*"}
ir=[]

def val(value):
    if value is not None:
        if value["_type"] == "Constant":
            return str(value["value"])
        elif value["_type"] == "Name":
            return value["id"]
        elif value["_type"] == "BinOp":
            op = ops[value["op"]["_type"]]
            left = val(value["left"])
            right = val(value["right"])
            return f'({left}{op}{right})'
        elif value["_type"] == "Compare":
            left = val(value["left"])
            right = val(value["comparators"][0])
            op = ops[value["ops"][0]["_type"]]
            return f'{left}{op}{right}'

def offset(node):
    if node["_type"]=="Assign":
        return 1
    elif node["_type"]=="Expr":
        return 1
    elif node["_type"]=="If":
        offst=2
        for l in node["body"]:
            offst+= offset(l)
        for l in node["orelse"]:
            offst+= offset(l)
        return offst

def build_ir(node):
    if node["_type"]=="Assign":
        item=[]
        if node["value"]["_type"]!="Call":
            s=val(node["targets"][0])+"="+val(node["value"])
            bb=BasicBlock(s)
            bb.add_tac(find_tac(node))
            item.append(bb)
            item.append(1)
            ir.append(item)
        else:
            s=val(node["targets"][0])+"="
            bb=BasicBlock(s)
            bb.add_tac(find_tac(node))
            bb.name+=str(bb.tac.arg1)
            item.append(bb)
            item.append(1)
            ir.append(item)
    elif node["_type"]=="If":
        cond=[]
        s=val(node["test"])
        bb=BasicBlock(s)
        bb.add_tac(find_tac(node["test"],is_tac=True))
        cond.append(bb)
        cond_offs=2
        for l in node["body"]:
            cond_offs+=offset(l)
        cond.append(cond_offs)
        ir.append(cond)
        for b in node["body"]:
            build_ir(b)
        fals=[]
        fals.append("False")
        false_offs=1
        for l in node["orelse"]:
            false_offs+=offset(l)
        fals.append(false_offs)
        ir.append(fals)
        for b in node["orelse"]:
            build_ir(b)
    elif node["_type"]=="While":
        cond=[]
        s=val(node["test"])
        bb=BasicBlock(s)
        bb.type="while"
        bb.add_tac(find_tac(node["test"],is_tac=True))
        cond.append(bb)
        cond_offs=2
        for l in node["body"]:
            cond_offs+=offset(l)
        cond.append(cond_offs)
        ir.append(cond)
        for b in node["body"]:
            build_ir(b)
        fals=[]
        fals.append("False")
        fals.append(-(cond_offs-1))
        ir.append(fals)
    elif node["_type"]=="Expr":
        if node["value"]["_type"]=="Call":
            call=node["value"]
            if call["args"][0]["_type"]=="Compare":
                cond=[]
                s=val(call["args"][0])
                bb=BasicBlock("assume_"+s)
                bb.type="assume"
                tace=find_tac(call["args"][0],is_tac=True)
                tace.type="assume"
                bb.add_tac(tace)
                cond.append(bb)
                cond.append(1)
                ir.append(cond)

for node in data["body"]:
    build_ir(node)

for idx,item in enumerate(ir):
    print(idx,item[0],"[",item[1],"]")
    # if(item[0].type=="while"):
        # print("1wheel")
print('---------')
def genNode(d=None,id1=None):
    global nodes

    if id1 not in nodes.keys():
        if d!=None:
            s=''
            typ=None
            l=[]
            for x in d:
                if isinstance(x,BasicBlock):
                    s+=(str(x)+'\n')
                    if x.type=="while":
                        typ="while"
                    l.append(x.tac)
                else:
                    s+=x
            bb=BasicBlock(s)
            if typ!=None:
                bb.type="while"
            bb.instrlist=l
            nodes[id1]=bb
        else:
            nodes[id1]=BasicBlock('Termination')

def targetcalc(ir): ##Calculates targets for jump statements
	
	global t
	t=[]
	
	for idx,item in enumerate(ir):
		
		if(item[1]!=1):
			
			t.append(idx+item[1])

edges=[]

def build_cfg(ir):
    targetcalc(ir)
    global nodes
    nodes=dict()

    data=[]
    global t
    print(t)
    id1=0

    for idx,item in enumerate(ir):
        if len(data)==0:
            print(idx)
            id1=idx
            data.append(item[0])

            if item[1]!=1:
                genNode(data,id1)
                edges.append([id1,idx+1,"True"])
                edges.append([id1,idx+item[1],"False"])

                data=[]
        else:
            if item[1]==1:
                print('ii',idx)
                if idx not in t:
                    data.append(item[0])
                else:
                    genNode(data,id1)
                    edges.append([id1,idx,"Forward"])
                    data=[item[0]]
                    id1=idx
                    print(id1)
            else:
                if idx not in t:
                    if item[0]!="False":
                        edges.append([id1,idx+1,"True"])
                    data.append(item[0])
                    genNode(data,id1)
                    if item[0]=="False":
                        edges.append([id1,idx+item[1],"Merge"])
                    else:
                        edges.append([id1,idx+item[1],"False"])
                else:
                    genNode(data,id1)
                    edges.append([id1,idx,"Forward"])

                    genNode([item[0]],idx)
                    edges.append([idx,idx+1,"True"])
                    edges.append([idx,idx+item[1],"False"])
                data=[]
    
    if len(data)!=0:
        genNode(data,id1)
        edges.append([id1,len(ir),"Term"])
    genNode(d=None,id1=len(ir))

    print(edges)

build_cfg(ir)
cfg=ControlFlowGraph()
bbstart=BasicBlock("Start")
cfg.add_node(bbstart)
for id,node in nodes.items():
    print("nodes",id,type(node),node)
    cfg.add_node(node)
cfg.add_edge(bbstart,nodes[0])
for e in edges:
    cfg.add_edge(nodes[e[0]], nodes[e[1]], label=e[2])

abstractI=AbstractInterpreter(cfg)
bbin,bbout=abstractI.worklistAlgorithm(cfg)

print(type(bbin))
print(type(bbout))

for i,(a,b) in enumerate(bbin.items()):
    # for x in b['b']:
        # for y in x:
        # print(a,"b value", x)
    for x in b['a']:
        # for y in x:
        print(a,"a value", x)
    for x in b['i']:
        # for y in x:
        print(a,"i value", x)
    for x in b['j']:
        # for y in x:
        print(a,"j value", x)
    for x in b['k']:
        # for y in x:
        print(a,"k value", x)

for i,(a,b) in enumerate(bbout.items()):
    # print(a,b[0]['a'][0])
    # if len(b[0]['a'])>1:
    #     print(b[0]['a'][1])
    for x in b:
        # for y in x['b']:
            # print(a,"b value",y) 
        for y in x['a']:
        # for y in x:
            print(a,"a value", y)
        for y in x['i']:
            print(a,"i value",y)
        for y in x['j']:
            print(a,"j value",y) 
        for y in x['k']:
            print(a,"k value",y)  
          

pos = nx.planar_layout(cfg.nxgraph)
nx.draw(cfg.nxgraph, pos, with_labels=True, font_weight='bold', node_size=700, node_color="skyblue")
plt.savefig("filename.png")
plt.show()






















