import sys
import os
from writeNodesEdges import writeObjects

branch_file = sys.argv[1]
file_name = os.path.splitext(os.path.basename(branch_file))[0]

branchfile = open(branch_file, 'rb')
[node_count, edge_count] = map(int, branchfile.readline().strip().split(" "))

edges = []
positions = []
scalars = []
types = []

for i in range(0, edge_count):
	edge = tuple(map(int, branchfile.readline().strip().split(" ")))
	edges.append(edge)
	
for i in range(0, node_count):
	node = branchfile.readline().strip().split(" ")
	node_index = int(node[0])
	node_position = int(node[1])
	scalar_value = float(node[2])
	node_type = int(node[3])
	node_x = float(node[4])
	node_y = float(node[5])
	node_z = float(node[6])
	
	positions.append([node_x, node_y, node_z])
	scalars.append(scalar_value)
	types.append(node_type)

writeObjects(positions, edges=edges, scalar=scalars, name='scalars', scalar2 = types, name2 = 'NodeType', fileout=file_name+'-visual')
branchfile.close()

print 'Done! :)'
