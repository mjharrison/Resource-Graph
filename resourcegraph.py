"""resourcegraph.py

Author: Matthew James Harrison
Class: CSI-480 AI
Assignment: 2 - Deadlocks
Due Date: November 4, 2017

Description:
Module for creating resource graphs and detecting deadlocks in them.

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

class Node:
    def __init__(self, name, is_process):
        self.name = name
        self.is_process = is_process
        self.children = []

    def add_child(self, child):
        """ Purpose: Add a child to the node.
        Pre: Child node
        Post: Child node added to children
        """
        self.children.append(child)

class ResourceGraph:
    def __init__(self):
        self.resources = {}
        self.processes = []

    def add_node(self, process_name, resource_names_owned, resource_names_requested):
        """ Purpose: Add a process node to the graph.
        Pre: Process name, names of owned resources, and names of requested resources
        Post: Process node created with specified connections to resources
        """
        # Create the new process and add it to the processes list
        new_process_node = Node(process_name, True)
        self.processes.append(new_process_node)

        # Create connections from owned resources to the new process
        for resource_name in resource_names_owned:
            self.__ensure_resource__(resource_name)
            self.resources[resource_name].add_child(new_process_node)

        # Create connections from the new process to its requested resources
        for resource_name in resource_names_requested:
            self.__ensure_resource__(resource_name)
            new_process_node.add_child(self.resources[resource_name])

    def detect_cycles(self, find_all=False, override=None):
        """ Purpose: Detect cycles (i.e. deadlocks) in the resource graph
        Pre: Whether or not to find all cycles (optional), name of detection algorithm (optional)
        Post: Detection results printed to console
        """
        print("Searching resource graph for cycles.")

        # Select a detection function (only DFS and Floyd are available)
        detection_function = self.__detect_cycles_dfs__
        if override:
            print("Overriding default cycle detection algorithm (DFS) with:", override)
            if override is "dfs":
                pass
            elif override is "floyd":
                detection_function = self.__detect_cycles_floyd__
            else:
                print("Cycle detection algorithm", override, "not implemented")

        # Search for cycles from each process node and then display the results
        for node in self.processes:
            print("Searching for cycles from node", node.name)
            path_with_cycle = self.__detect_cycles_dfs__(node)
            if path_with_cycle:
                print("Path with cycle:", [visited_node.name for visited_node in path_with_cycle])
                if not find_all:
                    break
            else:
                print("Search complete. No cycles detected.")

    def display(self):
        """ Purpose: Display the processes, resources, and their relations
        Pre: None
        Post: Output printed to console
        """
        # Generate a map: { Process name : list of owned resources }
        # i.e. reverse-engineer the reverse connections
        reverse_connections = {}
        for process_node in self.processes:
            reverse_connections[process_node.name] = []
        for resource_name in self.resources.keys():
            resource_node = self.resources[resource_name]
            for process_node in resource_node.children:
                reverse_connections[process_node.name].append(resource_name)

        # Display each process's name, owned resources, and requested resources
        for process_node in self.processes:
            process_name = process_node.name
            resource_names = [resource.name for resource in process_node.children]
            print(process_name, reverse_connections[process_name], resource_names)

        # Display a summary of process and resource names
        print("All processes:", [process.name for process in self.processes])
        print("All resources:", [key for key in self.resources.keys()])

    def get_process_by_name(self, name, get_all=False):
        """ Purpose: Utility function for finding processes by name
        Pre: Process name, whether or not to get a list of all matching processes (optional)
        Post: Returns process node (or list of process nodes)
        """
        search_result = None
        matches = [node for node in self.processes if node.name is name]
        if matches:
            if not find_all:
                search_result = matches[0]
            else:
                search_result = matches
        return search_result

    def __ensure_resource__(self, resource_name):
        """ Purpose: Creates a resource if it doesn't exist
        Pre: Resource name
        Post: Resource created if it doesn't exist
        """
        # If a resource does not exist, add it
        if resource_name not in self.resources:
            self.resources[resource_name] = Node(resource_name, False)

    def __detect_cycles_dfs__(self, root):
        """ Purpose: Use DFS to detect cycles
        Pre: Node to start DFS at
        Post: Returns path containing cycle, or None if no cycle exists
        """
        # Perform a depth-first search
        # A cycle is found if a node's successor already exists in the visited list
        visited = []
        frontier = []
        frontier.append(root)
        while frontier:
            node = frontier.pop()
            if node in visited:
                print("Cycle detected at node", node.name)
                visited.append(node)
                return visited
            visited.append(node)
            for child in node.children:
                frontier.append(child)
        return None

    def __detect_cycles_floyd__(self, root):
        """ Purpose: Use Floyd's algorithm to detect cycles
        Pre: Node to start DFS at
        Post: Returns path containing cycle, or None if no cycle exists
        """
        def __floyd_step__(node):
            """ Purpose: Helper function for stepping through linked list
            Pre: Current node (note: this has access to parent function's variables)
            Post: Next node or None if no additional nodes exist
            """
            next_node = None
            if node in visited:
                index = visited.index(node)+1
                if index < len(visited):
                    next_node = visited[index]
            return next_node

        # Use DFS to derive singly-linked list of visited nodes from the tree
        visited = []
        frontier = []
        frontier.append(root)
        while frontier:
            node = frontier.pop()
            visited.append(node)
            for child in node.children:
                frontier.append(child)

        # Use Floyd's algorithm to detect cycles in the visited list
        tortoise = __floyd_step__(root)
        hare = __floyd_step__(__floyd_step__(root))
        while tortoise is not hare:
            tortoise = __floyd_step__(tortoise)
            hare = __floyd_step__(__floyd_step__(hare))
        if tortoise is hare and tortoise is not None:
            print("Cycle detected at node", hare.name)
            return visited
        return None

def main():
    # Stub driver
    resource_graph = ResourceGraph()
    resource_graph.add_node('A', ['R'], ['S'])
    resource_graph.add_node('B', [], ['T'])
    resource_graph.add_node('C', [], ['S'])
    resource_graph.add_node('D', ['U'], ['S', 'T'])
    resource_graph.add_node('E', ['T'], ['V'])
    resource_graph.add_node('F', ['W'], ['S'])
    resource_graph.add_node('G', ['V'], ['U'])

    resource_graph.display()

    resource_graph.detect_cycles()
    resource_graph.detect_cycles(override="floyd")

if __name__ == "__main__":
    main()
