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
        # n = self.name
        # s = self.state
        # r = n+s
        return self.name + str(self.state)

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
        p_x = self.p_given_parents()
        p_not_x = 1 - p_x
        if self.children != {}:
            for child in self.children.values():
                p_child = child.p_given_parents()
                p_x *= p_child
                p_not_x *= (1 - p_child)
        alpha = 1 / (p_x + p_not_x)
        p_x = p_x*alpha

        if random.random() < p_x:
            self.state = 1
            self.distribution[1] += 1
        else:
            self.state = 0
            self.distribution[0] += 1

    def get_probability(self, state: int):
        state_0 = self.distribution[0]
        state_1 = self.distribution[1]
        if state == 0:
            return round(state_0 / (state_0 + state_1) * 100)
        elif state == 1:
            return round(state_1 / (state_0 + state_1) * 100)

#Keys: parents state, values: probability
#-1 = orphan
S_p_table = {'-1': .2}
R_p_table = {'-1': .4}
W_wet_p_table = {'R0': .01, 'R1': .90}
H_wet_p_table = {'R0S0': .15,'R0S1': .95, 'R1S0': .8, 'R1S1': .99}

R_node = Node('R', R_p_table)
S_node = Node('S', S_p_table)
W_node = Node('W', W_wet_p_table)
H_node = Node('H', H_wet_p_table)

nodes = {'R':R_node, 'S':S_node, 'W':W_node, 'H':H_node}

R_parents = {}
S_parents = {}
W_parents = {'R': R_node}
H_parents = {'R': R_node, 'S': S_node}

R_node.parents = R_parents
S_node.parents = S_parents
W_node.parents = W_parents
H_node.parents = H_parents

R_children = {'W': W_node}
S_children = {'H': H_node, 'W': W_node}
W_children = {}
H_children = {}

R_node.children = R_children
S_node.children = S_children
W_node.children = W_children
H_node.children = H_children


def infer_probability(x_key: str, x_state: int, given_states: dict):
    for node in nodes.values():
        for value in node.distribution.values():
            value = 0

    #Set nodes to observed values or to random values if they are unobserved
    observed_nodes = {}
    unobserved_nodes = {}
    for n in nodes.keys():
        if n in given_states:
            nodes[n].state = given_states[n]
            observed_nodes[n] = nodes[n]
        else:
            nodes[n].state = random.choice(list({0,1}))
            unobserved_nodes[n] = nodes[n]
    #Stocastic simulation of probabilities
    for i in range(1000):
        random_node = random.choice(list(unobserved_nodes.values()))
        random_node.update()

    print('Probability of ', x_key, '=', x_state, ' given ', given_states, ' is ', nodes[x_key].get_probability(x_state), '%')

infer_probability('R', 1 , {'H':1, 'W':1})
infer_probability('S', 1 , {'H':1, 'W':1})
infer_probability('R', 1 , {'W':1})
infer_probability('W', 1 , {'S':1})
infer_probability('H', 1 , {'S':0, 'R':1 })
infer_probability('H', 1 , {'R':1})








