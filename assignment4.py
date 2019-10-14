#  R  S
#  |\ |
#  | \|
#  W  H

import random

class Node:
    def __init__(self, name, p_table):
        self.name = name
        self.p_table = p_table
        self.state = 0
        # number of times state = 0, and state = 1:
        self.distribution = {0:0, 1:0}
        self.parents = {}
        self.children = {}

    def get_state_as_str(self):
        return str(self.state)

    def get_parents_state(self):
        #check for orphans
        if not self.parents:
            return '-1'

        s = ''
        for parent in self.parents.values():
            s += parent.get_state_as_str()
        return s

    def p_given_parents(self):
        return self.p_table[self.get_parents_state()]

    def update(self):
        p_x =  self.p_given_parents()
        p_not_x = 1 - self.p_given_parents() #Kan vel ta 1-p_x bare? :)
        if self.children != {}:
            for child in self.children.values():
                temp = child.p_given_parents()
                p_x *= temp
                p_not_x *= (1 - temp)
        alpha = 1 / (p_x + p_not_x)

        p_x = p_x*alpha

        if random.random() < p_x:
            self.state = 1
            self.distribution[1] += 1
        else:
            self.state = 0
            self.distribution[0] += 1

#Keys: parents state, values: probability
#-1 = orphan
S_p_table = {'-1': .2}
R_p_table = {'-1': .4}
W_wet_p_table = {'0': .1, '1': .75}
H_wet_p_table = {'00': .15,'01': .95, '10': .8, '11': .99}

R_node = Node('R', R_p_table)
S_node = Node('S', S_p_table)
W_node = Node('W', W_wet_p_table)
H_node = Node('H', H_wet_p_table)

nodes = {'R':R_node, 'S':S_node, 'W':W_node, 'H':H_node}

R_parents = {}
S_parents = {}
W_parents = {'R' : R_node}
H_parents = {'R' : R_node, 'S' : S_node}

R_node.parents = R_parents
S_node.parents = S_parents
W_node.parents = W_parents
H_node.parents = H_parents

R_children = {'W': W_node}
S_children = {'H' : H_node, 'W' : W_node}
W_children = {}
H_children = {}

R_node.children = R_children
S_node.children = S_children
W_node.children = W_children
H_node.children = H_children


given_states_example = {'H':1,'W':1}
p_x_state_example = {'R':1}

def infer_probability(p_x_state : dict, given_states: dict):

    # Remember d-seperation

    #Set nodes to observed values or to random values if they are unobserved
    observed_nodes = {}
    unobserved_nodes = {}
    for n in nodes.keys():
        if n in given_states:
            nodes[n].state = given_states[n]
            observed_nodes[n] = nodes[n]
        # elif n not in p_x_state:
        #     nodes[n].state = random.randrange(0,1)
        #     unobserved_nodes[n] = nodes[n]
        else:
            nodes[n].state = random.randrange(0,1)
            unobserved_nodes[n] = nodes[n]

    for i in range(10):
        random_node = random.choice(list(unobserved_nodes.values()))
        random_node.update()

infer_probability(p_x_state_example, given_states_example)

for n in nodes.values():
    print(n.distribution)








