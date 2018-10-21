import numpy as numpy


class State:

	def __init__(self, puzzle_matrix):
		self.puzzle_matrix = puzzle_matrix

	def __eq__(self, other):
		return self.equals(other)

	def __hash__(self):
		result = 0
		base = 1
		for i in numpy.nditer(self.puzzle_matrix):
			result += int(i) * base
			base *= 10
			base = min(base, 1e9)
			result %= 1000000007

		#return result
		return int(result) % 1000000007

	def equals(self, other_state):
		return numpy.array_equal(self.puzzle_matrix, other_state.puzzle_matrix)

class Problem:

	def __init__(self, initial_state, rows, cols):
		self.initial_state = initial_state
		self.rows = rows
		self.cols = cols
		arr = list(range(0, rows * cols))
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

		raise ValueError('unknown action.')

	def goal_test(self, state):
		return self.goal_state.equals(state)

class Node:
	def __init__(self, state, parent, action, path_cost):
		self.state = state
		self.children = dict()
		self.parent = parent
		self.action = action
		self.path_cost = path_cost

	def __lt__(self, other):
		return self.path_cost < other.path_cost

	def add_child(self, child_node, action):
		self.children[action] = child_node
		child_node.parent = self
		child_node.action = action

	def children(self):
		return self.children
