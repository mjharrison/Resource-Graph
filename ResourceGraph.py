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

	def detect_cycles(self, find_all=False, override=None):
		print("Searching resource graph for cycles.")

		detection_function = self.__detect_cycles_dfs__
		if override:
			print("Overriding default cycle detection algorithm (DFS) with:", override)
			if override is "floyd":
				detection_function = self.__detect_cycles_floyd__
			else:
				print("Cycle detection algorithm", override, "not implemented")

		for node in self.processes:
			print("Searching for cycles from node", node.name)
			path_with_cycle = self.__detect_cycles_dfs__(node)
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

	def __detect_cycles_dfs__(self, root):
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
		def __floyd_step__(node):
			next_node = None
			if node in visited:
				index = visited.index(node)+1
				if index < len(visited):
					next_node = visited[index]
			return next_node

		print("Searching for cycles from node", root.name)
		visited = []
		frontier = []

		frontier.append(root)
		while frontier:
			node = frontier.pop()
			visited.append(node)
			for child in node.children:
				frontier.append(child)

		tortoise = __floyd_step__(root)
		hare = __floyd_step__(__floyd_step__(root))
		while tortoise is not hare:
			tortoise = __floyd_step__(tortoise)
			hare = __floyd_step__(__floyd_step__(hare))
		if tortoise is hare and tortoise is not None:
			return visited
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

	resource_graph.detect_cycles(override="floyd")

if __name__ == "__main__":
	main()
