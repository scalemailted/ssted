#Generate Random Power Law Graphs:

Step-by-Step Instructions
[Ted Package]: app.stgpy.analysis.Powerlaw
1. Copy/paste code from python script into REPL
2. Invoke function: buildPowerlawDataset()


Node Counts
- 50 Nodes:  buildPowerlawDataset(nodes=50)
- 100 Nodes  buildPowerlawDataset(nodes=100)
- 500 Nodes  buildPowerlawDataset(nodes=500)
- 1000 Nodes buildPowerlawDataset(nodes=1000)
- 5000 Nodes buildPowerlawDataset(nodes=5000)

Temporal Mutation Probability
+ 10% Mutation
+ 20% Mutation
+ 30% Mutation
+ 40% Mutation
+ 50% Mutation

buildPowerlawDataset(nodes=50, duration=10, mutation=0.1)

##############################################################

#Temporal Network Analysis
#Temporal Evolution Dynamics

Step-by-Step Instructions
[Ted Package]: app.stgpy.analysis.Powerlaw-Analysis
1. Copy/paste code from python script into REPL
2. Invoke function: 

#Read Networks

#50 node analysis:
filenames = getFilenames('50-nodes/powerlaw-50nodes-10frames-removal-0.1',0,9)
tn = readTN(filenames)

get_shortest_paths(tn, start=0, end=9)
degrees = temporal_degree_centrality(tn)
temporal_degree_centrality_overall(degrees)
topological_overlap_overall(tn)
nodal_overlaps = topological_overlap(tn)
nodal_averages = topological_overlap_average(nodal_overlaps)
temporal_correlation_coefficient(nodal_averages)
icts = intercontact_times(tn)
bursty_coeff(icts)
local_variation(icts)
