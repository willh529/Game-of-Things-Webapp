import unittest
from Player import Player

class PlayerTest(unittest.TestCase):
    def testGrabName(self):
        testPlayer = Player('Jeff')
        self.assertEquals(testPlayer.getName(), 'Jeff')
        
    def testCheckGuesses(self):
        testPlayer = Player('Jim')
        testPlayer.updateAnswer('Test Answer')
        self.assertTrue(testPlayer.checkGuess('Test Answer'))
    
if __name__ == '__main__':
    unittest.main()
