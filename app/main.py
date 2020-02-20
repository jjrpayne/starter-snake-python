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
	
	print(head_coord["you"]["body"])
	head_coord = game_data["you"]["body"][0]
	
	directions = {"up": 0, "down": 0, "left": 0, "right": 0}

	snakes = game_data["board"]["snakes"]
	foods = game_data["board"]["food"]

	for snake in snakes:
		for coords in snakes:
			directions["up"] += abs(coords["x"] - head_coord["x"])
			directions["up"] += abs(coords["y"] - (head_coord["y"]+1))
			directions["down"] += abs(coords["x"] - head_coord["x"])
			directions["down"] += abs(coords["y"] - (head_coord["y"]-1))
			directions["left"] += abs(coords["x"] - (head_coord["x"]-1))
			directions["left"] += abs(coords["y"] - head_coord["y"])
			directions["right"] += abs(coords["x"] - (head_coord["x"]+1))
			directions["right"] += abs(coords["y"] - head_coord["y"])

	for food in foods:
		directions["up"] -= abs(food["x"] - head_coord["x"])
		directions["up"] -= abs(food["y"] - (head_coord["y"]+1))
		directions["down"] -= abs(food["x"] - head_coord["x"])
		directions["down"] -= abs(food["y"] - (head_coord["y"]-1))
		directions["left"] -= abs(food["x"] - (head_coord["x"]-1))
		directions["left"] -= abs(food["y"] - head_coord["y"])
		directions["right"] -= abs(food["x"] - (head_coord["x"]+1))
		directions["right"] -= abs(food["y"] - head_coord["y"])

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
