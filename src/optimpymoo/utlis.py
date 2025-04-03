import numpy as np

from src.drawer import reset_drawer, draw_solution
from src.evaluation import creer_matrice_ecarts
from pymoo.visualization.scatter import Scatter



def freq_from_index(problem, X):
    return [problem.get_domain_of_variable(ii)[jj] for ii,jj in enumerate(X)]

def interface_pymoo(problem):
    n_var = len(problem.variables)
    xl = np.zeros(len(problem.variables))
    xu= np.array([len(problem.get_domain_of_variable(ii))-1 for ii in range(len(problem.variables))])
    return n_var, xl, xu


def identify_pareto(scores, minimize=True):
    if minimize:
        scores = -scores        
    # Count number of items
    population_size = scores.shape[0]
    # Create a NumPy index for scores on the pareto front (zero indexed)
    population_ids = np.arange(population_size)
    # Create a starting list of items on the Pareto front
    # All items start off as being labelled as on the Parteo front
    pareto_front = np.ones(population_size, dtype=bool)
    # Loop through each item. This will then be compared with all other items
    for i in range(population_size):
        # Loop through all other items
        for j in range(population_size):
            # Check if our 'i' pint is dominated by out 'j' point
            if all(scores[j] >= scores[i]) and any(scores[j] > scores[i]):
                # j dominates i. Label 'i' point as not on Pareto front
                pareto_front[i] = 0
                # Stop further comparisons with 'i' (no more comparisons needed)
                break
    # Return ids of scenarios on pareto front
    return population_ids[pareto_front]

def solution_freq(problem, X):
    pred = freq_from_index(problem,np.round(X).astype(int))
    pred = {v: k for v, k in enumerate(pred)}
    return pred

def multiobjectivescores(problem, pred):
    eval_matrix = creer_matrice_ecarts(problem, pred)
    f1 = eval_matrix.sum()
    f2 = eval_matrix.max()
    f3 = np.count_nonzero( eval_matrix)
    return [f1, f2, f3]

def affichPareto(problem, result, algo:str):
    plot = Scatter(angle=(10, 140))
    if algo=="PSO":
        sol =[]
        for algorithm in result.history:
            pred = solution_freq(problem, np.round(algorithm.opt.get("X").astype(int)[0]))
            score = np.array(multiobjectivescores(problem, pred))
            plot.add(score, color='b', alpha=0.1)
            sol.append(score)
        plot.add(np.array(sol)[identify_pareto(np.array(sol))],color='r')
        plot.show()
        return plot
    elif algo=="NSGA2":
        for algorithm in result.history:
            plot.add(algorithm.opt.get("F"), color='b', alpha=0.1)
        plot.add(algorithm.opt.get("F")[identify_pareto(algorithm.opt.get("F"))], color='r')
        plot.show()
        return plot

def drawhistory(problem, result, f_eval, algo:str):
    if algo=="PSO":
        reset_drawer()
        best_score = None
        best_solution = None
        for algorithm in result.history:
            pred = solution_freq(problem, np.round(algorithm.opt.get("X").astype(int)[0]))
            score = f_eval(problem, pred)
            if best_score is None or score < best_score:
                best_score = score
                best_solution = pred.copy()
            draw_solution(problem, pred, best_solution, f_eval, draw = (algorithm == result.history[-1]), end_of_exec= (algorithm == result.history[-1]))
    elif algo=="NSGA2":
        reset_drawer()
        for algorithm in result.history:
            for pred in algorithm.opt.get("X"):
                pred2 = solution_freq(problem, np.round(pred).astype(int))
                end = ((algorithm is result.history[-1]) and all(pred == algorithm.opt.get("X")[-1]))
                draw_solution(problem, pred2, best_solution = None, f_eval = None, draw = end, end_of_exec=end)
