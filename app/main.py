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

	you = data["you"]
	body = you["body"]
	head = body[0]
	
	directions = {"up": 0, "down": 0, "left": 0, "right": 0}

	snakes = data["board"]["snakes"]
	foods = data["board"]["food"]

	# get avg distance of closest snake to each direction
	min_distances = [0, 0, 0, 0]
	# order: up, down, left, right
	for snake in snakes:
		# make sure snake is not you
		if(snake["id"] != you["id"]):
			distances = [0, 0, 0, 0]
			for coords in snake["body"]:
				distances[0] = abs(coords["x"] - head["x"])
				distances[0] += abs(coords["y"] - (head["y"]-1))
				distances[1] = abs(coords["x"] - head["x"])
				distances[1] += abs(coords["y"] - (head["y"]+1))
				distances[2] = abs(coords["x"] - (head["x"]-1))
				distances[2] += abs(coords["y"] - head["y"])
				distances[3] = abs(coords["x"] - (head["x"]+1))
				distances[3] += abs(coords["y"] - head["y"])
		
			distances /= len(snake["body"])

			for i in range(4):
				if(min_distances[i] == 0 or distances[i] < min_distances[i]):
					min_distances[i] = distances[i]

	directions["up"] += min_distances[0]
	directions["down"] += min_distances[1]
	directions["left"] += min_distances[2]
	directions["right"] += min_distances[3]
	
	min_distances = [0, 0, 0, 0]

	# get distance of closest food
	for food in foods:
		distances = [0, 0, 0, 0]
		distances[0] = abs(food["x"] - head["x"])
		distances[0] += abs(food["y"] - (head["y"]-1))
		distances[1] = abs(food["x"] - head["x"])
		distances[1] += abs(food["y"] - (head["y"]+1))
		distances[2] = abs(food["x"] - (head["x"]-1))
		distances[2] += abs(food["y"] - head["y"])
		distances[3] = abs(food["x"] - (head["x"]+1))
		distances[3] += abs(food["y"] - head["y"])

		for i in range(4):
			if(min_distances[i] == 0 or distances[i] < min_distances[i]):
				min_distances[i] = distances[i]

	directions["up"] -= min_distances[0]
	directions["down"] -= min_distances[1]
	directions["left"] -= min_distances[2]
	directions["right"] -= min_distances[3]

	print(directions)

	# stop snake from eating itself
	current_movement = max(directions, key=directions.get)
	for seg in body:
		if(current_movement == "up" and seg["x"] == head["x"] and seg["y"] == head["y"]-1):
			if(current_movement in directions):
				del directions[current_movement]
				current_movement = max(directions, key=directions.get)
		if(current_movement == "down" and seg["x"] == head["x"] and seg["y"] == head["y"]+1)
			if(current_movement in directions):
				del directions[current_movement]	
				current_movement = max(directions, key=directions.get)
		if(current_movement == "left" and seg["x"] == head["x"]-1 and seg["y"] == head["y"])
			if(current_movement in directions):
				del directions[current_movement]	
				current_movement = max(directions, key=directions.get)
		if(current_movement == "right" and seg["x"] == head["x"]+1 and seg["y"] == head["y"])
			if(current_movement in directions):
				del directions[current_movement]	
				current_movement = max(directions, key=directions.get)
		if len(directions) <= 1:
		# either snake is trapped, or there is only one viable direction
		# in either case, there is no point in checking any more segments
			break

	return move_response(current_movement)


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
