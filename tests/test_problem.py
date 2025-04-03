from unittest import TestCase

from src.problem import load_problem


class TestAgentShape(TestCase):

    def test_agent_shapeinput(self):

        problem = load_problem("test_problem.txt")
        self.assertEqual(list(problem.domains.keys()), [1,2])
        self.assertEqual(problem.domains[1], [5.0])
        self.assertEqual(problem.domains[2], [9.0, 10.0])
        self.assertEqual(list(problem.variables.keys()), [7, 9])
        self.assertEqual(problem.variables[7], (1, 0.5, 0.5))
        self.assertEqual(problem.variables[9], (2, 0.3, 0.3))
        self.assertEqual(problem.constraints, [(7,9,4.0)])

    def test_load_big_file(self):

        problem = load_problem("fapp05_0050.coo")
        print(problem.domains)
        print(problem.variables)
        print(problem.constraints)