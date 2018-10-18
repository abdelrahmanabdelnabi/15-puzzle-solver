import itertools
from heapq import heappush, heappop, heapify

class Heap:
	def __init__(self):
		self.pq = []                         # list of entries arranged in a heap
		# self.entry_finder = {}               # mapping of tasks to entries
		# self.REMOVED = '<removed-task>'      # placeholder for a removed task
		# self.counter = itertools.count()     # unique sequence count

	# def add(self, task, priority=0):
	#     'Add a new task or update the priority of an existing task'
	#     if task in self.entry_finder:
	#         remove_task(task)
	#     count = next(self.counter)
	#     entry = [priority, count, task]
	#     self.entry_finder[task] = entry
	#     heappush(self.pq, entry)

	# def remove(self, task):
	#     'Mark an existing task as REMOVED.  Raise KeyError if not found.'
	#     entry = entry_finder.pop(task)
	#     entry[-1] = self.REMOVED

	# def pop(self):
	#     'Remove and return the lowest priority task. Raise KeyError if empty.'
	#     while self.pq:
	#         priority, count, task = heappop(self.pq)
	#         if task is not self.REMOVED:
	#             del self.entry_finder[task]
	#             return task
	#     raise KeyError('pop from an empty priority queue')

	def pop(self):
		return heappop(self.pq)

	def decrease_key(self, node, new_value):
		for idx in enumerate(pq):
			if node.state.equals(pq[idx][1].state):
				pq[idx] = (node.path_cost, node)
				heapify(pq)
				return
		raise ValueError("element not found")

	def add(self, item, priority=0):
		return heappush(self.pq, (priority, item))