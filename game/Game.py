from Questions import Questions
from Player import Player

class Game(object):
    def __init__(self, scoreLimit):
        """
        Makes the players for the game and gets the list of questions
        :param scoreLimit: The score limit to reach
        """
        self.numPlayers = 0
        self.questions = Questions()
        self.questions.loadQuestionsFromFiles('ListOfQuestions.txt')
        self.scoreLimit = scoreLimit
        self.unassignedAnswers = []
        self.players = {}
        self.names = []

    def addPlayer(self, name):
        """
        Add a player to the game
        :param name: Name of the player to add. 
        """
        self.players[name] = Player(name)
        self.names = self.players.keys()
        self.numPlayers += 1

    def addQuestion(self, question):
        """
        Add a question to the database
        :param question: Question to add.
        """
        self.questions.addQuestion(question, 'ListOfQuestions.txt')
    
    def displayQuestion(self):
        """
        Displays a question from the list
        """
        return self.questions.selectQuestion()
    
    def getPlayerAnswers(self, name, answer):
        """
        Collects the answers for a question for a player
        :param name: Name of the player
        :param answer: Answer to the question
        """
        self.unassignedAnswers.append(answer)
        self.players[name].updateAnswer(answer)
            
    def checkGuess(self, guesser, guessee, guess):
        """
        Checks if this player's guess is right and increases the guesser's score if it is
        :param guesser: The name of the player that is guessing
        :param guessee: The name of the player that is being guessed
        :param guess: The answer that the guesser is trying to associate with the guessee
        :return: True if guess is correct
        """
        guessee_object = self.players[guessee]
        guesser_object = self.players[guesser]
        if guessee_object.checkGuess(guess):
            guesser_object.increaseScore()
            self.unassignedAnswers.remove(guess)
            self.names.remove(guessee_object.getName())
            return True
        return False

    def resetNameArray(self):
        self.names = self.players.keys()

    def clearAnswers(self):
        self.unassignedAnswers = []
    
    def isGameOver(self):
        """
        Checks if the score limit was reached.
        :return: True if score limit was reached
        """
        #score limit is -1 if infinite play is on
        if self.scoreLimit == -1:
            return False
        for k,v in self.players.iteritems():
            if v.getScore() >= self.scoreLimit:
                print('Player ' + k + ' has won!')
                return True
        return False

    def getPlayerScore(self, name):
        """
        Returns the score of the player.
        :param name: Name of the player
        """
        return self.players[name].getScore()