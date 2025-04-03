from unittest import TestCase

from src.evaluation import creer_matrice_ecarts
from src.optimizers.optim_utils import find_best_neighbor, random_neighbor, random_first_solution, \
    find_best_neighbor_with_tabou
from src.problem import load_problem
import numpy as np

class TestAgentShape(TestCase):

    def fonction_evaluation(self, problem, solution):
        eval_matrix = creer_matrice_ecarts(problem, solution)
        # evaluation = eval_matrix.sum()/2
        # evaluation = eval_matrix.max()
        # evaluation = np.count_nonzero(eval_matrix) / 2
        evaluation = 20 * eval_matrix.max() + eval_matrix.sum() / 2 + 50 * np.count_nonzero(eval_matrix) / 2

        return (evaluation)
    def test_find_best_neighbor(self):
        problem = load_problem("./test_problem_optim_utils.txt")
        solution = {1 : 5, 2 : 1, 3 : 9}
        value, best_neighbor = find_best_neighbor(problem, solution, self.fonction_evaluation)
        self.assertEqual(best_neighbor, {1 : 5, 2 : 1, 3 : 11})

    def test_find_best_neighbor_with_tabou(self):
        problem = load_problem("./test_problem_optim_utils.txt")
        solution = {1 : 5, 2 : 1, 3 : 9}
        def tabou_function(i, freq, value):
            return i
        tabou_list = [3]
        value, best_neighbor, element_tabou = find_best_neighbor_with_tabou(problem, solution, self.fonction_evaluation, tabou_list, tabou_function)
        self.assertEqual(best_neighbor, {1 : 5, 2 : 0, 3 : 9})
        def tabou_function2(i, freq, value):
            return (i, freq)
        tabou_list2 = [(3, 9)]
        value, best_neighbor, element_tabou = find_best_neighbor_with_tabou(problem, solution, self.fonction_evaluation, tabou_list2, tabou_function2)
        self.assertEqual(best_neighbor, {1 : 5, 2 : 1, 3 : 11})
        def tabou_function3(i, freq, value):
            return (i, freq)
        tabou_list3 = [(3, 11)]
        value, best_neighbor, element_tabou = find_best_neighbor_with_tabou(problem, solution, self.fonction_evaluation, tabou_list3, tabou_function3)
        self.assertEqual(best_neighbor, {1 : 5, 2 : 0, 3 : 9})

    def test_random_neighbor(self):
        problem = load_problem("./test_problem_optim_utils2.txt")
        self.assertEqual(list(problem.domains.keys()), [0,1,2])
        self.assertEqual(problem.domains[0], [5,6,7])
        self.assertEqual(problem.domains[1], [0,1,3])
        self.assertEqual(problem.domains[2],[9,11,13])
        solution = {1 : 5, 2 : 1, 3 : 13}
        for i in range(1000):
            new_solution = random_neighbor(problem, solution)
            for j in problem.variables.keys():
                self.assertTrue(new_solution[j] in  problem.get_domain_of_variable(j))
                n_diffs = sum(i != j for i,j in zip(solution.values(), new_solution.values()))
                self.assertTrue(n_diffs == 1)

    def test_random_solution(self):
        problem = load_problem("./test_problem_optim_utils2.txt")
        for i in range(100):
            solution = random_first_solution(problem)
            self.assertEqual(solution.keys(), problem.variables.keys())
            for i in solution.keys():
                self.assertTrue(solution[i] in problem.get_domain_of_variable(i))