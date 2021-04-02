import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import BSpline, make_interp_spline



"""
# temporal degree centrality (all snapshots)    #DONE (RGB)
def draw_temporal_degree_centrality(degrees):
    degree_matrix = np.array( list( degrees.values()))
    rows,cols = degree_matrix.shape
    for i in range(cols):
        unique, counts = np.unique(degree_matrix[:,i], return_counts=True)
        plt.plot(unique[1:], counts[1:], '-o')
    plt.xlabel('Degree Count')
    plt.ylabel('Number of Nodes')
    plt.title('Temporal Degree Centrality (per snapshot)')
    #plt.xlim(left=0.95)
    plt.show()
"""
"""
# temporal degree centrality (all snapshots)    #DONE (RGBA)
def draw_temporal_degree_centrality(degrees):
    degree_matrix = np.array( list( degrees.values()))
    rows,cols = degree_matrix.shape
    for i in range(cols):
        unique, counts = np.unique(degree_matrix[:,i], return_counts=True)
        a =  (i+1)/cols
        #a = 0.1 if i < cols-1 else 1
        if a <= 0.25:
            a=0.1
            color= 'gray'
        elif a <= 0.5:
            a=0.25
            color='gray'
        elif a <= 0.75:
            a=0.5
            color='gray'
        elif a <= 0.95:
            a=0.75
            color='gray'
        elif a <= 1:
            #a=1  
            color='red'
        plt.plot(unique[1:], counts[1:], '-o', color=color, alpha=a)
    plt.xlabel('Degree Count')
    plt.ylabel('Number of Nodes')
    plt.title('Temporal Degree Centrality (per snapshot)')
    #plt.xlim(left=0.95)
    plt.show()
"""
"""
# temporal degree centrality (all snapshots)    #DONE (RGBA)
def draw_temporal_degree_centrality(degrees):
    degree_matrix = np.array( list( degrees.values()))
    rows,cols = degree_matrix.shape
    for i in range(cols):
        unique, counts = np.unique(degree_matrix[:,i], return_counts=True)
        a =  (i+1)/cols
        #a = 0.1 if i < cols-1 else 1
        color = (1-a,1-a,1-a)
        if i == cols-1:
            color = 'red'
        plt.plot(unique[1:], counts[1:], '-o', color=color, alpha=a)
    plt.xlabel('Degree Count')
    plt.ylabel('Number of Nodes')
    plt.title('Temporal Degree Centrality (per snapshot)')
    #plt.xlim(left=0.95)
    plt.show()
"""

from collections import OrderedDict
from matplotlib.ticker import MaxNLocator
def draw_temporal_degree_centrality(degrees):
    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    degree_matrix = np.array( list( degrees.values()))
    rows,cols = degree_matrix.shape
    for i in range(cols):
        unique, counts = np.unique(degree_matrix[:,i], return_counts=True)
        a =  (i+1)/cols
        color = 'gray' if a < 0.75 else 'black'
        a = 0.25 if a < 0.75 else 0.5
        #color = (1-a,1-a,1-a)
        if i == cols-1:
            color = 'red'
            a = 1
        if color == 'red':
            label = 'Last snapshot (newest)'
        elif color == 'black':
            label = 'Recent (last 25%)'
        elif color == 'gray':
            label = 'Old (first 75%)'
        plt.plot(unique[1:], counts[1:], '-o', color=color, alpha=a,label=label)
    plt.xlabel('Degree Count')
    plt.ylabel('Number of Nodes')
    plt.title('Temporal Degree Centrality (per snapshot)')
    #plt.xlim(left=0.95)
    #plt.legend()
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    #plt.show()
    plt.savefig('./browser/data/temporal_degree_centrality.png')
    plt.close()

# temporal degree centrality overall    #DONE
def draw_temporal_degree_centrality_overall(degree_totals):
    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    uniques = list(set(degree_totals.values()))
    counts = [ list(degree_totals.values()).count(i) for i in uniques]
    counts = [x for _,x in sorted(zip(uniques[1:],counts[1:]))] #2021-3-5 #VALIDATE
    uniques = sorted(uniques[1:]) #2021-3-5 #VALIDATE
    plt.plot(uniques, counts, '-o') #TED This is a hack, refactor rather than cut index 0
    plt.xlabel('Degree Count')
    plt.ylabel('Number of Nodes')
    plt.title('Temporal Degree Centrality (overall totals)')
    #plt.xlim(left=0.95)
    #plt.show()
    plt.savefig('./browser/data/temporal_degree_centrality_overall.png')
    plt.close()


# topological overlap overall (per snapshot)
def draw_topological_overlap_overall(overlaps):
    x_vals = list(range(1,len(overlaps)+1))
    y_vals = overlaps
    plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Snapshots')
    plt.ylabel('Overlap % between frames')
    plt.title('Topological Overlap - Network Measure')
    #plt.show()
    plt.savefig('./browser/data/topological_overlap_overall.png')
    plt.close()

# topological overlap (node measure)
def draw_topological_overlap(overlaps):
    overlaps_matrix = np.array( list( overlaps.values()))
    plt.ylim((-.1,1.1))
    for y in overlaps_matrix:
        x = list(range(1,len(y)+1))
        plt.plot(x, y, 'or', alpha=0.05)
    plt.xlabel('Snapshots')
    plt.ylabel('Overlap % between frames')
    plt.title('Topological Overlap - Node Measure')
    #plt.show()
    plt.savefig('./browser/data/topological_overlap.png')
    plt.close()


# topological overlap average (node measure)
def draw_topological_overlap_average(overlaps_averages):
    x_vals = [0 for i in range(len(overlaps_averages))]
    y_vals = list(overlaps_averages.values())
    plt.ylim((-.1,1.1))
    plt.gca().axes.xaxis.set_visible(False)
    plt.plot(x_vals, y_vals, 'or', alpha=0.05)
    plt.xlabel('Averaged for All Snapshots')
    plt.ylabel('Overlap %')
    plt.title('Topological Overlap Average - Node Measure')
    #plt.show()
    plt.savefig('./browser/data/topological_overlap_average.png')
    plt.close()


# temporal correlation coefficient
def draw_temporal_correlation_coefficient(tcc):
    x_vals = [0,0]
    y_vals = [0,tcc]
    plt.ylim((0,1.1))
    plt.gca().axes.xaxis.set_visible(False)
    plt.bar(x_vals, y_vals)
    plt.text(-0.05, tcc+0.02, " "+str(round(tcc,3)), color='black', va='center', fontweight='bold')
    #plt.plot(x_vals, y_vals, '-r')
    plt.xlabel('Averaged across all Snapshots & Nodes')
    plt.ylabel('Overlap %')
    plt.title('Topological Overlap Average - Network Measure')
    #plt.show()
    plt.savefig('./browser/data/temporal_correlation_coefficient.png')
    plt.close()


# intercontact times - Edge Measure
# ??? How to visualize with so many edges?


# bursty coefficient - Edge Measure
# ??? How to visualize with so many edges?


# local variation - Edge Measure
# ??? How to visualize with so many edges?


# DONE
###############################################################################



def draw_temporal_degree_centrality_smooth(degrees):
    #degree_matrix = list( degrees.values() )
    degree_matrix = np.array( list( degrees.values()))
    rows,cols = degree_matrix.shape
    for i in range(cols):
        unique, counts = np.unique(degree_matrix[:,i], return_counts=True)
        x_vals = np.linspace(min(unique), max(unique),500)
        spline = make_interp_spline(unique, counts, k=3)
        y_vals = spline(x_vals)
        plt.plot(x_vals, y_vals)
    #plt.plot(unique, counts)
    #x_values = set(degree_matrix[:,0])
    #y_values = [degree_matrix[:,0].count(i) for i in x_values ]
    #plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.xlabel('Number of Nodes')
    plt.ylabel('Degree Count')
    plt.show()








def column(matrix, i):
    return [row[i] for row in matrix] 

def row(matrix, i):
    return matrix[i]



#################################################################
# Edge Analysis
from collections import defaultdict

#Complete!
def draw_icts_avg_lag(icts):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    vals = defaultdict(lambda: 0)
    for i in icts.values():
        vals[round(np.average(i),1)]+= 1
    #avg_lags = [ round(np.average(i),1) for i in icts.values()  ]
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Average tween-time (in frames)')
    plt.ylabel('Edge Count')
    plt.title('Intercontact Time - Edge Measure')
    #plt.show()
    plt.savefig('./browser/data/icts_avg_lag.png')
    plt.close()

#Complete!
def draw_icts_max_lag(icts):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    vals = defaultdict(lambda: 0)
    for i in icts.values():
        vals[max(i)]+= 1
    #max_lags = [ max(i) for i in icts.values()  ]
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Max tween-time (in frames)')
    plt.ylabel('Edge Count')
    plt.title('Intercontact Time - Edge Measure')
    #plt.show()
    plt.savefig('./browser/data/icts_max_lag.png')
    plt.close()

#Complete!
def draw_bursty_coeff(edge_coeff):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    vals = defaultdict(lambda: 0)
    for i in edge_coeff.values():
        vals[round(i,1)]+= 1
    #max_lags = [ max(i) for i in icts.values()  ]
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Bursty Coeff')
    plt.ylabel('Edge Count')
    plt.title('Bursty Coeff - Per Edge Measure')
    #plt.show()
    plt.savefig('./browser/data/bursty_coeff.png')
    plt.close()


#Complete
def draw_bursty_coeff_avg(edge_coeff):
    avg_coeff = np.average(list(edge_coeff.values()))
    x_vals = [0,1]
    y_vals = [avg_coeff,avg_coeff]
    plt.ylim((-1.1,1.1))
    plt.xlim((.1,.9))
    plt.gca().axes.xaxis.set_visible(False)
    plt.plot(x_vals, y_vals, 'r')
    plt.text(0.45, avg_coeff+0.04, " "+str(round(avg_coeff,3)), color='black', va='center', fontweight='bold')
    #plt.plot(x_vals, y_vals, '-r')
    plt.ylabel('Bursty Coeff Avg')
    plt.title('Average Bursty Coeff - Network Measure')
    #plt.show()
    plt.savefig('./browser/data/bursty_coeff_avg.png')
    plt.close()

#Complete
def draw_lvs(lvs):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    vals = defaultdict(lambda: 0)
    for i in lvs.values():
        vals[round(i,1)]+= 1
    #max_lags = [ max(i) for i in icts.values()  ]
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Local Variation')
    plt.ylabel('Edge Count')
    plt.title('Local Variations - Per Edge Measure')
    #plt.show()
    plt.savefig('./browser/data/lvs.png')
    plt.close()

#Complete
def draw_lvs_avg(lvs):
    avg_lvs = np.average(list(lvs.values()))
    x_vals = [0,1]
    y_vals = [avg_lvs,avg_lvs]
    plt.gca().axes.xaxis.set_visible(False)
    plt.plot(x_vals, y_vals, 'r')
    plt.text(0.45, avg_lvs+0.04, " "+str(round(avg_lvs,3)), color='black', va='center', fontweight='bold')
    #plt.plot(x_vals, y_vals, '-r')
    plt.ylabel('Local Variation Avg')
    plt.title('Average Local Variation - Network Measure')
    #plt.show()
    plt.savefig('./browser/data/lvs_avg.png')
    plt.close()

def draw_shortest_paths(path_data):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #set xaxis to int
    vals = defaultdict(lambda: 0)
    for key in path_data:
        delta = path_data[key]['delta'].values()
        #print( len(delta) )
        vals[len(delta)] += 1
    x_vals,y_vals = zip(*sorted(vals.items()))
    #plt.ylim((-.1,1.1))
    plt.plot(x_vals, y_vals, '-o')
    plt.xlabel('Node Reachability Score')
    plt.ylabel('Node Count')
    plt.title('Reachable Nodes')
    #plt.show()
    plt.savefig('./browser/data/shortest_paths.png')
    plt.close()

    ###########################################

#Visualizations
def draw_betweenness(betweenness):
    x_vals = [0]* len(betweenness)
    y_vals = list(betweenness.values())
    plt.ylim((-.1,1.1))
    plt.gca().axes.xaxis.set_visible(False)
    plt.plot(x_vals, y_vals, 'or', alpha=0.05)
    plt.xlabel('Temporal Betweenness Centrality')
    plt.ylabel('TBC %')
    plt.title('Temporal Betweenness Centrality - Node Measure')
    #plt.show()
    plt.savefig('./browser/data/tbc.png')
    plt.close()



def draw_closeness(closeness):
    x_vals = [0]* len(closeness)
    y_vals = list(closeness.values())
    plt.ylim((-.1,1.1))
    plt.gca().axes.xaxis.set_visible(False)
    plt.plot(x_vals, y_vals, 'or', alpha=0.05)
    plt.xlabel('Temporal Closeness Centrality')
    plt.ylabel('TCC %')
    plt.title('Temporal Closeness Centrality - Node Measure')
    #plt.show()
    plt.savefig('./browser/data/tcc.png')
    plt.close()