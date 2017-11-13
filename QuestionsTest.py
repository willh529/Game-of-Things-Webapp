import unittest
from Questions import Questions

class GraphTests(unittest.TestCase):
    def testSelectQuestion(self):
        questions = Questions()
        questions.loadQuestionsFromFiles('ListOfQuestions.txt')
        currLen = questions.numQuestions()
        print(questions.selectQuestion())
        self.assertNotEqual(currLen, questions.numQuestions())
        
    def testAddQuestion(self):
        questions = Questions()
        questions.loadQuestionsFromFiles('ListOfQuestions.txt')
        currLen = questions.numQuestions()
        newQuestion = raw_input('Enter a new question: ')
        questions.addQuestion(newQuestion, 'ListOfQuestions.txt')
        self.assertNotEqual(currLen, questions.numQuestions())

if __name__ == '__main__':
    unittest.main()