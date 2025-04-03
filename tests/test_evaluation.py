from unittest import TestCase

from TP_RO.src.evaluation import creer_matrice_ecarts
from TP_RO.src.problem import load_problem


class TestAgentShape(TestCase):

    def test_creer_matrice_evaluation(self):
        problem = load_problem("test_problem_2.txt")
        solution = {0 : 5, 1 : 9, 3 : 9}
        m = creer_matrice_ecarts(problem, solution)
        self.assertEqual(m.tolist(), [[0, 4.0, 0, 5.0], [0, 0,0,0], [0, 0,0,0], [0, 0,0,0]])
