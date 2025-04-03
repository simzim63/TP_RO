from unittest import TestCase

from src.evaluation import creer_matrice_ecarts, fonction_evaluation
from src.optimizers.steepest_descent import steepest_descent_with_initial_solution, steepest_descent
from src.problem import load_problem
import numpy as np


class TestSteepestDescent(TestCase):

    def test_steepest_descent_with_initial_solution(self):
        problem = load_problem("./test_problem_optim_utils2.txt")
        initial_solution = { 1 : 6, 2 : 3, 3 : 9}
        new_value, new_solution = steepest_descent_with_initial_solution(problem, initial_solution, fonction_evaluation, None, display= False)
        self.assertEqual(new_solution, { 1 : 6, 2 : 0, 3 : 13})


    def test_realistic_example(self):
        problem = load_problem("fapp05_0050.coo")
        for i in range(50):
            value, solution = steepest_descent(problem, fonction_evaluation)
            eval_matrix = creer_matrice_ecarts(problem, solution, fonction_evaluation)
            print(np.count_nonzero(eval_matrix))

    def test_draw_realistic_example(self):
        problem = load_problem("fapp05_0050.coo")
        value, solution = steepest_descent(problem, fonction_evaluation)