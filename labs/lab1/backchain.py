from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    goal_tree = OR()
    goal_tree.append(hypothesis)  # The hypothesis is the ultimate CSF

    if not rules:
        return list(goal_tree)  # Bad base test? Not sure why the need to cast back to list

    for rule in rules:
        consequent = rule.consequent()[0]  # should handle multiple?
        bindings = match(consequent, hypothesis)

        if bindings:
            antecedent = rule.antecedent()
            if isinstance(antecedent, AND):
                branch = AND()
                for condition in antecedent:
                    cond = populate(condition, bindings)
                    branch.append(backchain_to_goal_tree(rules, cond))
                goal_tree.append(branch)
            elif isinstance(antecedent, OR):
                branch = OR()
                for condition in antecedent:
                    cond = populate(condition, bindings)
                    branch.append(backchain_to_goal_tree(rules, cond))
                goal_tree.append(branch)
            else:  # leaf
                leaf = populate(antecedent, bindings)
                goal_tree.append(leaf)

    return simplify(goal_tree)

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
