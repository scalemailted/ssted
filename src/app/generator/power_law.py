from ..models.network import *
from ..generator.generator_utils import *

import numpy as np
import random



def powerlaw(k_min, k_max, gamma):
    y = np.random.uniform(0,1)
    return ((k_max**(-gamma+1) - k_min**(-gamma+1))*y  + k_min**(-gamma+1.0))**(1.0/(-gamma + 1.0))


def generate(nodes=100, k_min=1.0, k_max=100, gamma=3.0, isForced=False):
    degree_list = generate_degrees(powerlaw, nodes, k_min, k_max, gamma)
    edge_list = generate_edges(degree_list)
    tnet = generate_tnet(edge_list,isForced)
    return tnet

