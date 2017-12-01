"""deadlock.py
Author: Matthew James Harrison
Class: CSI-480 AI
Assignment: 2 - Deadlocks
Due Date: November 4, 2017

Description:
Stub driver showing how to use the resource graph module to detect deadlocks.

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
 - Reproduce this assignment and provide a copy to another member of academic
   staff; and/or
 - Communicate a copy of this assignment to a plagiarism checking service
   (which may then retain a copy of this assignment on its database for the
   purpose of future plagiarism checking)
"""

from resourcegraph import ResourceGraph

def main():
    resource_graph = ResourceGraph()
    resource_graph.add_node('A', ['R'], ['S'])
    resource_graph.add_node('B', [], ['T'])
    resource_graph.add_node('C', [], ['S'])
    #resource_graph.add_node('D', ['U'], ['S', 'T'])
    resource_graph.add_node('E', ['T'], ['V'])
    resource_graph.add_node('F', ['W'], ['S'])
    resource_graph.add_node('G', ['V'], ['U'])

    resource_graph.display()

    resource_graph.detect_cycles()
    resource_graph.detect_cycles(override="floyd")

if __name__ == "__main__":
    main()
