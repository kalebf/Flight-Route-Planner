import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "flights.csv"  # Make sure this matches your file name
data = pd.read_csv(file_path)

# Display the first few rows to verify it loaded correctly
print(data.head())

# Initialize a directed graph
graph = nx.DiGraph()

# Add edges to the graph with weights (distances)
for _, row in data.iterrows():
    origin = row['Origin_airport']
    destination = row['Destination_airport']
    distance = row['Distance']  # Adjust if column name is different
    graph.add_edge(origin, destination, weight=distance)

def find_shortest_path(graph, start, end):
    try:
        path = nx.shortest_path(graph, source=start, target=end, weight='weight')
        distance = nx.shortest_path_length(graph, source=start, target=end, weight='weight')
        return path, distance
    except nx.NetworkXNoPath:
        return None, float('inf')  # No path found

def find_hubs(graph):
    in_degrees = dict(graph.in_degree())
    out_degrees = dict(graph.out_degree())
    max_in = max(in_degrees, key=in_degrees.get)
    max_out = max(out_degrees, key=out_degrees.get)
    return max_in, max_out

def find_unreachable(graph, start):
    reachable = set(nx.single_source_shortest_path_length(graph, start).keys())
    all_nodes = set(graph.nodes())
    return all_nodes - reachable
def visual():
    if len(graph.nodes()) == 0:
        print("The graph is empty. Please check your dataset.")
        return

    # Focus on the top 20 nodes for better visualization
    subgraph_nodes = list(graph.nodes())[:20]
    subgraph = graph.subgraph(subgraph_nodes)

    # Generate the layout
    pos = nx.kamada_kawai_layout(subgraph)  # Alternative layout for better clarity

    # Plot the graph
    plt.figure(figsize=(24, 16))
    nx.draw(subgraph, pos, with_labels=True, node_size=200, node_color='skyblue', font_size=10, font_weight='bold')
    labels = nx.get_edge_attributes(subgraph, 'weight')
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=labels)
    plt.title("Flight Route Subgraph")
    plt.show()


def main():
    
    while True:
        print("\nFlight Route Planning Menu")
        print("1. Find the shortest path between two airports")
        print("2. Identify hub airports")
        print("3. Find unreachable airports from a starting airport")
        print("4. View graph")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            start = input("Enter the starting airport: ").upper()
            end = input("Enter the destination airport: ").upper()
            path, distance = find_shortest_path(graph, start, end)
            if path:
                print(f"The shortest path from {start} to {end} is: {' -> '.join(path)} with a distance of {distance}")
            else:
                print(f"No path found from {start} to {end}.")
        
        elif choice == '2':
            max_in, max_out = find_hubs(graph)
            print(f"Hub with the most incoming flights: {max_in}")
            print(f"Hub with the most outgoing flights: {max_out}")
        
        elif choice == '3':
            start = input("Enter the starting airport: ").upper()
            unreachable = find_unreachable(graph, start)
            if unreachable:
                print(f"Unreachable airports from {start}: {', '.join(unreachable)}")
            else:
                print(f"All airports are reachable from {start}.")
        elif choice =='4':
            visual ()
        
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
