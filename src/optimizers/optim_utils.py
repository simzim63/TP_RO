import random
import numpy as np

def find_best_neighbor(problem, solution, fonction_evaluation):
    best_solution = solution.copy()
    best_value = fonction_evaluation(problem, solution)
    for i in solution.keys():
        for new_freq in problem.get_domain_of_variable(i):
            current_solution = solution.copy()
            current_solution[i] = new_freq
            value = fonction_evaluation(problem, current_solution)
            if value < best_value:

                best_value = value
                best_solution = current_solution
    return best_value, best_solution

def find_best_neighbor_with_tabou(problem, solution, fonction_evaluation, current_list_tabou, tabou_element_function):
    best_value = None
    best_element_tabou = None
    for i in solution.keys():
        for new_freq in problem.get_domain_of_variable(i):
            current_solution = solution.copy()
            current_solution[i] = new_freq
            value = fonction_evaluation(problem, current_solution)
            element_tabou = tabou_element_function(i, new_freq, value)
            if (best_value is None or value < best_value) and element_tabou not in current_list_tabou:
                store = (i, new_freq)
                best_value = value
                best_solution = current_solution
                best_element_tabou = element_tabou
    if best_value is None:
        return None, None, None
    return best_value, best_solution, best_element_tabou


def random_neighbor(problem, solution):
    chosen_antenna = random.choice(list(problem.variables.keys()))
    freqs = problem.get_domain_of_variable(chosen_antenna)
    chosen_freq = solution[chosen_antenna]
    new_solution = solution.copy()

    freq_changed = False
    while not freq_changed:
        chosen_freq = random.choice(freqs)
        freq_changed = chosen_freq != solution[chosen_antenna]
    new_solution[chosen_antenna] = chosen_freq
    return new_solution

def random_first_solution(problem):
    solution = {}
    for i in problem.variables.keys():
        solution[i] = random.choice(problem.get_domain_of_variable(i))
    return solution