import random


def get_arms(prior: tuple, n_arms: int):
    beta_arms = [list(prior) for k in range(n_arms)]
    print(beta_arms)
    return beta_arms


def select_arm_with_thompson_sampling_beta_dist(arms, desired):
    sample_delta_from_desired = [desired - random.gauss(arm[0], arm[1]) for arm in arms]
    best_arm = max(enumerate(sample_delta_from_desired), key=lambda x: x[1])
    return best_arm[0]


def play_arm(arm_i):
    # interact with the random environment
    # in this case we assume that the best arm has a reward prob of 80%
    # and the rest arms has a 40% win prob
    best_arm_hidden_from_user = 3
    if arm_i == best_arm_hidden_from_user:
        return random.gauss(8,3)

    else:
        return random.gauss(5,4)


def update_arms_with_conjugate_prior(arm, reward):
    alpha = arm[0]
    beta = arm[1]
    if reward:
        return alpha + 1, beta

    else:
        return alpha, beta + 1


T = 100
n_arms = 5
prior = (1.0, 1.0)

arms = get_arms(prior, n_arms)
rewards = 0
desired_value = 0

for t in range(T):
    best_arm = select_arm_with_thompson_sampling_beta_dist(arms)
    reward_t = play_arm(best_arm)
    rewards += reward_t

    updated_arm_dist = update_arms_with_conjugate_prior(arms[best_arm], reward_t)
    arms[best_arm] = updated_arm_dist

print("-----")
print("total reward: {}".format(rewards))
print("---- arms -----")
for k, arm in enumerate(arms):
    print("arm {} => dist: ({}, {}) ".format(k, arm[0], arm[1]))