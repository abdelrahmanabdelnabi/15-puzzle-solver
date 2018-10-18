import numpy as numpy


class State:

	def __init__(self, puzzle_matrix):
		self.puzzle_matrix = puzzle_matrix

	def equals(self, other_state):
		return numpy.array_equal(self.puzzle_matrix, other_state.puzzle_matrix)

class Problem:

	def __init__(self, initial_state, rows, cols):
		self.initial_state = initial_state
		self.rows = rows
		self.cols = cols
		self.goal_state = State(
			numpy.array([
				[1,2,3,4],
				[5,6,7,8],
				[9,10,11,12],
				[13,14,15,0]]))

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

	def add_child(self, child_node, action):
		self.children[action] = child_node
		child_node.parent = self
		child_node.action = action

	def children(self):
		return self.children

class BFS:

	def __init__(self, problem):
		self.problem = problem

	def search(self):
		node = Node(self.problem.initial_state, None, '', 0)

		if self.problem.goal_test(node.state):
			return node, "success"

		frontier_list = list()
		frontier_set = set()
		explored_set = set()

		frontier_list.append(node)
		frontier_set.add(node)

		while True:
			if not frontier_list:
				return node, "failure"

			node = frontier_list.pop(0)
			frontier_set.remove(node)

			explored_set.add(node.state)

			for action in self.problem.actions(node.state):
				child = self.child_node(self.problem, node, action)

				if child.state not in explored_set and not child.state in frontier_set:
					if self.problem.goal_test(child.state):
						return child, "success", len(explored_set)

					frontier_list.append(child)
					frontier_set.add(child)

	def child_node(self, problem, node, action):
		next_state = problem.next_state(node.state, action)
		return Node(next_state, node, action, node.path_cost + 1)