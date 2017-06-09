import csv, sys, os

# Store the function value for each vertex
values_1 = {}
values_2 = {}

# Store the connected vertices for each vertex
connections_1 = {}
connections_2 = {}

# Store the sum of function values for each tree
value_sum_1 = 0
value_sum_2 = 0

# Store the sum of degrees of each vertex in each tree
deg_sum_1 = 0
deg_sum_2 = 0

# Store Results
deg_difference = None
value_difference = None

# Storing scalar function values
with open(sys.argv[1], 'r') as csvfile:
    csvfile.readline() 
    spamreader = csv.reader(csvfile, delimiter=' ')
    for r in spamreader:
        row = r[0].split(',')
        try:
            # Store vextex index
            node_1 = int(row[0])
            node_2 = int(row[1])

            # Initialize Adjacency List
            if node_1 not in connections_2.keys():
                connections_2[node_1] = []
            if node_2 not in connections_2.keys():
                connections_2[node_2] = []

            # Store Adjacency List
            connections_2[node_1].append(node_2)
            connections_2[node_2].append(node_1)

            # Store the function values for the respective indices
            values_2[node_1]= float(row[2])
            values_2[node_2]= float(row[3])
        except:
        	pass
        	

# Similarly for the first tree, again
# Storing scalar function values
with open(sys.argv[2], 'r') as csvfile:
    csvfile.readline() 
    spamreader = csv.reader(csvfile, delimiter=' ')
    for r in spamreader:
        row = r[0].split(',')
        try:
			node_1 = int(row[0])
			node_2 = int(row[1])

			if node_1 not in connections_1.keys():
				connections_1[node_1] = []
			if node_2 not in connections_1.keys():
				connections_1[node_2] = []

			connections_1[node_1].append(node_2)
			connections_1[node_2].append(node_1)

			values_1[node_1]= float(row[2])
			values_1[node_2]= float(row[3])
        except:
            pass

# Iterate across the Adjacency List
for node in connections_1.keys():
    value_sum_1 += values_1[node]
    deg_sum_1 += len(connections_1[node])
  
for node in connections_2.keys():
    value_sum_2 += values_2[node]
    deg_sum_2 += len(connections_2[node])

# Store results
value_difference = round(abs(value_sum_1-value_sum_2),2)
degree_difference = abs(deg_sum_1-deg_sum_2)
    
print (value_difference, degree_difference)

os.remove(sys.argv[1])
os.remove(sys.argv[2])

print 'Done :)'
