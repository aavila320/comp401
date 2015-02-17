README

The data structure I chose to implement is a QuadTree.
The code was written in python and many different links from the Python Documentation site were used.

The following was the main site used for formatting the different strings in the code: https://docs.python.org/2/library/string.html
The Wikipedia site: http://en.wikipedia.org/wiki/Quadtree was also used extensively to gain a better understanding of what a QuadTree is.

Quadtree:
A tree data structure in which each internal node has four children. Often times a QuadTree is used in gaming to detect collisions as well as special indexing and storing data. Each number is given a body ID which is a specified identification (for those numbers that were added). 
Each QuadTree structure is broken into four different quadrants commonly called North West (NW), North East (NE), South West (SW) and South East (SE). Each quadrant is recursively divided to determine where nodes are to be placed. Once numbers are inserted, the nodes are split when their maximum capacity is reached. Child nodes are represented on the matrix in arrays.
