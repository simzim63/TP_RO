from IPython.core.display import clear_output, display
from matplotlib import pyplot as plt
import numpy as np
from TP_RO.src.evaluation import creer_matrice_ecarts

fig = None
ax = None
ax_cout = None
ax_contraintes = None
ax_somme = None
ax_max_ecarts = None
couts = []
contraintes_non_respectees = []
somme_ecarts = []
max_ecarts = []
line_cout = None
line_contraintes = None
line_somme = None
line_max_ecarts = None
lines = {}
lines_best = {}
ax_best = None
scores_history = []
ax_pareto = None
lines_pareto = {}
count_scatter = 0
REFRESH_SCATTER = 50

def return_pareto_minimize(score_list):
    pareto = []
    dominated = []
    for scores in score_list:
        on_pareto = True
        for scores2 in score_list:
            if all (scores2 <= scores) and any (scores2 < scores):
                on_pareto = False
        if on_pareto:
            pareto.append(scores)
        else:
            dominated.append(scores)

    return pareto, dominated

def reset_drawer():
    global fig
    global ax
    global couts
    global ax_cout
    global ax_contraintes
    global contraintes_non_respectees
    global ax_somme
    global ax_max_ecarts
    global somme_ecarts
    global max_ecarts
    global line_contraintes
    global line_cout
    global line_somme
    global line_max_ecarts
    global lines
    global lines_best
    global ax_best
    global scores_history
    global ax_pareto
    global lines_pareto
    global scores_history

    fig = None
    ax = None
    ax_cout = None
    ax_contraintes = None
    couts = []
    contraintes_non_respectees = []
    ax_somme = None
    ax_max_ecarts = None
    somme_ecarts = []
    max_ecarts = []
    line_cout = None
    line_contraintes = None
    line_somme = None
    line_max_ecarts = None
    lines = {}
    lines_best = {}
    ax_best = None
    scores_history = []
    ax_pareto = None
    lines_pareto = {}

def resize_windows(has_f_eval = True):
    global ax_somme
    global ax_max_ecarts
    global ax_cout
    global ax_contraintes
    if has_f_eval:
        l = [ax_somme, ax_max_ecarts, ax_cout, ax_contraintes]
    else:
        l = [ax_somme, ax_max_ecarts, ax_contraintes]
    for i in l:
        i.relim()
        i.autoscale_view()

def initialize_ax(ax_ref, lines_ref, problem, solution):
    current_label = 0
    ax_ref.axis('off')
    for c in problem.constraints:
        antenna1 = c[0]
        antenna2 = c[1]
        ecart = c[2]
        current_label += 1

        if abs(solution[antenna1] - solution[antenna2]) < ecart:
            lines_ref[c], = ax_ref.plot([problem.variables[c[0]][1], problem.variables[c[1]][1]],
                                [problem.variables[c[0]][2], problem.variables[c[1]][2]], label=str(current_label),
                                color="red")
        else:
            lines_ref[c], = ax_ref.plot([problem.variables[c[0]][1], problem.variables[c[1]][1]],
                                [problem.variables[c[0]][2], problem.variables[c[1]][2]], label=str(current_label),
                                color="green")


def draw_solution(problem, solution, best_solution, f_eval, draw = True, end_of_exec = False):
    global fig
    global ax
    global couts
    global ax_cout
    global ax_contraintes
    global contraintes_non_respectees
    global ax_somme
    global ax_max_ecarts
    global somme_ecarts
    global max_ecarts
    global line_contraintes
    global line_cout
    global line_somme
    global line_max_ecarts
    global lines
    global lines_best
    global ax_best
    global ax_pareto
    global lines_pareto

    beginning = fig == None
    if fig is None :
        plt.ion()
        plt.show(block=False)
        fig = plt.figure(figsize=(20,10))
        if f_eval is not None:
            ax_best = fig.add_subplot(2,4,4)
            ax_contraintes = fig.add_subplot(2,4,5)
            ax_cout = fig.add_subplot(2, 4, 6)
            ax = fig.add_subplot(2, 4, 3)
            ax_somme = fig.add_subplot(2, 4, 2)
            ax_max_ecarts = fig.add_subplot(2, 4, 1)
            ax_pareto = fig.add_subplot(2, 4, 7, projection='3d')
        else:
            ax_contraintes = fig.add_subplot(2, 3, 4)
            ax = fig.add_subplot(2, 3, 3)
            ax_somme = fig.add_subplot(2, 3, 2)
            ax_max_ecarts = fig.add_subplot(2, 3, 1)
            ax_pareto = fig.add_subplot(2, 3, 5, projection='3d')
    if f_eval is not None:
        value = f_eval(problem, solution)

    m = creer_matrice_ecarts(problem, solution)
    if f_eval is not None:
        couts.append(value)
    score = np.array([np.count_nonzero(m), np.sum(m), np.max(m)])
    contraintes_non_respectees.append(score[0])
    somme_ecarts.append(score[1])
    max_ecarts.append(score[2])
    scores_history.append(score)

    if beginning:
        initialize_ax(ax, lines, problem, solution)
        if best_solution is not None:
                initialize_ax(ax_best, lines_best, problem, best_solution)
        ax.set_title("Solution courante")
        if best_solution is not None:
                ax_best.set_title("Meilleure solution")
        if f_eval is not None:
            line_cout, = ax_cout.plot(range(len(couts)), couts)
            ax_cout.set_title("Fonction évaluation")
        line_contraintes, = ax_contraintes.plot(range(len(contraintes_non_respectees)),contraintes_non_respectees)
        ax_contraintes.set_title("Nombre d'écarts non respectés")
        line_somme, = ax_somme.plot(range(len(somme_ecarts)), somme_ecarts)
        ax_somme.set_title("Somme des différences aux écarts")
        line_max_ecarts, = ax_max_ecarts.plot(range(len(max_ecarts)), max_ecarts)
        ax_max_ecarts.set_title("Maximum des différences aux écarts")
        ax_pareto.set_title("Front de Pareto (s'affiche à la fin)")
        #lines_pareto = ax_pareto.plot(2,2,3)



    else:
        for c in problem.constraints:
            antenna1 = c[0]
            antenna2 = c[1]
            ecart = c[2]
            if abs(solution[antenna1] - solution[antenna2]) < ecart:
                lines[c].set_color("red")
            else:
                lines[c].set_color("green")
            if best_solution is not None:
                if abs(best_solution[antenna1] - best_solution[antenna2]) < ecart:
                    lines_best[c].set_color("red")
                else:
                    lines_best[c].set_color("green")
        if f_eval is not None:
            line_cout.set_xdata(range(len(couts)))
            line_cout.set_ydata(couts )
        line_somme.set_xdata(range(len(somme_ecarts)))
        line_somme.set_ydata(somme_ecarts)
        line_contraintes.set_xdata(range(len(contraintes_non_respectees)))
        line_contraintes.set_ydata(contraintes_non_respectees)
        line_max_ecarts.set_xdata(range(len(max_ecarts)))
        line_max_ecarts.set_ydata(max_ecarts)

        if end_of_exec:
            pareto, dominated = return_pareto_minimize(scores_history)
            for score2 in dominated:
                ax_pareto.scatter(score2[0], score2[1], score[2], color='b')
            for score2 in pareto:
                ax_pareto.scatter(score2[0], score2[1], score[2], color='r')
        if draw:
            plt.draw()
    if draw:
        resize_windows(f_eval is not None)
        plt.pause(0.01)


