from puzzle import Problem, Node, State
from heap import Heap
from math import sqrt
from frontier import QueueFrontier, StackFrontier
import time

class Solver:

	def __init__(self, problem):
		self.problem = problem

	def _graph_search(self, frontier):
		node = Node(self.problem.initial_state, None, '', 0)

		if self.problem.goal_test(node.state):
			return node, "success", 0

		explored_set = set()

		frontier.insert(node)

		while True:
			if not frontier:
				return node, "failure", len(explored_set)

			node = frontier.pop()
			explored_set.add(node.state)

			for action in self.problem.actions(node.state):
				child = self.child_node(self.problem, node, action)

				if child.state not in explored_set and not child in frontier:
					if self.problem.goal_test(child.state):
						return child, "success", len(explored_set)

					frontier.insert(child)

	def BFS(self):
		return self._search(lambda: self._graph_search(QueueFrontier()))

	def DFS(self):
		return self._search(lambda: self._graph_search(StackFrontier()))

	def AStar(self, distance_type):
		return self._search(lambda: self._AStar(distance_type))

	def _AStar(self, distance_type):
		node = Node(self.problem.initial_state, None, '', 0)

		if self.problem.goal_test(node.state):
			return node, "success", 0

		frontier_heap = Heap()
		frontier_set = dict() # key: state, value: cost
		explored_set = set()

		frontier_heap.add(node, priority=node.path_cost)
		frontier_set[node.state] = node.path_cost

		while True:
			if not frontier_heap.pq:
				return node, "failure", len(explored_set)

			cost, node = frontier_heap.pop()
			frontier_set.pop(node.state, None)

			if self.problem.goal_test(node.state):
				return node, "success", len(explored_set)

			explored_set.add(node.state)

			for action in self.problem.actions(node.state):
				# child = self.child_node_manhattan(self.problem, node, action)
				child = self.child_node(self.problem, node, action)

				if child.state not in explored_set and child.state not in frontier_set:
					# frontier_heap.add(child, priority=child.path_cost)
					child_path_to_goal = distance(child.state, distance_type)
					child_total_path = child.path_cost + child_path_to_goal

					frontier_heap.add(child, priority=child_total_path)
					frontier_set[child.state] = child_total_path
				elif child.state in frontier_set:
					prev_cost = frontier_set[child.state]

					child_path_to_goal = distance(child.state, distance_type)
					child_total_path = child.path_cost + child_path_to_goal

					# if prev_cost > child.path_cost:
					if prev_cost > child_total_path:
						# frontier_heap.decrease_key(child, child.path_cost)
						frontier_heap.decrease_key(child, child_total_path)

	def child_node(self, problem, node, action):
		next_state = problem.next_state(node.state, action)
		return Node(next_state, node, action, node.path_cost + 1)

	def _search(self, agent):
		start_time = time.time()
		node, result, num_explored = agent()
		running_time = round(time.time() - start_time, 5)

		steps = list()
		if result == 'success':
			while node.parent != None:
				steps.append(node.action)
				node = node.parent

			steps.reverse()

		return result, num_explored, steps, running_time

def distance(state, type):
	matrix = state.puzzle_matrix
	result = 0

	rows = matrix.shape[0]
	cols = matrix.shape[1]

	for i in range(rows):
		for j in range(cols):
			val = matrix[i][j]
			if val != 0:
				expected_row = val // cols
				expected_col = val % cols

				if type == 1:
					result += abs(expected_row - i) + abs(expected_col - j)
				elif type == 2:
					result += sqrt(pow((expected_row - i), 2) + pow((expected_col - j), 2))

	return result
