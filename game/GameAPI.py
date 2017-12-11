from __future__ import print_function
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from Game import Game
import threading
import sys
from random import shuffle

#TODO: implement database to store game states.

app = Flask(__name__)
CORS(app)

game_of_things = None
freshQuestion = True
currQuestion = ''
currAnswers = []

@app.route('/', methods=['GET'])
def home():
	"""
	The home page for the app. Gives instructions.
	"""
	returnDict = {}
	returnDict['title'] = "Welcome to Game of Things!"
	returnDict['startup'] = "Click on setup to initialize the game with a score limit and players."
	returnDict['question'] = "Go to /question to display a question and start collecting player responses."
	returnDict['guessing'] = "Go to /guess to guess answers with players."
	returnDict['score'] = "Go to /score to display current score."
	returnDict['points'] = "Enter in your score limit for the game in the points field (-1 for infinite)."
	returnDict['player'] = "Make a POST request with the key 'player' to add a player for /start"
	returnDict['players'] = "Enter your player names in the players field. Separate names with a comma and a space."
	returnDict['answer'] = "Make a POST request with the key 'answer' to add an answer for /question"
	returnDict['guesser'] = "Make a POST request with they key 'guesser' for the name of the current player who is guessing"
	returnDict['guessee'] = "Make a POST request with the key 'guessee' for the name of the player being guessed."
	return jsonify(returnDict)

@app.route('/add', methods=['POST'])
def addQuestion():
	"""
	Adds a question to the database.
	"""
	global game_of_things
	#dummy game just to access the questions
	game_of_things = Game(-1)
	newData = request.get_json(force=True)
	game_of_things.addQuestion(newData['question'])
	game_of_things = None
	returnDict = {}
	returnDict['success'] = 'Question added.'
	return jsonify(returnDict)

@app.route('/start', methods=['POST'])
def start():
	"""
	Initializes the game with players.
	"""
	newData = request.get_json(force=True)
	if 'points' and 'players' in newData:
		gameInitiliaze()
		return addMultiplePlayers()
	if 'points' and 'player' in newData:
		gameInitiliaze()
		return addPlayer()
	if 'points' in newData:
		return gameInitiliaze()
	if 'players' in newData:
		return addMultiplePlayers()
	if 'player' in newData:
		return addPlayer()
	returnDict = {}
	returnDict['error'] = 'Improper format. Set the points and/or players.'
	return jsonify(returnDict)

@app.route('/question', methods=['GET', 'POST'])
def question():
	"""
	Shows the question and gets player answers
	"""
	global game_of_things
	global freshQuestion
	global currQuestion
	global currAnswers
	returnDict = {}
	if game_of_things == None:
		return gameNotSet()
	if freshQuestion:
		currAnswers = []
		currQuestion = game_of_things.displayQuestion()
		freshQuestion = False
	returnDict['question'] = currQuestion
	returnDict['answers'] = currAnswers
	returnDict['players'] = game_of_things.players.keys()
	if request.method == 'POST':
		newData = request.get_json(force=True)
		if not('answer' in newData) or not('player' in newData):
			returnDict['error'] = "Improper format. Use 'answer' for an answer and 'player' for the player entering."
			return jsonify(returnDict)
		game_of_things.getPlayerAnswers(newData['player'], newData['answer'])
		currAnswers.append(newData['answer'])
		returnDict['answers'] = shuffle(currAnswers)
	return jsonify(returnDict)

@app.route('/score', methods=['GET'])
def score():
	"""
	Shows the scores of the players
	"""
	global game_of_things
	returnDict = {}
	if game_of_things == None:
		return gameNotSet()
	scores = []
	scoreDict = {}
	for name in game_of_things.players.keys():
		scores.append(str(name) + ': ' + str(game_of_things.getPlayerScore(name)))
		scoreDict[name] = int(game_of_things.getPlayerScore(name))
	winner = ''
	max = 0
	for k,v in scoreDict.iteritems():
		if v >= max:
			max = v
			winner = k
	returnDict['winner'] = winner
	returnDict['scores'] = scores
	return jsonify(returnDict)

def getScore():
	scores = []
	for name in game_of_things.players.keys():
		scores.append(str(name) + ': ' + str(game_of_things.getPlayerScore(name)))
	return scores

@app.route('/guess', methods=['GET', 'POST'])
def guess():
	"""
	Implements ability for players to guess an answer with another player.
	"""
	global game_of_things
	global currAnswers
	global freshQuestion
	returnDict = {}
	if game_of_things == None:
		return gameNotSet()
	if not(len(currAnswers) == len(game_of_things.names)):
		returnDict['error'] = 'Not everyone has answered yet.'
		return jsonify(returnDict)
	answer_json = []
	players_json = []
	for i in range(0, len(currAnswers)):
		answer_json.append({'text': currAnswers[i], 'value': currAnswers[i]})
	for i in range(0, len(game_of_things.names)):
		players_json.append({'text': game_of_things.names[i], 'value': game_of_things.names[i]})
	returnDict['answers'] = answer_json
	returnDict['players'] = players_json
	returnDict['player_names'] = game_of_things.names
	if request.method == 'POST':
		newData = request.get_json(force=True)
		if not('guesser' in newData) or not('guessee' in newData) or not('answer' in newData):
			returnDict['error'] = 'Improper format. Use "guessee", "guesser" and "answer" as your keys.'
			returnDict['scores'] = getScore()
			return jsonify(returnDict)
		if not(newData['guessee']) or not(newData['answer']):
			returnDict['error'] = 'Need to choose.'
			returnDict['scores'] = getScore()
			return jsonify(returnDict)
		if newData['guesser'] == newData['guessee']:
			returnDict['error'] = 'Cannot guess yourself.'
			returnDict['scores'] = getScore()
			return jsonify(returnDict)
		if game_of_things.checkGuess(newData['guesser'], newData['guessee'], newData['answer']):
			returnDict['status'] = 'Correct guess!'
			currAnswers = game_of_things.unassignedAnswers
			returnDict['scores'] = getScore()
			if len(currAnswers) == 1:
				freshQuestion = True
				returnDict['status'] = 'Time for a new question.'
				game_of_things.clearAnswers()
				game_of_things.resetNameArray()
				return jsonify(returnDict)
			if game_of_things.isGameOver():
				returnDict['status'] = 'Score limit reached.'
			answer_json = []
			players_json = []
			for i in range(0, len(currAnswers)):
				answer_json.append({'text': currAnswers[i], 'value': currAnswers[i]})
			for i in range(0, len(game_of_things.names)):
				players_json.append({'text': game_of_things.names[i], 'value': game_of_things.names[i]})
			returnDict['answers'] = answer_json
			returnDict['players'] = players_json
			returnDict['player_names'] = game_of_things.names
		else:
			returnDict['status'] = 'Incorrect guess.'
			returnDict['scores'] = getScore()
	return jsonify(returnDict)

def addPlayer():
	"""
	Adds a player to the game.
	"""
	global game_of_things
	returnDict = {}
	if game_of_things == None:
		return gameNotSet()
	else:
		newData = request.get_json(force=True)
		if not('player' in newData):
			returnDict['error'] = 'Improper format. Use "player" as your key for your player name.'
			return jsonify(returnDict)
		game_of_things.addPlayer(newData['player'])
		returnDict['players'] = game_of_things.names
		return jsonify(returnDict)

def addMultiplePlayers():
	"""
	Adds players to the game.
	"""
	global game_of_things
	returnDict = {}
	if game_of_things == None:
		return gameNotSet()
	else:
		newData = request.get_json(force=True)
		if not('players' in newData):
			returnDict['error'] = 'Improper format. Use "players" as your key for your player names.'
			return jsonify(returnDict)
		for name in newData['players']:
			game_of_things.addPlayer(name)
		returnDict['players'] = game_of_things.names
		return jsonify(returnDict)

def gameNotSet():
	"""
	Creates an error message for when the game has not been initialized yet.
	"""
	returnDict = {}
	returnDict['error'] = 'Score limit has not been set yet.'
	return jsonify(returnDict)

def gameInitiliaze():
	"""
	Initializes the game with number of players and score limit.
	"""
	global game_of_things
	returnDict = {}

	points = request.get_json(force=True)['points']

	try:
		points = int(points)
	except ValueError:
		returnDict['error'] = 'The points must be integers.'
		return jsonify(returnDict)
	except TypeError:
		returnDict['error'] = 'You must enter the parameters to play. Go to the home page to see instructions.'
		return jsonify(returnDict)

	game_of_things = Game(points)

	returnDict['success'] = "Game has been initialized."

	return jsonify(returnDict)


if __name__ == '__main__':
    app.run(debug=True, port=5000)