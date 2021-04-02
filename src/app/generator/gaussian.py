from ..models.network import *
from ..generator.generator_utils import *

import numpy as np
import random



def gaussian(min, max):
    return random.randint(0,max/2) + random.randint(min,max/2)


def generate(nodes=100, min=1, max=10, isForced=False):
    degree_list = generate_degrees(gaussian, nodes, min, max)
    edge_list = generate_edges(degree_list)
    tnet = generate_tnet(edge_list, isForced)
    return tnet