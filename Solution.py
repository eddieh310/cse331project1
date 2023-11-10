# the main modification to BFS will be:
# The objective of BFS is to find the shortest or least -weight paths in a graph,
# In the first exercise, the weight of each link was simply 1, representing the 
# standard length of a link. However, in this case, we want the algorithm to avoid
# nodes with limited bandwidth. To achieve this, we assign less weight to paths that 
# pass through nodes with higher bandwidth compared to those with lower bandwidth,
# This is because if many paths use nodes with low bandwidth, it will lead to significant
# network delays. Consequently, the weight associated with each link changes from being
# 1 to being 1 + 1/bandwidth. This modification in weight allows the BFS algorithm to 
# prioritize routes that use nodes with higher bandwidth capacity, thus optimizingroutes 
# that use nodes with higher bandwidth capacity, thus optimizing 
# the delivery of messages across the network.

from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys

class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        paths, bandwidths, priorities = {}, {}, {}
        # Note: You do not need to modify all of the above. For Problem 1, only the paths variable needs to be modified. If you do modify a variable you are not supposed to, you might notice different revenues outputted by the Driver locally since the autograder will ignore the variables not relevant for the problem.
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)
