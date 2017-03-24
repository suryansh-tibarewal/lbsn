import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from valueSetters import *
from constants import *
from simulation import F


#need a list of list with list[0]
#as a list of number of inf users
#if only initial prop for each inf prob [0.2, 0.3, 0.4, 0.5]
def comparePropagationModels(f):
    x = np.array([0.2, 0.3, 0.4])

    pos = list(range(len(x)))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10,5))

    f = []
    for i in range(3):
        if i == 0:
            switchInitOn(True)
            switchOsnOn(False)
            switchPwOn(False)
        if i == 1:
            switchInitOn(True)
            switchOsnOn(True)
            switchPwOn(False)
        else:
            switchInitOn(True)
            switchOsnOn(True)
            switchPwOn(True)

        for j in range(x.size):
            res = []
            set_inf_prob(x[j])
            res.append(F((e_lat, e_lon)))

    f.append(res)


    plt.bar(pos, f[0], width, alpha=0.5, color='#EE3224')
    plt.bar([p + width for p in pos], f[1], width, alpha=0.5, color='#F78F1E')
    plt.bar([p + width*2 for p in pos], f[2], width, alpha=0.5, color='#FFC222')

    ax.set_ylabel('number of influenced users')
    ax.set_xlabel('influencing probability')
    ax.set_xticks([p+ 1.5*width for p in pos])
    ax.set_xtickslabels(x)

    #plt.xlim(min(pos)-width, max(pos)+width*4)
    #plt.ylim([0, 2000] )

    # Adding the legend and showing the plot
    plt.legend(['Initial only', 'Initial and OSN', 'Initial and OSN and PW'], loc='upper left')
    plt.grid()
    plt.show()

###infUsers VS init_pro VS infProb
#Z = np.array([[7 values], [7 values], [...], [...], [...], [...], [...], [...]])
###infUsers VS add_pro VS infProb
###infUsers VS initInfReg VS infProb
def surfacePlot(x, y, Z, xlabel, ylabel, zlabel, xx, yy):
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(x, y)

    ax.plot_surface(X, Y, Z, cmap=cm.jet, rstride = xx, cstride = yy)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.grid()
    plt.show()

def init_pro_surfacePlot():
    l1 = set_init_pro()
    x = l1[0]
    xlabel = l1[1]
    l2 = set_inf_prob()
    y = l2[0]
    ylabel = l2[1]

    Z = np.array((x.size, y.size))
    for i in range(x.size):
        for j in range(init_pro.size):
            setInitPro(x[i])
            setP(y[j])
            Z[i, j] = F((e_lat, e_lon))
    zlabel = 'Number of influenced users'
    surfacePlot(x, y, Z, xlabel, ylabel, zlabel)

def add_pro_surfacePlot():
    l1 = set_add_pro()
    x = l1[0]
    xlabel = l1[1]
    l2 = set_inf_prob()
    y = l2[0]
    ylabel = l2[1]

    Z = np.array((x.size, y.size))
    for i in range(x.size):
        for j in range(init_pro.size):
            setAddPro(x[i])
            setP(y[j])
            Z[i, j] = F((e_lat, e_lon))
    zlabel = 'Number of influenced users'
    surfacePlot(x, y, Z, xlabel, ylabel, zlabel)

def initInfReg_surfacePlot():
    l1 = set_init_inf_region()
    x = l1[0]
    xlabel = l1[1]
    l2 = set_inf_prob()
    y = l2[0]
    ylabel = l2[1]

    Z = np.array((x.size, y.size))
    for i in range(x.size):
        for j in range(init_pro.size):
            setInitInfReg(x[i])
            setP(y[j])
            Z[i, j] = F((e_lat, e_lon))
    zlabel = 'Number of influenced users'
    surfacePlot(x, y, Z, xlabel, ylabel, zlabel)
