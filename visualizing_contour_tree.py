import networkx as nx
from writeNodesEdges import writeObjects
import sys
import csv

G=nx.Graph()
G.add_nodes_from(range(0, 110))
scalars = [0] * 110
nodeType = [0] * 110
vertexIdentifier = [0] * 110

# Storing scalar function values
with open(sys.argv[1], 'r') as csvfile:
    csvfile.readline() 
    spamreader = csv.reader(csvfile, delimiter=' ')
    for r in spamreader:
        row = r[0].split(',')
        try:
            # Store vextex index
            node_1 = int(row[6])
            node_2 = int(row[7])

            G.add_edge(node_1, node_2)

            # Store the function values for the respective indices
            scalars[node_1]= float(row[2])
            scalars[node_2]= float(row[3])
               
            # Store the type of node for the respective indices
            nodeType[node_1]= float(row[4])
            nodeType[node_2]= float(row[5])
           
            # Store the node identifier
            vertexIdentifier[node_1]= int(row[0])
            vertexIdentifier[node_2]= int(row[1])
            
        except:
        	pass

# return a dictionary of positions keyed by node
layouts = ['circular_layout',
           'random_layout',
           'shell_layout',
           'spring_layout',
           'spectral_layout',
           'fruchterman_reingold_layout']
pos = nx.fruchterman_reingold_layout(G,dim=3)

# convert to list of positions (each is a list)
xyz = [list(pos[i]) for i in pos]

writeObjects(xyz, edges=G.edges(), scalar=scalars, name='scalars', scalar2 = nodeType, name2 = 'NodeType', scalar3 = vertexIdentifier, name3 = 'VertexIdentifier', fileout='tv_108_visual')
