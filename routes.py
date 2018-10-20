from flask import Flask, render_template, send_from_directory, request, jsonify
import numpy
import json
import time
import math

from puzzle import State, Problem, Solver, Node

app = Flask(__name__)

@app.route('/')
def home():
  return send_from_directory('templates', 'index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/solve', methods=['POST'])
def solve():
	print(request.get_json())
	data = request.get_json()
	sequence = data['sequence']
	strategy = data['strategy']
	if is_square(len(sequence)):
		sqrt = int(math.sqrt(len(sequence)))
		np_array = numpy.array(sequence).reshape(sqrt,sqrt)
	initial_state = State(np_array)
	problem = Problem(initial_state, sqrt, sqrt)
	solver = Solver(problem)

	start_time = time.time()

	if strategy == 'A* Manhattan Distance':
		node, result, num_explored = solver.AStar(1)
	elif strategy == 'A* - Euclidean Distance':
		node, result, num_explored = solver.AStar(2)
	elif strategy == 'BFS':
		node, result, num_explored = solver.BFS()
	elif strategy == 'DFS':
		node, result, num_explored = solver.DFS()

	running_time = round(time.time() - start_time, 5)

	solution_path_cost = node.path_cost

	steps = list()

	while node.parent != None:
		steps.append(node.action)
		node = node.parent

	steps.reverse()

	solution = {
		"steps": steps,
		"nodes explored": num_explored,
		"running time": running_time,
		"path cost": len(steps)
	}

	print(solution)
	print(jsonify(solution))
	return jsonify(solution)


def is_square(integer):
    root = math.sqrt(integer)
    if int(root + 0.5) ** 2 == integer:
        return True
    else:
        return False

if __name__ == '__main__':
  app.run(debug=True)
