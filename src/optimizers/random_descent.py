from src.drawer import draw_solution, reset_drawer
from src.optimizers.optim_utils import random_first_solution, find_best_neighbor, random_neighbor


def random_descent_with_initial_solution(problem, initial_solution, fonction_evaluation, max_iterations, display = True):
    current_solution = initial_solution.copy()
    current_value = fonction_evaluation(problem, current_solution)
    n_iterations = 0
    if display:
        reset_drawer()
        draw_solution(problem, current_solution, current_solution, fonction_evaluation)
    while (max_iterations is None or n_iterations < max_iterations):
        n_iterations += 1
        solution = random_neighbor(problem, current_solution)
        value = fonction_evaluation(problem, solution)
        if value < current_value:
            current_solution = solution.copy()
            current_value = value
        if display:
            draw_solution(problem, current_solution, current_solution, fonction_evaluation)
    if display:
        draw_solution(problem, current_solution, current_solution, fonction_evaluation, end_of_exec = True)
    return current_value, current_solution

def random_descent(problem, fonction_evaluation, max_iterations = None, display = True):
    return random_descent_with_initial_solution(problem, random_first_solution(problem), fonction_evaluation, max_iterations, display = display)
