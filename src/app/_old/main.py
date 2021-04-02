from generator.generator_utils import *
from generator import power_law
from generator import gaussian
from generator import uniform
from generator import geometric
from serializer import writer

tnets = {}

tnet = power_law.generate()
evolve(tnet, 30, .5)
writer.save_json(tnet,name='powerlaw',start=0,end=30)
tnet = gaussian.generate(min=1,max=6)
evolve(tnet, 30, .5)
writer.save_json(tnet,name='gaussian',start=0,end=30)
tnet = uniform.generate(min=1,max=6)
evolve(tnet, 30, .5)
writer.save_json(tnet,name='uniform',start=0,end=30)

