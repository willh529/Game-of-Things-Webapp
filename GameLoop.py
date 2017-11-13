from Game import Game

numPlayers = int(raw_input('How many players are there? '))
scoreLimit = int(raw_input('Enter the score limit: '))
game = Game(numPlayers, scoreLimit)
game.createPlayers()

while(1):
    print(game.displayQuestion())
    game.getPlayerAnswers()
    questionFinished = False
    while not(questionFinished):
        questionFinished = game.runGuesses()
    if game.isGameOver():
        print("Game over!")
        break
    endGame = input("End game? (Y/N)")
    if endGame.lower() == 'y':
        print("Game over!")
        break
    