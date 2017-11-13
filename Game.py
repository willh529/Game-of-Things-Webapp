from Questions import Questions
from Player import Player

class Game(object):
    def __init__(self, numPlayers, scoreLimit):
        """
        Makes the players for the game and gets the list of questions
        :param numPlayers: The number of players for the game session 
        :param scoreLimit: The score limit to reach
        """
        self.numPlayers = numPlayers
        self.questions = Questions()
        self.questions.loadQuestionsFromFiles('ListOfQuestions.txt')
        self.scoreLimit = scoreLimit
        self.unassignedAnswers = []
        self.players = {}
        self.names = []
        
    def createPlayers(self):
        """
        Creates the players for the game
        """
        i = 0
        while i < self.numPlayers:
            name = raw_input('Enter name for player ' + str(i+1) +': ')
            self.players[name] = Player(name)
            i += 1
        self.names = self.players.keys()
        
    
    def displayQuestion(self):
        """
        Displays a question from the list
        """
        return self.questions.selectQuestion()
    
    def getPlayerAnswers(self):
        """
        Collects the answers for a question
        """
        for k,v in self.players.iteritems():
            answer = raw_input('What is your answer, ' + k + '? ')
            self.unassignedAnswers.append(answer)
            v.updateAnswer(answer)
            
    def checkGuess(self, guesser, guessee, guess):
        """
        Checks if this player's guess is right and increases the guesser's score if it is
        :param guesser: The player that is guessing
        :param guessee: The player that is being guessed
        :param guess: The answer that the guesser is trying to associate with the guessee
        :return: True if guess is correct
        """
        if guessee.checkGuess(guess):
            guesser.increaseScore()
            self.unassignedAnswers.remove(guess)
            self.names.remove(guessee.getName())
            return True
        return False
    
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
    
    def runGuesses(self):
        """
        Runs a loop of guesses among the players
        :return: True if all answers assigned
        """        
        for k,v in self.players.iteritems():
            if not(k in self.names):
                print("Player " + k + " has been guessed already")
                continue
            answerIndex = 0
            nameIndex = 0
            print("Player " + k + "'s turn")
            print("Available answers:")
            for option in self.unassignedAnswers:
                print(str(answerIndex + 1) + '. ' + option)
                answerIndex += 1
            print("\nAvailable players:")
            for name in self.names:
                print(str(nameIndex + 1) + '. ' + name)
                nameIndex += 1
            answerNum = int(raw_input("Choose the Answer ")) - 1
            nameNum = int(raw_input("Choose the Player ")) - 1
            if self.checkGuess(v, self.players[self.names[nameNum]], self.unassignedAnswers[answerNum]):
                print("Correct guess!")
            else:
                print("Wrong guess.")
        return len(self.unassignedAnswers) == 0
        