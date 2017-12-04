class Player(object):
    def __init__(self, name):
        """
        Initializes a player with their answer to the question with a score of 0
        :param answer: The answer for the current question
        """
        self.answer = ''
        self.name = name
        self.score = 0
        
        
    def getName(self):
        """
        Get name of player
        :return: Name of player
        """
        return self.name
        
    def checkGuess(self, guess):
        """
        Checks if a player answered the current guess
        :return: True if player answered the current guess
        """
        return self.answer == guess
    
    def increaseScore(self):
        """
        Increment score when player guesses right
        """
        self.score += 1
        
    def getScore(self):
        """
        Gets the score of the player
        :return: The score of the player
        """
        return self.score
        
    def updateAnswer(self, newAnswer):
        """
        Update the answer for a new question
        """
        self.answer = newAnswer
        
    
    