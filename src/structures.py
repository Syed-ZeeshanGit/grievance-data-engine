# src/structures.py
import time
from typing import List, Dict, Any, Optional

class TicketNode:
    """
    Represents a single node inside the Priority Queue Heap structure.
    Balances Computer Science data structures with Information Systems attributes.
    """
    def __init__(self, ticket_id: int, severity: int, created_at: float, sla_hours: int):
        self.ticket_id: int = ticket_id
        self.severity: int = severity          # Scale from 1 (Low) to 5 (Critical)
        self.created_at: float = created_at    # Epoch timestamp
        self.sla_hours: int = sla_hours        # Hours allotted by service contract
        self.priority_score: float = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Applies a deterministic mathematical weight formula to calculate scheduling priority.
        Formulation: Score = (Severity * 10) + (Hours Elapsed * 1.5) - (SLA Buffer * 2.0)
        """
        hours_elapsed: float = (time.time() - self.created_at) / 3600.0
        # Simulated multiplier for testing purposes if hours_elapsed is near 0
        if hours_elapsed < 0.01:
            hours_elapsed = 0.5  # Give it a baseline mock age for instant UI feedback
            
        return (self.severity * 10.0) + (hours_elapsed * 1.5) - (self.sla_hours * 2.0)


class MaxBinaryHeapPriorityQueue:
    """
    A pure Python implementation of a Max Binary Heap Priority Queue.
    Enforces O(log n) insertion and extraction without utilizing 'heapq' or 'queue'.
    """
    def __init__(self):
        self.heap: List[TicketNode] = []

    def get_parent_index(self, index: int) -> int:
        return (index - 1) // 2

    def get_left_child_index(self, index: int) -> int:
        return (2 * index) + 1

    def get_right_child_index(self, index: int) -> int:
        return (2 * index) + 2

    def swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, node: TicketNode) -> None:
        """
        Inserts a new element into the heap and performs up-heapification.
        Time Complexity: O(log n)
        """
        self.heap.append(node)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self) -> Optional[TicketNode]:
        """
        Removes and returns the highest priority node from the root, re-balancing the heap.
        Time Complexity: O(log n)
        """
        if len(self.heap) == 0:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()

        root_node = self.heap[0]
        self.heap[0] = self.heap.pop()  # Move last element to root
        self._heapify_down(0)
        
        return root_node

    def _heapify_up(self, index: int) -> None:
        """
        Recursively moves an element up the tree structure to maintain Max-Heap invariant.
        """
        parent = self.get_parent_index(index)
        if index > 0 and self.heap[index].priority_score > self.heap[parent].priority_score:
            self.swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index: int) -> None:
        """
        Recursively pushes an element down the tree to maintain Max-Heap invariant.
        """
        max_index = index
        left = self.get_left_child_index(index)
        right = self.get_right_child_index(index)

        if left < len(self.heap) and self.heap[left].priority_score > self.heap[max_index].priority_score:
            max_index = left

        if right < len(self.heap) and self.heap[right].priority_score > self.heap[max_index].priority_score:
            max_index = right

        if index != max_index:
            self.swap(index, max_index)
            self._heapify_down(max_index)

    def get_heap_array_view(self) -> List[Dict[str, Any]]:
        """
        Serializes the heap state into a clean dictionary format for Streamlit rendering.
        """
        return [
            {
                "Position": idx,
                "Ticket ID": node.ticket_id,
                "Calculated Score": round(node.priority_score, 2),
                "Severity": node.severity
            }
            for idx, node in enumerate(self.heap)
        ]