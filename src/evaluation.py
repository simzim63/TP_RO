import numpy as np

def creer_matrice_ecarts(problem, solution):
    n_vars = max(problem.variables.keys()) + 1
    m = np.zeros((n_vars,n_vars))
    for c in problem.constraints:
        ecart = abs(solution[c[0]]-solution[c[1]])
        if ecart < c[2]:
            m[c[0]][c[1]] = max(m[c[0]][c[1]], c[2]-ecart)
    return m


def fonction_evaluation(problem, solution):
    eval_matrix = creer_matrice_ecarts(problem, solution)
    #evaluation = eval_matrix.sum()/2
    #evaluation = eval_matrix.max()
    evaluation = np.count_nonzero( eval_matrix )/2
    #evaluation = 20 * eval_matrix.max() + eval_matrix.sum() / 2 + 50 * np.count_nonzero(eval_matrix) / 2

    return (evaluation)
