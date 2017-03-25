import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
from valueSetters import *
from constants import *
from simulation import F



#need a list of list with list[0]
#as a list of number of inf users
#if only initial prop for each inf prob [0.2, 0.3, 0.4, 0.5]
def comparePropagationModels():
    x = np.array([0.2, 0.3, 0.4])
    pos = list(range(x.size))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10,5))

    foo = []
    for i in range(0,3):
        if i == 0:
            switchInitOn(True)
            switchOsnOn(False)
            switchPwOn(False)
        elif i == 1:
            switchInitOn(True)
            switchOsnOn(True)
            switchPwOn(False)
        elif i==2:
            switchInitOn(True)
            switchOsnOn(True)
            switchPwOn(True)
        #print "rishabh", x.size
        res = []
        for j in range(x.size):
            print x[j]
            setP(x[j])
            res.append(F((e_lon, e_lat)))
        foo.append(res)
    print foo

    plt.bar(pos, foo[0], width, alpha=0.5, color='#EE3224')
    plt.bar([p + width for p in pos], foo[1], width, alpha=0.5, color='#F78F1E')
    plt.bar([p + width*2 for p in pos], foo[2], width, alpha=0.5, color='#FFC222')

    ax.set_ylabel('number of influenced users')
    ax.set_xlabel('influencing probability')
    ax.set_xticks([p+ 1.5*width for p in pos])
    ax.set_xticklabels(x)

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
    switchInitOn(True)
    switchOsnOn(True)
    switchPwOn(True)
    l1 = set_init_pro()
    x = l1[0]
    xlabel = l1[1]
    l2 = set_inf_prob()
    y = l2[0]
    ylabel = l2[1]
    Z = np.zeros([x.size, y.size])
    #print Z.len
    for i in range(x.size):
        for j in range(y.size):
            setInitPro(x[i])
            setP(y[j])
            Z[i, j] = F((e_lat, e_lon))
    zlabel = 'Number of influenced users'
    surfacePlot(x, y, Z, xlabel, ylabel, zlabel, 0.01, 0.1)

def add_pro_surfacePlot():
    switchInitOn(True)
    switchOsnOn(True)
    switchPwOn(True)
    l1 = set_add_pro()
    x = l1[0]
    xlabel = l1[1]
    l2 = set_inf_prob()
    y = l2[0]
    ylabel = l2[1]

    Z = np.array((x.size, y.size))
    for i in range(x.size):
        for j in range(y.size):
            setAddPro(x[i])
            setP(y[j])
            Z[i, j] = F((e_lat, e_lon))
    zlabel = 'Number of influenced users'
    surfacePlot(x, y, Z, xlabel, ylabel, zlabel, 0.1, 0.1)

def initInfReg_surfacePlot():
    switchInitOn(True)
    switchOsnOn(True)
    switchPwOn(True)

    l1 = set_init_inf_region()
    x = l1[0]
    print 'x:: ' + x
    xlabel = l1[1]
    l2 = set_inf_prob()
    y = l2[0]
    print 'y:: ' + y
    ylabel = l2[1]
    print x.size, y.size
    Z = np.array((x.size, y.size))
    for i in range(x.size):
        for j in range(y.size):
            setInitInfReg(x[i])
            setP(y[j])
            Z[i, j] = F((e_lat, e_lon))
    zlabel = 'Number of influenced users'
    surfacePlot(x, y, Z, xlabel, ylabel, zlabel, 0.002, 0.1)

#init_pro_surfacePlot()
init_pro_surfacePlot()
