from src.drawer import draw_solution, reset_drawer
from src.optimizers.optim_utils import random_first_solution, find_best_neighbor, find_best_neighbor_with_tabou
from collections import deque

def tabou_with_initial_solution(problem, initial_solution, fonction_evaluation, max_without_improvement, length_list_tabou, tabou_element_function, max_iterations, display = True):
    current_solution = initial_solution.copy()
    current_value = fonction_evaluation(problem, current_solution)
    best_solution = current_solution
    best_value = current_value
    n_iterations = 0
    list_tabou = deque([], length_list_tabou)
    n_iterations_without_improvement = 0
    if display:
        reset_drawer()
        draw_solution(problem, current_solution, best_solution, fonction_evaluation)
    while (n_iterations_without_improvement < max_without_improvement) and (max_iterations is None or n_iterations < max_iterations):
        n_iterations += 1
        new_value, new_solution, element_tabou = find_best_neighbor_with_tabou(problem, current_solution, fonction_evaluation, list_tabou, tabou_element_function)
        if new_value is None:
            break
        list_tabou.appendleft(element_tabou)
        current_solution = new_solution
        current_value = new_value
        if new_value >= best_value:
            n_iterations_without_improvement += 1
        else:
            n_iterations_without_improvement = 0
            best_solution = new_solution.copy()
            best_value = new_value
        if display:
            draw_solution(problem, current_solution, best_solution, fonction_evaluation)
    if display:
        draw_solution(problem, current_solution, best_solution, fonction_evaluation, end_of_exec = True)
    return current_value, current_solution

def tabou(problem, fonction_evaluation,  max_without_improvement, length_list_tabou, tabou_element_function, max_iterations = None, display = True):
    return tabou_with_initial_solution(problem, random_first_solution(problem), fonction_evaluation, max_without_improvement, length_list_tabou, tabou_element_function,  max_iterations = max_iterations, display = display)
