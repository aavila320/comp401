# ###################################################################
# This program will implement a QuadTree. Numbers are chosen randomly
# based on time. If nodes have been filled their children will be shown.
# 
# A QuadTree is a tree structure that is broken into four quadrants.
# It is commonly used for collision detection in 2D and 3D gaming,
# spacial indexing and storing sparse data.
# Quadrants are recursively divided into regions in a 2D space. 
# Each node has a maximum capacity that can be filled and quadrants
# are usually divided into NW,NE,SW and SE. 
# Information was also output to driver.py file
# ###################################################################


outputFileName = "driver.py"
outputFile = open( outputFileName, 'w' )
# Dictionaries for body parameters
numbers = {}
positionx = {}

# Dictionaries for node parameters
lengths = {0: None}
vertices = {0: None}
lowest_host_node = {0: None}
childnodes = {0: []}

#ID=1 because root node=0
ID = 1

# Returns new and unused ID as int
def newid(reset=False):
    global ID
    if reset:
        ID = 1
    while any(ID in maps for maps in (numbers, childnodes)):
        ID += 1
    return ID

# Initiate QuadTree and initialize lengths and vertices
def initiate(vertex, length):  
    lengths[0] = length  # Length is the side length
    vertices[0] = vertex # Vetrex is the bottom right or SW

# If node is external -> true
def isexternal(node):
    if lowest_host_node[node]:
        return True

# If node is internal -> true
def isinternal(node):
    if childnodes[node]:
        return True

# If node is empty -> returns true
def isempty(node):

    if (not lowest_host_node[node]) and (not childnodes[node]):
        return True
# This fucntion will add a body to the QuadTree.
# Body ID is an optional argument and unless unique 
# is auto generated. The number (positive int or float),
# position (tuple or list (x,y)) and childnodes are passed as
# arguments.
def addbody(number, position1, childnodes, body_id=None):
    if not body_id or body_id in numbers:
        body_id = newid()
    numbers[body_id] = number
    positionx[body_id] = position1
    connect(body_id)

# Can the node fit inside the body?
# External -> Can't Fit, another body inside
# Internal -> Cant't Fit, has child nodes
# Empty -> Can fit
# None -> Out of bounds, can't fit at all
def node_state(body, node):
    bx, by = positionx[body]
    nx, ny = vertices[node]
    l = lengths[node]
    if (0<=bx-nx<=l) and (0<=by-ny<=l):
        if isexternal(node):
            return 'EXTERNAL'
        if isinternal(node):
            return 'INTERNAL'
        return 'EMPTY'

# Splits given node (external or empty)
# Divides into four (internal) quadrants
# Rearrange -> nodes will be redistributed to appropriate childnode and
# be removed/detached from node itself
def split(node, rearrange=True):
    nx, ny = vertices[node]
    h = lengths[node] / 2
    hx, hy = nx + h, ny + h
    for vertex in ((nx,ny), (nx,hy), (hx,hy), (hx,ny)):
        node_id = newid()
        lengths[node_id] = h
        vertices[node_id] = vertex
        lowest_host_node[node_id] = None
        childnodes[node_id] = []
        childnodes[node].append(node_id)
  
    # Detach the body, distribute it to a child node (rearrange).
    if rearrange:
        body = lowest_host_node[node]
        lowest_host_node[node] = None
        for child in childnodes[node]:
            if connect(body, child):
                break

# Attaches body to host node
def connect(body, node=0):
    for node_id in generate(node):
        status = node_state(body, node_id)
        if status == 'EMPTY':
            lowest_host_node[node_id] = body
            return True
        elif status == 'EXTERNAL':
            split(node_id)
            for child in childnodes[node_id]:
                if connect(body, child):
                    return True

# Go through the QuadTree and generate node IDs
# Top =0  -> Walks through QuadTree
# Topdown -> parent node will be generated before child if True
# Gettop -> top node is yielded
def generate(top=0, topdown=True, gettop=True):
    if topdown:
        if gettop:
            yield top
            
        queue = list(childnodes[top])
        for child in queue:
            yield child
            queue.extend(childnodes[child])
    else:
        for child in childnodes[top]:
            for node in generate(child, topdown, gettop=True):
                yield node
        if gettop:
            yield top

#Called to update QuadTree
def update(node=0):
    pass

#Summary Report
def summarize(brief=False, line=False):
    # Prints QuadTree as table
    # Prints how many nodes were created and how many bodies they fit into
    def report():
        global period
        print ("----------------------------------QuadTree Status------------------------------------------")
        print ("{0} nodes were created to fit {1} body IDs in {2} seconds!"
               .format(len(childnodes), len(numbers), style[2]%period))
        outputFile.write(("----------------------------------QuadTree Status------------------------------------------"))
        outputFile.write(("{0} nodes were created to fit {1} body IDs in {2} seconds!"
               .format(len(childnodes), len(numbers), style[2]%period)))
    if brief:
        report()
        return
    
    # Styles and formats to make table neat (as neat as possoble)
    # Different styles (array) are indexed into so format can be set
    # for variables
    style = ['{:>7}', '{:>15}', '%.2f', '(%.2f, %.2f)', '{:>19}', '\x1b[0m',
             '\x1b[7m', '\x1b[0m', '{:>9}', '{:>31}']
    form1 = style[0]*2 + style[1]*1 
    form2 = style[0]*2 + style[4] + style[8] + style[9]
    head1 = ["       BODY_ID", "#", "POSITION"]
    head2 = ["      NODE_ID", "  LENGTH", "VERTEX", " LOWEST_NODE", "CHILDREN"]

# Use enumerate to return a tuple
# Print the table and the items in the table
# with correct formatting

# Prints the body IDs, the number and the positions
    print ("-------------------------------------------------------------------------------------------")
    print ("------------------------------QuadTree Matrix Report---------------------------------------") 
    print ()
    print (form1.format(*head1))
    outputFile.write(("-------------------------------------------------------------------------------------------"))
    outputFile.write(("------------------------------QuadTree Matrix Report---------------------------------------")) 
    outputFile.write(("\n"))
    outputFile.write((form1.format(*head1)))
    for i, body_id in enumerate(numbers):
        if line:
            if i % 2 == 0: space = style[6]
            else: space = style[7]
        else: space = ''
        print (space+form1.format(body_id, style[2]%numbers[body_id],
                              style[3]%positionx[body_id]))
        outputFile.write((space+form1.format(body_id, style[2]%numbers[body_id],
                              style[3]%positionx[body_id])))
# Prints the node IDs, length (based on the Bottom Right) and side lengths of the QuadTree                               
    print ()
    print (form2.format(*head2))
    for i, node_id in enumerate(childnodes):
        if line:
            if i % 2 == 0: space = style[6]
            else: space = style[7]
        else: space = ''
        print (space+form2.format(node_id, style[2]%lengths[node_id],
                              style[3]%vertices[node_id], lowest_host_node[node_id],
                              childnodes[node_id]))
        outputFile.write((space+form2.format(node_id, style[2]%lengths[node_id],
                              style[3]%vertices[node_id], lowest_host_node[node_id],
                              childnodes[node_id])))
    print ("-------------------------------------------------------------------------------------------")
    print ()
    outputFile.write(("-------------------------------------------------------------------------------------------"))
    outputFile.write(("\n"))
    
    # Report prints how many nodes were created
    # and how many body Ids they fit into. Also
    # tells us how long it took.
    report()

# Random number is chosen based on time
if __name__ == '__main__':
    from random import *
    import time

    start = time.time()

    # Initialize the QuadTree
    # Uniform sets upper and lower limits
    initiate((-5,-5), 10)
    r = range(4)
    n = (uniform(1,100) for i in r)
    p = ((uniform(-5,5),uniform(-5,5)) for i in r)
    c = ((uniform(-10,10),uniform(-10,10)) for i in r)
    
    # Add bodies
    for num, pos, child in zip(n, p, c):
        addbody(num, pos, child)

    #Update QuadTree
    update()

    period = time.time() - start
    
    # Print summary
    summarize(line=True)               
