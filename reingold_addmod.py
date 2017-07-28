from gen import Tree, gentree
from demo_trees import trees
from operator import lt, gt
from sys import stdout, maxint
from demo_trees import trees
from writeNodesEdges import writeObjects

minint = -maxint - 1
nodes = [0,1,2,3,4,5,6]
positions = []
edges = [(0,1),(0,4),(1,2),(1,3),(4,5),(4,6)]

class DrawTree:
    def __init__(self, tree, depth=-1):
        self.x = -1
        self.y = 2-depth
        self.tree = tree
        self.children = []
        self.thread = None
        self.mod = 0

    def left(self): 
        try:
            p = self.thread
        except:
            pass
        try:
            q = len(self.children)
        except:
            pass
        try:
            r = self.children[0]
        except:
            pass
        s = q and r
        t = p or s
        return t

    def right(self):
        try:
            p = self.thread
        except:
            pass
        try:
            q = len(self.children)
        except:
            pass
        try:
            r = self.children[-1]
        except:
            pass
        s = q and r
        t = p or s
        return t
        #return self.thread or len(self.children) and self.children[-1]

#traverse to the bottom of the tree, and place the leaves at an arbitrary
#   x coordinate
#if the node is a parent, draw its subtrees, then shift the right one as close
#   to the left as possible
#place the parent in the middle of the two trees.
def layout(tree):
    dt = reingold_tilford(tree)
    k = addmods(dt)
    #print tree, dt.x, dt.y
    return k

def addmods(tree, mod=0):
    tree.x += mod
    for c in tree.children:
        addmods(c, mod+tree.mod)
    #print tree.x, tree.y
    return tree

def reingold_tilford(tree, depth=0):
    #creating an instance/object of class DrawTree
    dt = DrawTree(tree, depth)
    
    #if node is a leaf node:
    if len(tree) == 0:
        dt.x = 0
        return dt

    #if node has one child:
    if len(tree) == 1:
        #recursing through the child node
        dt.children = [reingold_tilford(tree[0], depth+1)]
        dt.x = dt.children[0].x
        return dt
    
    #get left subtree
    left = reingold_tilford(tree[0], depth+1)
    #get right subtree
    right = reingold_tilford(tree[1], depth+1)

    dt.children = [left, right]
    dt.x = fix_subtrees(left, right)
    
    return dt

#place the right subtree as close to the left subtree as possible
def fix_subtrees(left, right):
    li, ri, diff, loffset, roffset, lo, ro \
        = contour(left, right)
    diff += 1
    diff += (right.x + diff + left.x) % 2       #stick to the integers

    right.mod = diff
    right.x += diff          
    if right.children:
        roffset += diff

    #add threads if depths of right and left sub-trees are different
    #right was deeper than left
    if ri and not li:
        lo.thread = ri
        lo.mod = roffset - loffset
    #left was deeper than right
    elif li and not ri:
        ro.thread = li
        ro.mod = loffset - roffset 

    return (left.x + right.x) / 2

#find the maximum difference between the left and right trees so that they won't conflict with each other
def contour(left, 
            right, 
            max_offset=None,
            loffset=0,
            roffset=0,
            left_outer=None, 
            right_outer=None):
    if not max_offset or (left.x + loffset) - (right.x + roffset) > max_offset:
        max_offset = left.x + loffset - (right.x + roffset)

    if not left_outer:
        left_outer = left
    if not right_outer:
        right_outer = right

    lo = left_outer.left()
    li = left.right()
    ri = right.left()
    ro = right_outer.right()

    #if children exist
    if li and ri:
        loffset += left.mod
        roffset += right.mod
        return contour(li, ri, max_offset, loffset, roffset, lo, ro)

    return li, ri, max_offset, loffset, roffset, left_outer, right_outer

def print_tree(tree_root):

    positions.append([tree_root.x, tree_root.y, 0])
    
    
    # print tree_root.tree, tree_root.x, tree_root.y #, len(tree_root.children)
    try:
        print_tree(tree_root.children[0])
    except:
        pass
    try:
        print_tree(tree_root.children[1])
    except:
        pass  

if __name__ == "__main__":
    #tree_root = layout(trees[6])
    #print_tree(tree_root)
    #print positions
    #print type(nodes[0])
    """edges= [(0,98),(78,93),(45,72),(85,86),(81,84),(48,49),(94,95),(11,22),(27,36),(76,77),(75,76),(50,69),(3,8),(53,66),(15,17),(1,2),(70,71),(46,47),(73,74),(12,16),(56,65),(82,83),(30,31),(4,7),(59,63),(89,90),(25,26),(41,42),(5,6),(28,29),(91,92),(37,38),(87,88),(32,33),(23,24),(43,44),(96,97),(60,61),(62,64),(18,19),(20,21),(79,80),(67,68),(39,40),(54,55),(13,14),(9,10),(57,58),(51,52),(34,35)]

    positions = [[0.0, -2.8284268, 0.0],[0.082579345, -2.7766757, 0.9965845],[0.0, -2.7526927, 0.0],[0.24548548, -2.727079, 0.9694003],[0.3471689, -2.7191222, 1.370939],[0.49097094, -2.717945, 1.9388005],[0.3471689, -2.7160883, 1.370939],[0.24548548, -2.7155142, 0.9694003],[0.0, -2.6882217, 0.0],[0.40169543, -2.6503966, 0.91577333],[0.0, -2.650324, 0.0],[0.67728156, -2.649928, 0.7357239],[0.77350146, -2.645441, 1.1839322],[1.0938963, -2.6448996, 1.6743329],[0.77350146, -2.6447067, 1.1839322],[0.0, -2.6420221, 0.0],[0.67728156, -2.6374552, 0.7357239],[0.87947375, -2.617894, 0.47594735],[0.67728156, -2.557129, 0.7357239],[0.9578208, -2.556631, 1.0404707],[1.1160132, -2.5407937, 0.86862797],[0.67728156, -2.5403762, 0.7357239],[0.0, -2.538051, 0.0],[0.0, -2.533691, 0.0],[0.94581723, -2.5326483, 0.32469955],[0.0, -2.5324774, 0.0],[0.9863613, -2.529513, 0.16459455],[0.9694003, -2.2702622, -0.24548547],[1.4142135, -2.26858, 1.0677015E-7],[0.9694003, -2.266858, -0.24548547],[1.3949255, -2.2638314, -0.23277196],[0.9694003, -2.2601075, -0.24548547],[1.3375876, -2.2299373, -0.45919427],[0.9694003, -2.228822, -0.24548547],[1.2437637, -2.18538, -0.6730913],[0.9694003, -2.1853619, -0.24548547],[0.0, -2.1831017, 0.0],[0.7891404, -2.157484, -0.6142128],[0.0, -2.1558454, 0.0],[0.6772814, -2.1474745, -0.7357241],[0.0, -2.1472058, 0.0],[0.0, -2.1293597, 0.0],[0.54694784, -2.127165, -0.83716667],[0.0, -2.1121926, 0.0],[0.40169495, -2.1114771, -0.9157735],[0.16459392, -2.0357466, -0.98636144],[0.34716803, -2.035296, -1.3709393],[0.16459392, -2.0171664, -0.98636144],[0.11678378, -1.8225758, -1.4093834],[0.16459392, -1.6624354, -0.98636144],[0.0, -1.6555687, 0.0],[0.0, -1.6546059, 0.0],[-0.87947404, -1.6545695, -0.47594684],[-0.47594798, -1.6538248, -0.87947345],[-0.45919514, -1.6515068, -1.3375872],[-0.16515993, -1.6512488, -1.9931687],[-0.45919514, -1.6262196, -1.3375872],[-0.45919514, -1.6256928, -1.3375872],[-0.80339193, -1.6256382, -1.8315461],[-0.45919514, -1.6254603, -1.3375872],[-0.47594798, -1.6232914, -0.87947345],[-0.9578214, -1.6227427, -1.0404701],[-0.49097192, -1.6225212, -1.9388002],[-1.0938975, -1.6221577, -1.674332],[-0.6943391, -1.6220052, -2.7418773],[-0.49097192, -1.6215656, -1.9388002],[-0.45919514, -1.6214784, -1.3375872],[-0.47594798, -1.6013469, -0.87947345],[-1.1160136, -1.6010742, -0.86862737],[-0.47594798, -1.5965437, -0.87947345],[0.0, -1.4854369, 0.0],[-0.9458175, -1.4656032, -0.32469878],[0.0, -1.4584167, 0.0],[-0.98636144, -1.371754, -0.16459376],[0.0, -1.3590088, 0.0],[0.0, -1.3507724, 0.0],[0.0, -1.2816762, 0.0],[-0.98636115, -1.2002745, 0.16459566],[0.0, -1.1819232, 0.0],[0.0, -1.1164166, 0.0],[-0.6772808, -1.1161405, 0.7357246],[0.0, -0.9092406, 0.0],[-0.7735001, -0.70299125, 1.1839331],[-0.5469472, -0.6990819, 0.83716714],[0.0, -0.6856282, 0.0],[0.0, -0.65376496, 0.0],[0.0, -0.35387707, 0.0],[-0.87947315, 0.28176475, 0.47594854],[-1.337587, 0.28313875, 0.459196],[-0.87947315, 0.28983688, 0.47594854],[-1.2437629, 0.29296112, 0.6730929],[-0.87947315, 0.29585934, 0.47594854],[-1.116012, 0.29758024, 0.8686295],[-0.87947315, 0.29917932, 0.47594854],[0.0, 0.7904966, 0.0],[0.0, 0.9381361, 0.0],[-0.0825778, 2.2957892, 0.9965846],[0.0, 2.2964826, 0.0],[0.0, 2.8284268, 0.0]]
    
    scalars =[-0.0946899,-0.0932655,-0.0926054,-0.0919004,-0.0916814,-0.091649,-0.0915979,-0.0915821,-0.0908309,-0.0897898,-0.0897878,-0.0897769,-0.0896534,-0.0896385,-0.0896332,-0.0895593,-0.0894336,-0.0888952,-0.0872227,-0.087209,-0.0867731,-0.0867616,-0.0866976,-0.0865776,-0.0865489,-0.0865442,-0.0864626,-0.079327,-0.0792807,-0.0792333,-0.07915,-0.0790475,-0.0782171,-0.0781864,-0.0769907,-0.0769902,-0.076928,-0.0762229,-0.0761778,-0.0759474,-0.07594,-0.0754488,-0.0753884,-0.0749763,-0.0749566,-0.0728722,-0.0728598,-0.0723608,-0.0670049,-0.0625972,-0.0624082,-0.0623817,-0.0623807,-0.0623602,-0.0622964,-0.0622893,-0.0616004,-0.0615859,-0.0615844,-0.0615795,-0.0615198,-0.0615047,-0.0614986,-0.0614886,-0.0614844,-0.0614723,-0.0614699,-0.0609158,-0.0609083,-0.0607836,-0.0577255,-0.0571796,-0.0569818,-0.0545965,-0.0542457,-0.054019,-0.0521172,-0.0498767,-0.0493716,-0.0475686,-0.047561,-0.0418663,-0.0361895,-0.0360819,-0.0357116,-0.0348346,-0.0265805,-0.00908512,-0.0090473,-0.00886294,-0.00877695,-0.00869718,-0.00864981,-0.0086058,0.0049172,0.00898082,0.0463488,0.0463679,0.0610091]
    """
    writeObjects(positions, edges, scalar = scalars, name= 'scalars', fileout='sushmitha_visual')
