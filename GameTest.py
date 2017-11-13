import unittest
from Game import Game

class GameTest(unittest.TestCase):
    def testCreatePlayers(self):
        testGame = Game(4, -1)
        testGame.createPlayers()
        self.assertEquals(len(testGame.players), 4)
        
    def testCollectPlayerAnswers(self):
        testGame = Game(4, -1)
        testGame.createPlayers()
        print(testGame.displayQuestion())
        testGame.getPlayerAnswers()
        self.assertEquals(len(testGame.unassignedAnswers), 4)
        
    def testEndGame(self):
        testGame = Game(1, 3)
        testGame.createPlayers()
        testPlayer = testGame.players.values()[0]
        testPlayer.increaseScore()
        testPlayer.increaseScore()
        testPlayer.increaseScore() 
        self.assertTrue(testGame.isGameOver())

    def testRunGuess(self):
        testGame = Game(3, -1)
        testGame.createPlayers()
        print(testGame.displayQuestion())
        testGame.getPlayerAnswers()
        self.assertTrue(testGame.runGuesses())

if __name__ == '__main__':
    unittest.main()