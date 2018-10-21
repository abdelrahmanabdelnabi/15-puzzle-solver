from collections import deque
from puzzle import Node

class QueueFrontier:

	def __init__(self):
		self._q = deque()
		self._set = set()

	def insert(self, node):
		if node.state in self._set:
			raise ValueError("a node with an identical state is already in the frontier")
		self._q.append(node)
		self._set.add(node.state)

	def pop(self):
		result = self._q.popleft()
		self._set.remove(result.state)
		return result

	def __contains__(self, item):
		if not isinstance(item, Node):
			raise ValueError("passed item is not a Node.")
		return item.state in self._set

	# for python 2. for python 3, implement __bool__() instead
	def __nonzero__(self):
		if self._set:
			return True
		return False

class StackFrontier:

	def __init__(self):
		self._s = list()
		self._set = set()

	def insert(self, node):
		if node.state in self._set:
			raise ValueError("a node with an identical state is already in the frontier")
		self._s.append(node)
		self._set.add(node.state)

	def pop(self):
		result = self._s.pop()
		self._set.remove(result.state)
		return result

	def __contains__(self, item):
		if not isinstance(item, Node):
			raise ValueError("passed item is not a Node.")
		return item.state in self._set

	# for python 2. for python 3, implement __bool__() instead
	def __nonzero__(self):
		if self._set:
			return True
		return False