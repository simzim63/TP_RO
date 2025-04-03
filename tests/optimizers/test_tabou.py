from unittest import TestCase

from TP_RO.src.evaluation import creer_matrice_ecarts, fonction_evaluation
from TP_RO.src.optimizers import tabou
from TP_RO.src.optimizers.steepest_descent import steepest_descent_with_initial_solution, steepest_descent
from TP_RO.src.problem import load_problem
import numpy as np
from src.optimizers.tabou import tabou

class TestSteepestDescent(TestCase):


    def test_draw_realistic_example(self):
        problem = load_problem("fapp05_0050.coo")
        def element_tabou_function(i, freq, value):
            return (i,value)
        value, solution = tabou(problem, fonction_evaluation,  max_without_improvement = 100, length_list_tabou = 20, tabou_element_function = element_tabou_function, max_iterations = None, display = True)
