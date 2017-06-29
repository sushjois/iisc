from gen import Tree, gentree
from demo_trees import trees
from operator import lt, gt
from sys import stdout, maxint
from demo_trees import trees
minint = -maxint - 1
nodes = []
positions = []

class DrawTree:
    def __init__(self, tree, depth=-1):
        self.x = -1
        self.y = depth
        self.tree = tree
        self.children = []
        self.thread = None
        self.mod = 0

    def left(self): 
        return self.thread or len(self.children) and self.children[0]

    def right(self):
        return self.thread or len(self.children) and self.children[-1]

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
    if not max_offset or left.x + loffset - (right.x + roffset) > max_offset:
        max_offset = left.x + loffset - (right.x + roffset)

    if not left_outer:
        left_outer = left
    if not right_outer:
        right_outer = right

    lo = left_outer.left()
    li = left.right()
    ri = right.left()
    ro = right_outer.right()

    if li and ri:
        loffset += left.mod
        roffset += right.mod
        return contour(li, ri, max_offset, loffset, roffset, lo, ro)

    return li, ri, max_offset, loffset, roffset, left_outer, right_outer

def print_tree(tree_root):
    nodes.append(tree_root.tree)
    positions.append([tree_root.x, tree_root.y, 0])
    #print tree_root.tree, tree_root.x, tree_root.y #, len(tree_root.children)
    try:
        print_tree(tree_root.children[0])
    except:
        pass
    try:
        print_tree(tree_root.children[1])
    except:
        pass  

if __name__ == "__main__":
    tree_root = layout(trees[6])
    print_tree(tree_root)
    print positions
