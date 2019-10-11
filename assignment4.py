#  R  S
#  |\ |
#  | \|
#  W  H



class Node:
    def __init__(self, name, p_table ):
        self.name = name
        self.p_table = p_table
        self.state = 0
        # number of times state = 0, and state = 1:
        self.distrobution = {0:0,1:0}
        self.parents = {}
        self.children ={}

R_node = Node('R', None)
S_node = Node('S', None)
W_node = Node('W', None)
H_node = Node('H', None)

nodes = {'R':R_node, 'S':S_node, 'W':W_node, 'H':H_node}


given_states_example = {'H':1,'W':1}
p_x_state_example = {'R':1}

def infer_probability(p_x_state : dict, given_states: dict):
    #set observered nodes
    for n in given_states.keys():






infer_probability(given_states_example, p_x_state_example)