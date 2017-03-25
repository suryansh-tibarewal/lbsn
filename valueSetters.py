import numpy as np

def set_init_pro():
    res = []
    res.append(np.linspace(0.04, 0.01, 7))
    label = 'initial propagation time'
    res.append(label)
    return res

def set_add_pro():
    res = []
    res.append(np.linspace(0.4, 0.1, 7))
    label = 'additional propagation time'
    res.append(label)
    return res

def set_init_inf_region():
    res = []
    res.append(np.linspace(0.01, 0.002, 10))
    label = 'initial influence region'
    res.append(label)
    return res

def set_inf_prob():
    res = []
    res.append(np.linspace(0.2, 0.5, 7))
    label = 'influencing probability'
    res.append(label)
    return res
