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


#Keys: parents state, values: probability
#-1 = orphan
S_p_table = dict({'-1': .2})
R_p_table = dict({'-1': .4})
W_wet_p_table = dict({'0': .1}, {'1': .75})
H_wet_p_table = dict({'00': .15}, {'01': .95}, {'10': .8}, {'11': .99})

R_node = Node('R', R_p_table)
S_node = Node('S', S_p_table)
W_node = Node('W', W_wet_p_table)
H_node = Node('H', H_wet_p_table)

nodes = {'R':R_node, 'S':S_node, 'W':W_node, 'H':H_node}

given_states_example = {'H':1,'W':1}
p_x_state_example = {'R':1}

def infer_probability(p_x_state : dict, given_states: dict):
    #set observered nodes
    for n in given_states.keys():






infer_probability(given_states_example, p_x_state_example)