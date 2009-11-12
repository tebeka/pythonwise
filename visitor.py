#!/usr/bin/env python

__author__ = "Miki Tebeka <miki@mikitebeka.com>"

class Visitor:
    '''General visitor'''
    def visit(self, node):
        '''Visit a node'''
        # Find a specific visit method, default to "default"
        methname = "visit_%s" % node.__class__.__name__
        method = getattr(self, methname, self.default)

        # Call visit method on node
        method(node)

    def default(self, node):
        '''Visit node children'''
        for child in node.children:
            self.visit(child)

class Node:
    '''Tree node'''
    def __init__(self, value, children=None):
        self.value = value # Node value
        # Node children
        if children:
            self.children = children[:] # Local copy
        else:
            self.children = []

# Different types of nodes
class ANode(Node): pass
class BNode(Node): pass
class CNode(Node): pass

class Printer(Visitor):
    '''Tree printer'''
    def __init__(self):
        self.level = 0 # Current level

    def _visit(self, node, name):
        '''Visit a node'''
        print "%s%s - %s" % ("   " * self.level, name, node.value)

        # Update level and descend to children
        self.level += 1
        self.default(node)
        self.level -= 1

    # Node specific visit function
    def visit_ANode(self, node):
        self._visit(node, "A")

    def visit_BNode(self, node):
        self._visit(node, "B")

    def visit_CNode(self, node):
        self._visit(node, "C")

class Summer(Visitor):
    '''Sum up a tree'''
    def __init__(self):
        self.sum = 0 # Sum of tree

    def default(self, node):
        self.sum += node.value
        Visitor.default(self, node)

# Small demo
if __name__ == "__main__":
    # Small tree
    t = ANode(1,
            [BNode(2,
                [CNode(3)]),
             BNode(4,
                [CNode(5)])
             ])

    # Print the tree
    print "* Printing"
    v = Printer()
    v.visit(t)

    # Sum the tree
    print "* Sum"
    v = Summer()
    v.visit(t)
    print v.sum
