class Node:
	def __init__(self, name, is_process):
		self.name = name
		self.is_process = is_process
		self.children = []

	def add_child(self, child):
		self.children.append(child)

class ResourceGraph:
	def __init__(self):
		self.resources = {}
		self.processes = []

	def add_node(self, name, resource_names_owned, resource_names_requested):
		new_process_node = Node(name, True)
		self.processes.append(new_process_node)

		for resource_name in resource_names_owned:
			self.__ensure_resource__(resource_name)
			self.resources[resource_name].add_child(new_process_node)

		for resource_name in resource_names_requested:
			self.__ensure_resource__(resource_name)
			new_process_node.add_child(self.resources[resource_name])

	def detect_cycles(self, find_all=False):
		print("Searching resource graph for cycles.")
		for node in self.processes:
			path_with_cycle = self.__detect_cycles__(node)
			if path_with_cycle:
				print("Path with cycle:", [visited_node.name for visited_node in path_with_cycle])
				if not find_all:
					break

	def display(self):
		# Generate a map: { Process name : list of owned resources }
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

	def get_process_by_name(self, name, get_all=False):
		search_result = None
		matches = [node for node in self.processes if node.name is name]
		if matches:
			if not find_all:
				search_result = matches[0]
			else:
				search_result = matches
		return search_result

	def __ensure_resource__(self, resource_name):
		if resource_name not in self.resources:
			self.resources[resource_name] = Node(resource_name, False)

	def __detect_cycles__(self, node):
		print("Searching for cycles from node", node.name)
		visited = []
		frontier = []

		frontier.append(node)
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

def main():
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

if __name__ == "__main__":
	main()
