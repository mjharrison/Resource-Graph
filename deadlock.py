from resourcegraph import ResourceGraph

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
	resource_graph.detect_cycles(override="floyd")

if __name__ == "__main__":
	main()
