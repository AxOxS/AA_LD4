"""
Shortest Path Algorithm Module

This module provides implementations of Dijkstra's algorithm to solve the
Shortest Path problem, which is in the P complexity class.

The Shortest Path problem: Given a weighted graph, find the shortest path
from a source vertex to all other vertices.
"""
import heapq
from typing import Dict, List, Tuple, TypeVar

# Type definitions
Vertex = TypeVar('Vertex', bound=int)
Weight = TypeVar('Weight', bound=float)
Graph = Dict[Vertex, List[Tuple[Vertex, Weight]]]


def dijkstra_shortest_path(graph: Graph, start: Vertex) -> Dict[Vertex, Weight]:
    """
    Dijkstra's shortest path algorithm.
    Returns the distances from start to all other vertices.
    
    Time Complexity: O(E + V log V) where E is the number of edges and V is the number of vertices
    Space Complexity: O(V)
    
    Args:
        graph: Dictionary mapping vertex to list of (neighbor, weight) tuples
        start: Starting vertex
        
    Returns:
        Dictionary mapping each vertex to its shortest distance from start
    """
    # Initialize distances
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    
    # Priority queue
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # If we've already found a better path, skip
        if current_distance > distances[current_vertex]:
            continue
        
        # Check all neighbors
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            
            # If we found a better path, update and add to queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances 