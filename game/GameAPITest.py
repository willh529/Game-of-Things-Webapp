from GameAPI import app
import json
import unittest
from flask import jsonify

class GameAPITests(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True 

	def testHome(self):
		response = self.app.get('/')
		self.assertTrue('Game of Things' in response.data)

	def testNotIntegerForPoints(self):
		response = self.app.post('/start', data=json.dumps({"points": "text"}))
		json2 = response.data
		self.assertTrue('"error"' in json2)

	def testSetPoints(self):
		response = self.app.post('/start', data=json.dumps({"points": -1}))
		json2 = response.data
		self.assertTrue('"success"' in json2)

	def testAddPlayer(self):
		self.app.post('/start', data=json.dumps({"points": -1}))
		response = self.app.post('/start', data=json.dumps({"player": "Mario"}))
		json2 = response.data
		self.assertTrue('"players"' in json2)
		self.assertTrue('"Mario"' in json2)

	def testAddPlayers(self):
		self.app.post('/start', data=json.dumps({"points": -1}))
		response = self.app.post('/start', data=json.dumps({"players": ["Mario", "Peach", "Luigi"]}))
		json2 = response.data
		self.assertTrue('Mario' in json2)
		self.assertTrue('Peach' in json2)
		self.assertTrue('Luigi' in json2)

	def testAddAnswer(self):
		self.app.post('/start', data=json.dumps({"points": -1}))
		self.app.post('/start', data=json.dumps({"players": ["Mario", "Peach", "Luigi"]}))
		response = self.app.post('/question', data=json.dumps({"player": "Mario", "answer": "sample"}))
		json2 = response.data
		self.assertTrue('"players"' in json2)
		self.assertTrue('"answers"' in json2)
		self.assertTrue('"sample"' in json2)

	def testCantGuessBeforeAllAnswers(self):
		self.app.post('/start', data=json.dumps({"points": -1}))
		self.app.post('/start', data=json.dumps({"players": ["Mario", "Peach", "Luigi"]}))
		#self.app.post('/question', data=json.dumps({"player": "Mario", "answer": "sample"}))
		response = self.app.get('/guess')
		self.assertTrue('"error"' in response.data)

	def testGuess(self):
		self.app.post('/start', data=json.dumps({"points": -1}))
		self.app.post('/start', data=json.dumps({"players": ["Mario", "Peach", "Luigi"]}))
		#self.app.post('/question', data=json.dumps({"player": "Mario", "answer": "sample"}))
		self.app.post('/question', data=json.dumps({"player": "Luigi", "answer": "test"}))
		self.app.post('/question', data=json.dumps({"player": "Peach", "answer": "placeholder"}))
		response = self.app.post('/guess', data=json.dumps({"guesser": "Peach", 'guessee': "Peach", "answer": "placeholder"}))
		json2 = response.data
		self.assertTrue('yourself' in json2)
		response = self.app.post('/guess', data=json.dumps({"guesser": "Luigi", "guessee": "Mario", "answer": "placeholder"}))
		json2 = response.data
		self.assertTrue('Incorrect' in json2)
		response = self.app.post('/guess', data=json.dumps({"guesser": "Mario", "guessee": "Luigi", "answer": "test"}))
		json2 = response.data
		self.assertTrue('Correct' in json2)
		
	def testScore(self):
		self.app.post('/start', data=json.dumps({"points": -1}))
		self.app.post('/start', data=json.dumps({"players": ["Mario", "Peach", "Luigi"]}))
		response = self.app.get('/score')
		self.assertTrue('"Mario",\n1')

if __name__ == '__main__':
	unittest.main()