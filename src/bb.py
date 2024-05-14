import networkx as nx
from tac import tac
class BasicBlock:
    def __init__(self, bbname):
        # self.indx=indx
        self.name = bbname
        self.pred = []
        self.succ=[]
        self.instrlist = []
        self.type=None
        self.tac=None
        if bbname == "START" or bbname == "END":
            self.irID = bbname
        else:
            self.irID = (bbname) 

    def __str__(self):
        return f'{self.name}'

    def add_tac(self,tac):
        self.tac=tac

    def append(self, instruction):
        self.instrlist.append(instruction)

    def extend(self, instructions):
        self.instrlist.extend(instructions)

    def label(self):
        if len(self.instrlist):
            return '\n'.join(str(instr[0])+'; L'+ str(instr[1]) for instr in self.instrlist)
        else:
            return self.name
    def addpre(self,BasicBlock):
        self.pred.append(BasicBlock)
    
    def addsucc(self,BasicBlock):
        self.succ.append(BasicBlock)

class ControlFlowGraph:
    def __init__(self,gname='cfg'):
        self.blocks = []
        self.name = gname
        self.nxgraph = nx.DiGraph(name=gname)
        self.entry = "0"
        self.exit = "END"

    def __iter__(self):
        return self.nxgraph.__iter__()

    def is_directed(self):
        return True

    def add_node(self, node):
        if not isinstance(node, BasicBlock):
            raise ValueError("wrong type for 'node' parameter")

        self.nxgraph.add_node(node)

    def has_node(self, node):
        return self.nxgraph.has_node(node)

    def add_edge(self, u, v, **attr):
        if self.has_node(u):
            if self.has_node(v):
                self.nxgraph.add_edge(u, v, **attr)
            else:
                # TODO: do appropriate error reporting
                raise NameError(v)
        else:
            raise NameError(u)

    def nodes(self):
        return self.nxgraph.nodes()

    def edges(self):
        return self.nxgraph.edges()

    def successors(self, node):
        return self.nxgraph.successors(node)

    def predecessors(self, node):
        return self.nxgraph.predecessors(node)

    def out_degree(self, node):
        return self.nxgraph.out_degree(node)

    def in_degree(self, node):
        return self.nxgraph.in_degree(node)

    def get_edge_label(self, u, v):
        edata = self.nxgraph.get_edge_data(u,v)
        # print(edata)
        return edata['label'] if len(edata) else 'T'