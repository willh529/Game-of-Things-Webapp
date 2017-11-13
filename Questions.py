import random

class Questions(object):
    def __init__(self):
        """
        Initializes empty questions
        questionsToDisplay represent questions that haven't been selected yet
        """
        self.questions = []
        self.questionsToDisplay = []
        
    def numQuestions(self):
        """
        :return: The number of remaining questions
        """
        return len(self.questionsToDisplay)
        
    def loadQuestionsFromFiles(self, textFile):
        """
        Fills the list of questions
        :param textFile: The file to read questions from
        """
        questionFile = open(textFile, 'r')
        for line in questionFile:
            self.questions.append(line.strip())
            self.questionsToDisplay.append(line.strip())
            
    def addQuestion(self, question, textFile):
        """
        Adds a question to the list and saves it to the database
        :param question: Question to add
        :param textFile: The file to save the questions to
        """
        self.questions.append(question)
        self.questionsToDisplay.append(question)
        outputFile = open(textFile, 'w')
        for q in self.questions:
            outputLine = q
            outputLine += '\n'
            outputFile.write(outputLine)
    
    def selectQuestion(self):
        """
        Selects a random question to be displayed
        :return: The question that was selected
        """
        question = random.choice(self.questionsToDisplay)
        self.questionsToDisplay.remove(question)
        return question
    
    