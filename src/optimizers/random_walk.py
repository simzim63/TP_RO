from TP_RO.src.drawer import draw_solution, reset_drawer
from TP_RO.src.optimizers.optim_utils import random_first_solution, random_neighbor


def random_walk_with_initial_solution(problem, initial_solution, fonction_evaluation, max_iterations, display = True):
    current_solution = initial_solution.copy()
    current_value = fonction_evaluation(problem, current_solution)
    best_solution = current_solution.copy()
    best_value = current_value
    n_iterations = 0
    if display:
        reset_drawer()
        draw_solution(problem, current_solution, best_solution, fonction_evaluation)
    while (max_iterations is None or n_iterations < max_iterations):
        n_iterations += 1
        current_solution = random_neighbor(problem, current_solution)
        current_value = fonction_evaluation(problem, current_solution)
        if current_value < best_value:
            best_solution = current_solution.copy()
            best_value = current_value
        if display:
            draw_solution(problem, current_solution, best_solution, fonction_evaluation)
    if display:
        draw_solution(problem, current_solution, best_solution, fonction_evaluation, end_of_exec = True)
    return best_value, best_solution

def random_walk(problem, fonction_evaluation, max_iterations = None, display = True):
    return random_walk_with_initial_solution(problem, random_first_solution(problem), fonction_evaluation, max_iterations, display = display)
