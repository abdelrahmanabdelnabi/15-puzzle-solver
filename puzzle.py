import numpy as numpy
from collections import deque
from heap import Heap

class State:

	def __init__(self, puzzle_matrix):
		self.puzzle_matrix = puzzle_matrix

	def __eq__(self, other):
		return self.equals(other)

	def __hash__(self):
		result = 1
		base = 1
		for i in numpy.nditer(self.puzzle_matrix):
			result += i * base
			base *= 10

		return result

	def equals(self, other_state):
		return numpy.array_equal(self.puzzle_matrix, other_state.puzzle_matrix)

class Problem:

	def __init__(self, initial_state, rows, cols):
		self.initial_state = initial_state
		self.rows = rows
		self.cols = cols
		arr = list(range(1,rows * cols))
		arr.append(0)
		self.goal_state = State(numpy.array(arr).reshape(rows, cols))

	def find_blank(self, state):
		idx = numpy.where(state.puzzle_matrix == 0)
		return idx[0][0], idx[1][0]

	# returns the possible actions available from the this state
	def actions(self, state):
		all_actions = ['up', 'down', 'left', 'right']
		x, y = self.find_blank(state)

		if x == 0:
			all_actions.remove('up')
		elif x == self.cols - 1:
			all_actions.remove('down')

		if y == 0:
			all_actions.remove('left')
		elif y == self.rows - 1:
			all_actions.remove('right')

		return all_actions


	def next_state(self, current_state, action):
		(x, y) = self.find_blank(current_state)
		next_state_matrix = numpy.copy(current_state.puzzle_matrix)

		if action == 'up':
			next_state_matrix[x][y] = next_state_matrix[x-1][y]
			next_state_matrix[x-1][y] = 0
			return State(next_state_matrix)
		if action == 'down':
			next_state_matrix[x][y] = next_state_matrix[x+1][y]
			next_state_matrix[x+1][y] = 0
			return State(next_state_matrix)
		if action == 'left':
			next_state_matrix[x][y] = next_state_matrix[x][y-1]
			next_state_matrix[x][y-1] = 0
			return State(next_state_matrix)
		if action == 'right':
			next_state_matrix[x][y] = next_state_matrix[x][y+1]
			next_state_matrix[x][y+1] = 0
			return State(next_state_matrix)

		raise ValueError('unkown action.')

	def goal_test(self, state):
		return self.goal_state.equals(state)

class Node:
	def __init__(self, state, parent, action, path_cost):
		self.state = state
		self.children = dict()
		self.parent = parent
		self.action = action
		self.path_cost = path_cost

# def __eq__(self, other):
#   if isinstance(other, self.__class__):
#    	return self.state.equals(other.state)

# def __hash__(self):
# 		return hash(self.state)

	def add_child(self, child_node, action):
		self.children[action] = child_node
		child_node.parent = self
		child_node.action = action

	def children(self):
		return self.children

class Solver:

	def __init__(self, problem):
		self.problem = problem

	def BFS(self):
		node = Node(self.problem.initial_state, None, '', 0)

		if self.problem.goal_test(node.state):
			return node, "success", 0

		frontier_list = deque()
		frontier_set = set()
		explored_set = set()

		frontier_list.append(node)
		frontier_set.add(node)

		while True:
			if not frontier_list:
				return node, "failure"

			node = frontier_list.popleft()
			frontier_set.remove(node)

			explored_set.add(node.state)

			for action in self.problem.actions(node.state):
				child = self.child_node(self.problem, node, action)

				if child.state not in explored_set and not child.state in frontier_set:
					if self.problem.goal_test(child.state):
						return child, "success", len(explored_set)

					frontier_list.append(child)
					frontier_set.add(child)

	def DFS(self):
		node = Node(self.problem.initial_state, None, '', 0)

		if self.problem.goal_test(node.state):
			return node, "success", 0

		frontier_list = list()
		frontier_set = set()
		explored_set = set()

		frontier_list.append(node)
		frontier_set.add(node.state)

		while True:
			if not frontier_list:
				return node, "failure", len(explored_set)

			node = frontier_list.pop()
			frontier_set.remove(node.state)

			explored_set.add(node.state)

			for action in self.problem.actions(node.state):
				child = self.child_node(self.problem, node, action)

				if child.state not in explored_set and not child.state in frontier_set:
					if self.problem.goal_test(child.state):
						return child, "success", len(explored_set)

					frontier_list.append(child)
					frontier_set.add(child.state)

	def AStar(self):
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
				child = self.child_node_manhattan(self.problem, node, action)

				if child.state not in explored_set and child.state not in frontier_set:
					frontier_heap.add(child, priority=child.path_cost)
					frontier_set[child.state] = child.path_cost
				elif child.state in frontier_set:
					prev_cost = frontier_set[child.state]

					if prev_cost > child.path_cost:
						frontier_heap.decrease_key(child, child.path_cost)

	def child_node(self, problem, node, action):
		next_state = problem.next_state(node.state, action)
		return Node(next_state, node, action, node.path_cost + 1)

	def child_node_manhattan(self, problem, node, action):
		next_state = problem.next_state(node.state, action)
		return Node(next_state, node, action, node.path_cost + manhattan_distance(next_state))

def manhattan_distance(state):
	matrix = state.puzzle_matrix
	result = 0

	rows = matrix.shape[0]	
	cols = matrix.shape[1]

	for i in range(rows):
		for j in range(cols):
			val = matrix[i][j]
			if val == 0:
				expected_col = cols
				expected_row = rows
			else:
				expected_row = (val - 1) // cols
				expected_col = (val - 1) % cols
			
			result += abs(expected_row - i) + abs(expected_col - j)
	
	return result

