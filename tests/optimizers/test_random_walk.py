from unittest import TestCase

from TP_RO.src.evaluation import fonction_evaluation
from TP_RO.src.optimizers.random_walk import random_walk
from TP_RO.src.problem import load_problem


class TestRandomWalk(TestCase):
    def test_draw_realistic_example(self):
        problem = load_problem("fapp05_0050.coo")
        value, solution = random_walk(problem, fonction_evaluation)
