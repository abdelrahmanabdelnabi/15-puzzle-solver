from flask import Flask, render_template, send_from_directory, request, jsonify
import numpy
import json
import time
from puzzle import State, Problem, BFS, Node

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
	print request.get_json()
	data = request.get_json()
	print data['sequence']
	np_array = numpy.array(data['sequence']).reshape(4,4)
	initial_state = State(np_array)
	problem = Problem(initial_state, 4, 4)
	bfs = BFS(problem)

	start_time = time.time()
	node, result, num_explored = bfs.search()
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
		"path cost": solution_path_cost
	}

	print solution
	print jsonify(solution)
	return jsonify(solution)

if __name__ == '__main__':
  app.run(debug=True)