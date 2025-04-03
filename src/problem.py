class Problem():
    def __init__(self):
        self.domains = {}
        self.variables = {}
        self.constraints = []

    def add_domain(self, label, value):
        if label in self.domains.keys():
            self.domains[label].append(value)
        else:
            self.domains[label] = [value]

    def add_variable(self, label, ref_domain, x, y):
        self.variables[label] = (ref_domain, x, y)

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def get_domain_of_variable(self, variable):
        return self.domains[self.variables[variable][0]]

def load_problem(problem_path):
    file = open(problem_path, 'r')
    problem = Problem()
    for line in file.readlines():
        a = line.split()
        if a[0] == "DM":
            problem.add_domain(int(a[1]), float(a[2]))
        elif a[0] == "TR":
            if int(a[2]) not in problem.domains.keys():
                raise Exception("The reference for the domain is not in the domain keys.")
            problem.add_variable(int(a[1]), int(a[2]), float(a[3]), float(a[4]))
        elif a[0] == "CE":
            if (int(a[1]) not in problem.variables.keys()) or (int(a[2]) not in problem.variables.keys()):
                raise Exception("One of the references of the antennas is not in the variables keys.")
            problem.add_constraint((int(a[1]), int(a[2]), float(a[3])))

    return problem