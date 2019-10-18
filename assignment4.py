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

    #What is the probability of the node beeing in it's current state given the current state of it's parents
    def p_given_parents(self):
        p = self.p_table[self.get_parents_state()]
        if self.state == 1:
            return p
        else:
            return 1-p

    #Get the state of parents, in a format compatible with the probability tables. Rain = 1, Sprinkler = 0: R1S0
    def get_parents_state(self):
        #check for orphans
        if not self.parents:
            return '-1'
        s = ''
        for parent in self.parents.values():
            s += parent.get_state_as_str()
        return s

    def get_state_as_str(self):
        return self.name + str(self.state)



    def stochastic_simulation_run(self):
        self.state = 1
        p_x = self.p_given_parents()    #P(x=1|current state of parents)
        p_not_x = 1 - p_x               #P(x=0|current state of parents)
        if self.children != {}:
            for child in self.children.values():
                p_child = child.p_given_parents() # P( child in it's current state| current state of it's  parents)
                p_x *= p_child

            self.state = 0
            for child in self.children.values():
                p_child = child.p_given_parents()
                p_not_x *= p_child

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
R_p_table = {'-1': .4}
S_p_table = {'-1': .2}
W_wet_p_table = {'R0': .001, 'R1': .90}
H_wet_p_table = {'R0S0': .002,'R0S1': .90, 'R1S0': .91, 'R1S1': .99}


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

R_children = {'W': W_node, 'H': H_node}
S_children = {'H': H_node}
W_children = {}
H_children = {}

R_node.children = R_children
S_node.children = S_children
W_node.children = W_children
H_node.children = H_children


def infer_probability(x_key: str, x_state: int, given_states: dict):
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
    for node in nodes.values():
        for value in node.distribution.values():
            value = 0
    #Stocastic simulation of probabilities
    for i in range(1000):
        random_node = random.choice(list(unobserved_nodes.values()))
        random_node.stochastic_simulation_run()
    print('Probability of ', x_key, '=', x_state, ' given ', given_states, ' is ', nodes[x_key].get_probability(x_state), '%')

infer_probability('R', 1 , {'H':1, 'W':1})
infer_probability('R', 1 , {'H':0, 'W':0})
infer_probability('S', 1 , {'H':0, 'W':1})
infer_probability('S', 1 , {'H':1, 'W':0})
infer_probability('R', 1 , {'W':1})
infer_probability('W', 1 , {'S':1})
infer_probability('H', 1 , {'S':0, 'R':1 })


#infer_probability('Questions', True , {'Perfect presentation'})

# infer_probability('Questions', True , {'Perfect presentation'})

        # print('---------------------')
        # print('Node    = ', self.name)
        # print('Alpha   = ',alpha)
        # print('p_x     = ',p_x )
        # print('p_not_x = ',p_not_x)
        # print('1       = ',alpha * (p_x + p_not_x))
        # print('---------------------')


# def update(self):
#     p_x = self.p_given_parents()
#     p_not_x = 1 - p_x
#     if self.children != {}:
#         for child in self.children.values():
#             p_child = child.p_given_parents()
#             p_x *= p_child
#             p_not_x *= (1 - p_child)
#
#     alpha = 1 / (p_x + p_not_x)
#
#     p_x = p_x*alpha
#
#     if random.random() < p_x:
#         self.state = 1
#         self.distribution[1] += 1
#     else:
#         self.state = 0
#         self.distribution[0] += 1
#





