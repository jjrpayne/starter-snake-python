import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response


@bottle.route('/')
def index():
	return '''
	Battlesnake documentation can be found at
	   <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
	'''


@bottle.route('/static/<path:path>')
def static(path):
	"""
	Given a path, return the static file located relative
	to the static folder.

	This can be used to return the snake head URL in an API response.
	"""
	return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
	"""
	A keep-alive endpoint used to prevent cloud application platforms,
	such as Heroku, from sleeping the application instance.
	"""
	return ping_response()


@bottle.post('/start')
def start():
	data = bottle.request.json

	"""
	TODO: If you intend to have a stateful snake AI,
			initialize your snake state here using the
			request's data if necessary.
	"""
	print(json.dumps(data))

	color = "#0F74F4"
	head = "pixel"
	tail = "pixel"

	return start_response((color, head, tail))


@bottle.post('/move')
def move():
	data = bottle.request.json

	"""
	TODO: Using the data from the endpoint request object, your
			snake AI must choose a direction to move in.
	"""
	game_data = json.dumps(data)
	print(game_data)
	

	#directions1 = ['up', 'down', 'left', 'right']
	#direction = random.choice(directions1)

	head_coord = data["you"]["body"][0]
	
	directions = {"up": 0, "down": 0, "left": 0, "right": 0}

	snakes = data["board"]["snakes"]
	foods = data["board"]["food"]

	# order: up, down, left, right
	min_distances = [0, 0, 0, 0]
	distances = [0, 0, 0, 0]

	# get distance of closest snake
	for snake in snakes:
		for coords in snake["body"]:
			distances[0] = abs(coords["x"] - head_coord["x"])
			distances[0] += abs(coords["y"] - (head_coord["y"]-1))
			distances[1] = abs(coords["x"] - head_coord["x"])
			distances[1] += abs(coords["y"] - (head_coord["y"]+1))
			distances[2] = abs(coords["x"] - (head_coord["x"]-1))
			distances[2] += abs(coords["y"] - head_coord["y"])
			distances[3] = abs(coords["x"] - (head_coord["x"]+1))
			distances[3] += abs(coords["y"] - head_coord["y"])

			for i in range(4):
				if(min_distances[i] == 0 or distances[i] < min_distances[i]):
					min_distances[i] = distances[i]

	directions["up"] += min_distances[0]
	directions["down"] += min_distances[1]
	directions["left"] += min_distances[2]
	directions["right"] += min_distances[3]
	
	min_distances = [0, 0, 0, 0]
	distances = [0, 0, 0, 0]

	# get distance of closest food
	for food in foods:
		distances[0] = abs(food["x"] - head_coord["x"])
		distances[0] -= abs(food["y"] - (head_coord["y"]-1))
		distances[1] = abs(food["x"] - head_coord["x"])
		distances[1] -= abs(food["y"] - (head_coord["y"]+1))
		distances[2] = abs(food["x"] - (head_coord["x"]-1))
		distances[2] -= abs(food["y"] - head_coord["y"])
		distances[3] = abs(food["x"] - (head_coord["x"]+1))
		distances[3] -= abs(food["y"] - head_coord["y"])

		for i in range(4):
			if(min_distances[i] == 0 or distances[i] < min_distances[i]):
				min_distances[i] = distances[i]

	directions["up"] -= min_distances[0]
	directions["down"] -= min_distances[1]
	directions["left"] -= min_distances[2]
	directions["right"] -= min_distances[3]

	print(directions)

	return move_response(max(directions, key=directions.get))


@bottle.post('/end')
def end():
	data = bottle.request.json

	"""
	TODO: If your snake AI was stateful,
		clean up any stateful objects here.
	"""
	print(json.dumps(data))

	return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
	bottle.run(
		application,
		host=os.getenv('IP', '0.0.0.0'),
		port=os.getenv('PORT', '8080'),
		debug=os.getenv('DEBUG', True)
	)
