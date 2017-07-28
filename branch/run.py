import fileinput
import re
import os
import sys

def file_replace(fname, pat, s_after):
    # first, see if the pattern is even in the file.
    with open(fname) as f:
        if not any(re.search(pat, line) for line in f):
            return # pattern does not occur in file so we are done.

    # pattern is in the file, so perform replace operation.
    with open(fname) as f:
        out_fname = fname + ".tmp"
        out = open(out_fname, "w")
        for line in f:
            out.write(re.sub(pat, s_after, line))
        out.close()
        os.rename(out_fname, fname)

file_path = sys.argv[1]
file_basename = os.path.basename(file_path)
file_text = os.path.splitext(file_basename)
file_name = file_text[0]
file_extension = file_text[1]

file_parent = os.path.abspath(os.path.join(file_path, os.pardir))

print file_parent

file_change = 'adhitya'

file_replace('contour_tree_vtk.py', file_change, file_name)
os.system('paraview --script=contour_tree_vtk.py')

print 'java -jar recon.jar ' + file_parent + os.sep + file_name + '.rg' ' '+ file_parent + os.sep + file_name + '-graph.txt'

os.system('java -jar recon.jar ' + file_parent + os.sep + file_name + '.rg' ' '+ file_parent + os.sep + file_name + '-graph.txt')

#os.system('python demo.py '+ file_parent + os.sep + file_name + '-graph.txt')
os.system('python makeVTKfromRG.py '+ file_parent + os.sep + file_name + '-graph.txt')
file_replace('seeGraph.py', file_change, file_name+'-graph-visual')
os.system('paraview --script=seeGraph.py')

file_replace('contour_tree_vtk.py', file_name, file_change)
file_replace('seeGraph.py', file_name+'-graph-visual', file_change)
