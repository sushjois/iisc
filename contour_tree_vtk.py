#### import the simple module from the paraview
from paraview.simple import *
import os, csv, sys
import subprocess

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()


file_path = '/home/sushmitha/Desktop/blobdata/Data/tv_108.vtk'
parent_path = '/home/sushmitha/Desktop/blobdata/' 
file_name = os.path.splitext(os.path.basename(file_path))[0]

# create a new 'Legacy VTK Reader'
vtkFile = LegacyVTKReader(FileNames=[file_path])

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [922, 548]

# show data in view
vtkFileDisplay = Show(vtkFile, renderView1)
# trace defaults for the display properties.
vtkFileDisplay.Representation = 'Outline'

# reset view to fit data
renderView1.ResetCamera()

# create a new 'TTK ContourForests'
tTKContourForests1 = TTKContourForests(Input=vtkFile)

# Properties modified on tTKContourForests1
tTKContourForests1.ArcSampling = 0
tTKContourForests1.ArcSmoothing = 100.0

# show data in view
tTKContourForests1Display = Show(tTKContourForests1, renderView1)
# trace defaults for the display properties.
tTKContourForests1Display.Representation = 'Surface'

# hide data in view
Hide(vtkFile, renderView1)

# show data in view
tTKContourForests1Display_1 = Show(OutputPort(tTKContourForests1, 1), renderView1)
# trace defaults for the display properties.
tTKContourForests1Display_1.Representation = 'Surface'

# hide data in view
Hide(vtkFile, renderView1)

# show data in view
tTKContourForests1Display_2 = Show(OutputPort(tTKContourForests1, 2), renderView1)
# trace defaults for the display properties.
tTKContourForests1Display_2.Representation = 'Outline'

# hide data in view
Hide(vtkFile, renderView1)

# hide data in view
Hide(tTKContourForests1, renderView1)

# hide data in view
Hide(tTKContourForests1, renderView1)

# hide data in view
Hide(OutputPort(tTKContourForests1, 2), renderView1)

# set active source
SetActiveSource(tTKContourForests1)

# get active source.
tTKContourForests1_1 = GetActiveSource()

# save data
SaveData(parent_path + '/trees/' + file_name + '.vtp', proxy=OutputPort(tTKContourForests1_1, 1), DataMode='Ascii')

# get layout
layout1 = GetLayout()

# split cell
layout1.SplitVertical(0, 0.5)

# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024L
# uncomment following to set a specific view size
# spreadSheetView1.ViewSize = [400, 400]

# place view in the layout
layout1.AssignView(2, spreadSheetView1)

# show data in view
tTKContourForests1Display_3 = Show(OutputPort(tTKContourForests1, 1), spreadSheetView1)

# show data in view
tTKContourForests1Display_4 = Show(tTKContourForests1, spreadSheetView1)

# export view
nodes_file = parent_path + 'nodes-'+ file_name + '.csv'
ExportView(nodes_file, view=spreadSheetView1, FilterColumnsByVisibility=1)

# show data in view
tTKContourForests1Display_3 = Show(OutputPort(tTKContourForests1, 1), spreadSheetView1)

# export view
arcs_file = parent_path + 'arcs-'+ file_name + '.csv'
ExportView(arcs_file, view=spreadSheetView1, FilterColumnsByVisibility=1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.0, 334.60652149512316]
renderView1.CameraParallelScale = 86.60254037844386

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).


scalars = {}
nodes = []
nodeType = {}
nodeIdentifier = {}

bounds = vtkFile.GetDataInformation().GetBounds()
[x_min,x_max,y_min,y_max,z_min,z_max]=bounds

x_dim = int(x_max - x_min + 1)
y_dim = int(y_max - y_min + 1)
z_dim = int(z_max - z_min + 1)

with open(nodes_file, 'rb') as csvfile:
	csvfile.readline() 
	spamreader = csv.reader(csvfile, delimiter=' ')
	for r in spamreader:
		row = r[0].split(',')
		scalars[int(row[2])] = float(row[0])
		nodeType[int(row[2])] = int(row[3])
		nodeIdentifier[int(row[2])] = int(row[1])

with open(arcs_file, 'rb') as csvfile:
	csvfile.readline()
	spamreader = csv.reader(csvfile, delimiter=' ')
	for r in spamreader:
		row = r[0].split(',')
		x = int(row[3]) + int(abs(x_min))
		y = int(row[4]) + int(abs(y_min))
		z = int(row[5]) + int(abs(z_min))
		index = z * x_dim * y_dim + y * x_dim + x
		nodes.append(index)

with open(parent_path+'/trees/'+file_name +'.csv', 'w') as csvfile:
	fieldnames = ['Node:0', 'Node:1', 'Scalar:0', 'Scalar:1', 'Type:0' , 'Type:1' , 'Identifier:0' , 'Identifier:1']
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow(fieldnames)	
	for index in range(0,len(nodes),2):
		writer.writerow([nodes[index], nodes[index+1], scalars[nodes[index]], scalars[nodes[index+1]], nodeType[nodes[index]] , nodeType[nodes[index + 1]] , nodeIdentifier[nodes[index]] , nodeIdentifier[nodes[index + 1]]])

contour_path = parent_path +'/trees/'+ 'tree-'+ file_name + '.dot'
contour_file = open(contour_path, 'w')
contour_file.write('graph {\n')
for index in range(0,len(nodes),2):
	line = str(nodes[index]) + ' -- ' + str(nodes[index+1])
	contour_file.write(line)
	contour_file.write('\n')

contour_file.write('}')
contour_file.close()

os.remove(nodes_file)
os.remove(arcs_file)

print 'Done! :)'
os._exit(0)

