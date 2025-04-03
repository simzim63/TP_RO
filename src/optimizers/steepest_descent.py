from TP_RO.src.drawer import draw_solution, reset_drawer
from TP_RO.src.optimizers.optim_utils import random_first_solution, find_best_neighbor


def steepest_descent_with_initial_solution(problem, initial_solution, fonction_evaluation, max_iterations, display = True):
    current_solution = initial_solution.copy()
    current_value = fonction_evaluation(problem, current_solution)
    best_value_found = False
    n_iterations = 0
    if display:
        reset_drawer()
        draw_solution(problem, current_solution, current_solution, fonction_evaluation)
    while not best_value_found and (max_iterations is None or n_iterations < max_iterations):
        n_iterations += 1
        new_value, new_solution = find_best_neighbor(problem, current_solution, fonction_evaluation)
        if new_value >= current_value:
            best_value_found = True
        else:
            current_solution = new_solution
            current_value = new_value
        if display:
            draw_solution(problem, current_solution, current_solution, fonction_evaluation)
    if display:
        draw_solution(problem, current_solution, current_solution, fonction_evaluation, end_of_exec = True)
    return current_value, current_solution

def steepest_descent(problem, fonction_evaluation, max_iterations = None, display = True):
    return steepest_descent_with_initial_solution(problem, random_first_solution(problem), fonction_evaluation, max_iterations, display = display)
