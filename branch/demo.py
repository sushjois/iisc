import sys
import os
from writeNodesEdges import writeObjects

nodes = []
edges = []
positions = []
scalars = []
types = []
visited = []
connect_nodes = []
connect_node_positions = []

def get_connect_nodes(node):
	k=len(nodes)
	for j in range(0,len(edges)):
		if(node==edges[j][0] and visited[edges[j][1]]==0):
			#nodes.append(len(nodes)+k)
			#positions.append([positions[edges[j][1]][0], positions[node][1], positions[edges[j][1]][2]])
			nodes.append(k)
			positions.append([positions[edges[j][1]][0], positions[node][1], positions[edges[j][1]][2]])	
			visited[edges[j][1]] = 1
			edges.remove((edges[j][0],edges[j][1]))
			edges.append((node,nodes[k]))
			edges.append((nodes[k],edges[j][1]))
			k+=1
			get_connect_nodes(edges[j][1])
			
		elif(node==edges[j][1] and visited[edges[j][0]]==0):
			#nodes.append(len(nodes(k))
			#positions.append([positions[edges[j][0]][0], positions[node[i]][1], positions[edges[j][0]][2]])
			nodes.append(k)
			positions.append([positions[edges[j][0]][0], positions[node][1], positions[edges[j][0]][2]])	
			visited[edges[j][0]] = 1
			edges.remove((edges[j][0],edges[j][1]))
			edges.append((node,nodes[k]))
			edges.append((nodes[k],edges[j][0]))
			k+=1
			get_connect_nodes(edges[j][0])		
	return
	
#branch_file = sys.argv[1]
branch_file = '/home/sushmitha/Desktop/branch/tv_23-graph.txt'
file_name = os.path.splitext(os.path.basename(branch_file))[0]

branchfile = open(branch_file, 'rb')
[node_count, edge_count] = map(int, branchfile.readline().strip().split(" "))

visited = [0]*node_count

last_pos = branchfile.tell()

root_edge =tuple(map(int,branchfile.readline().strip().split(" ")))
print root_edge
branchfile.seek(last_pos)
visited[root_edge[0]] = 1
visited[root_edge[1]] = 1

for i in range(0, edge_count):
	edge = tuple(map(int, branchfile.readline().strip().split(" ")))
	edges.append(edge)
	
last_pos = branchfile.tell()
node = branchfile.readline().strip().split(" ")
root1_position = (float(node[4]),float(node[5]),float(node[6]))
branchfile.seek(last_pos)
	
for i in range(0, node_count-1):
	node = branchfile.readline().strip().split(" ")
	node_index = int(node[0])
	node_position = int(node[1])
	scalar_value = float(node[2])
	node_type = int(node[3])
	node_x = float(node[4])
	node_y = float(node[5])
	node_z = float(node[6])
	
	positions.append([node_x, node_y, node_z])
	nodes.append(node_index)
	scalars.append(scalar_value)
	types.append(node_type)
	
node = branchfile.readline().strip().split(" ")
node_index = int(node[0])
node_x = float(node[4])
node_y = float(node[5])
node_z = float(node[6])
root2_position = (node_x, node_y, node_z)
positions.append([node_x, node_y, node_z])
nodes.append(node_index)

main_branch = []
main_branch.append(root_edge[0])
main_branch.append(root_edge[1])

for i in range(0,len(nodes)):
	if(positions[i][0] == root1_position[0] and positions[i][2] == root1_position[2]):
		main_branch.append(nodes[i])
		visited[nodes[i]] = 1
		
for i in range(0,len(main_branch)):
	get_connect_nodes(main_branch[i])
			
print len(positions)			
#writeObjects(positions, edges=edges, scalar=scalars, name='scalars', scalar2 = types, name2 = 'NodeType', fileout=file_name+'-visual')
branchfile.close() 


	





'''for j in range(0,len(edges)):
		if(main_branch[i]==edges[j][0] and visited[edges[j][1]]==0):
			connect_nodes.append(main_branch[i])
			connect_node_positions.append([positions[edges[j][1]][0], positions[main_branch[i]][1], positions[edges[j][1]][2]])	
			visited[edges[j][1]] = 1
		elif(main_branch[i]==edges[j][1] and visited[edges[j][0]]==0):
			connect_nodes.append(main_branch[i])
			connect_node_positions.append([positions[edges[j][0]][0], positions[main_branch[i]][1], positions[edges[j][0]][2]])	
			visited[edges[j][0]] = 1'''







	
	
