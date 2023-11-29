from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys
from functools import cmp_to_key

"""
    The following function is a comparison function that takes two clients and their information
    and returns which client has higher priority.
"""
def compare_function(client1,client2,info):
    """
        Clients who are not rural always have higher priority because rural clients always pay since they have no other option.
        When 1 is returned, it means the first client has higher priority than the second, when -1 is returned, it means the second 
        client has higher priority than the first. Lastly, when 0 is returned, it means both clients have the same priority.
    """
    if not info["is_rural"][client1] and info["is_rural"][client2]:
        return 1
    elif info["is_rural"][client1] and not info["is_rural"][client2]:
        return -1
    else:
        """
            In the case where both are rural or both are not, we start comparing if they are FCC or not.
            FCC clients have higher priority than non-FCC clients because they can cause more losses to the company through demands.
        """
        if info["is_fcc"][client1] and not info["is_fcc"][client2]:
            return 1
        elif not info["is_fcc"][client1] and info["is_fcc"][client2]:
            return -1
        else:
            """
                In the case where both are FCC or both are not, we start comparing by alphas, which is the customer's tolerance before they stop paying.
                Those with lower tolerance will have higher priority, as long as the tolerance difference is significant.
            """
            if abs(info["alphas"][client1] - info["alphas"][client2]) > 0.5:
                if info["alphas"][client1] < info["alphas"][client2]:
                    return 1
                elif info["alphas"][client1] > info["alphas"][client2]: 
                    return -1
            else:
                """
                    Finally, if they have approximately the same alpha, we will compare how much each one pays, 
                    and the one who pays more will have higher priority.
                """
                if info["payments"][client1] > info["payments"][client2]:
                    return 1
                elif info["payments"][client1] < info["payments"][client2]: 
                    return -1
                else:
                    """
                        In the case where all the previous variables are equal in both clients, they will have equal priority.
                    """
                    return 0

'''
        if info["alphas"][client1] < info["alphas"][client2]:
            return 1
        elif info["alphas"][client1] > info["alphas"][client2]: 
            return -1
        else:
            return 0
'''
'''
    if element1 > element2:
        return 1
    elif element1 < element2:
        return -1
    else:
        return 0
'''
class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

    def bfs_path(self,graph, isp, list_clients, bandwidths):
        """
        The algorithm utilizes a modified BFS approach to find the shortest paths,
        taking into account bandwidth constraints from the ISP node to each client
        in the given network. The modified BFS employs a priority queue, incorporating
        a weight of 1/bandwidths[node] instead of a simple weight of 1 per node.
        This approach aims to avoid nodes with low bandwidth, prioritizing higher
        bandwidth routes for path exploration.
        """
        paths = {} # Dictionary to store paths from ISP to clients

        graph_size = len(graph)
        priors = [-1]*graph_size # List to store predecessors for path reconstruction
        search_queue = deque()
        # Now the queue used to apply the BFS has tuples of the 
        # form (Node Id,the min Length/Weight of the path that reaches this node)
        search_queue.append((isp,0))
        while search_queue:
            # Sort the search queue based on the priority (bandwidth constraint)
            search_queue = deque(sorted(search_queue,key=lambda x:x[1]))
            node,weight = search_queue.popleft()
            for neighbor in graph[node]:
                if (priors[neighbor] == -1 and neighbor != isp):
                    priors[neighbor] = node
                    # The main modification to BFS:
                    # The objective of BFS is to find the shortest or least-weight paths in a graph. 
                    # In the first exercise, the weight of each link was simply 1, representing the 
                    # standard length of a link. However, in this case, we want the algorithm to avoid
                    #  nodes with limited bandwidth. To achieve this, we assign less weight to paths that 
                    # pass through nodes with higher bandwidth compared to those with lower bandwidth. 
                    # This is because if many paths use nodes with low bandwidth, it will lead to significant 
                    # network delays. Consequently, the weight associated with each link changes from being 
                    # 1 to being 1 + 1/bandwidth. This modification in weight allows the BFS algorithm to 
                    # prioritize routes that use nodes with higher bandwidth capacity, thus optimizing 
                    # the delivery of messages across the network.
                    search_queue.append((neighbor,weight+1+1/bandwidths[node]))

        # Reconstruct paths from ISP to clients using predecessors and store them in the paths dictionary
        for client in list_clients:
            path = []
            current_node = client
            while (current_node != -1):
                path.append(current_node)
                current_node = priors[current_node]
            path = path[::-1]
            paths[client] = path

        return paths

    def calculate_priorities(self):
        """
            This function orders the clients list by priority and then create the dictionary of priorities
        """
        client_list = self.info["list_clients"]
        client_list.sort(key=cmp_to_key(lambda a, b: compare_function(a,b,self.info)))
        priorities = {}
        i = 1
        for client in client_list:
            priorities[client] = i
            i+=1
        return priorities

    def output_paths(self):
        """
        This method calculates paths, bandwidths, and priorities in the network.
        It first computes paths using the modified BFS approach that considers bandwidth constraints.
        Then, it analyzes bandwidth usage and adjusts bandwidths if certain nodes are overloaded.
        
        :return: A tuple containing paths, bandwidths, and priorities.
        """
        paths, bandwidths, priorities = {}, {}, {}

        # Retrieve bandwidth information from the provided network information.
        bandwidths = self.info['bandwidths']

        # Compute paths using the modified BFS approach that considers bandwidth constraints.
        paths = self.bfs_path(self.graph, self.isp, self.info["list_clients"],self.info['bandwidths'])

        # Initialize a dictionary to track bandwidth usage for each node.
        bandwidth_use = {node:{} for node in self.graph.keys()}

        # Analyze bandwidth usage along the computed paths.
        for client,path in paths.items():
            i = 0
            for node in path[1:-1]:
                if i in bandwidth_use[node].keys():
                    bandwidth_use[node][i] += 1
                else:
                    bandwidth_use[node][i] = 1
                i+= 1

        # Initialize a dictionary to track maximum bandwidth usage per node.
        bandwidth_use_max = {}

        # Calculate the maximum bandwidth usage for each node at the same time.
        for node,values in bandwidth_use.items():


        for key,value in self.info.items():
            print(key)

        for client in self.info["list_clients"]:



        # Adjust bandwidths for nodes that are overloaded.
        for node,value in bandwidth_use_max.items():
            #This loop iterates through each node in the network for which bandwidth 
            # constraints have been exceeded (i.e., bandwidth_use_max is greater than zero for that node).

            if bandwidth_use_max[node] > len(self.info["list_clients"]) * 0.02:
                # Here, we check if the maximum bandwidth usage at the node (as stored in 
                # bandwidth_use_max) is greater than 2% of the total number of clients in the network. 
                # In other words, we're identifying nodes where the demand for bandwidth significantly
                # exceeds the network's capacity.

                bandwidths[node] += int(bandwidth_use_max[node]*0.2)
                # When the above condition is met, we take action to alleviate the overload. We increase
                #  the available bandwidth at the node by adding an amount equal to 20% of the maximum 
                # bandwidth usage observed at that node. By doing this, we're redistributing the network'
                # s capacity more efficiently and reducing congestion in nodes where it's needed most.
        
        # This part identifies nodes that are overloaded with high bandwidth demands 
        # (more than 3% of the total clients) and increases their available bandwidth by 30%. 
        # This adjustment helps optimize network performance by ensuring that heavily used nodes 
        # have the necessary bandwidth capacity to handle the traffic.

        
        #print(sorted(bandwidth_use_max.values()))
        # paths = bfs_path(self.graph, self.isp, self.info["list_clients"])
        #simulator = Simulator()
        #simulator.run(self.graph,self.isp,self.info['list_clients'],paths,bandwidths,priorities,False)
        #print(simulator.get_delays(self.info['list_clients']))
        priorities = self.calculate_priorities()
        #bandwidths = {}
        return (paths, bandwidths, priorities)
