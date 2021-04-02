from ..models.network import *
from ..generator.generator_utils import *

import numpy as np
import random



def uniform(min, max):
    return random.randint(min,max)


def generate(nodes=100, min=1, max=4, isForced=False):
    degree_list = generate_degrees(uniform, nodes, min, max)
    edge_list = generate_edges(degree_list)
    tnet = generate_tnet(edge_list, isForced)
    return tnet