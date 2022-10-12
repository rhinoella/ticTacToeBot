import discord
import io
from PIL import Image
import random


class tttClass:
  def __init__(self): #constructor
    self.rounds = -1
    self.user = None
    self.userId = None
    self.player2 = None
    self.blank = Image.open("blank.png")
    self.oCat = Image.open("O.png")
    self.xCat = Image.open("X.png")
    self.userSymbol = Image.open("blank.png")
    self.boardList = [[self.blank, self.blank, self.blank], #creates an array of blank images
                      [self.blank, self.blank, self.blank],
                      [self.blank, self.blank, self.blank]]
    self.board = None
    self.winner = False
    self.tie = False

  def playerMove(self, board, author, recipient): #prompts the move and prints out the current board
    self.player2 = author
    if self.rounds % 2 == 0:
      self.user = author
      self.userId = author.id
    else:
      self.user = recipient
      self.userId = recipient.id

    embed = discord.Embed(
    title=f"｡⋆୨୧˚{self.user.display_name}'s turn˚୨୧⋆｡",
    description="..................................................................", color=0xffccdb)
    embed.set_footer(text="Send the row and column of your move: 'y x'")
    embed.set_thumbnail(url="https://i.imgur.com/uz1hkjP.png")
    with io.BytesIO() as image_binary: #converts the image into a PNG so that discord can embed it
      board.save(image_binary, 'PNG')
      image_binary.seek(0)
      file = discord.File(fp=image_binary, filename='image.png')
    embed.set_image(url="attachment://image.png")
    embedList = [file, embed]
    return embedList

  def editBoard(self, y, x): #edits the board array depending on the move
    if self.rounds % 2 == 0 and self.rounds != -1:
      self.boardList[y][x] = self.oCat
    elif self.rounds != -1:
      self.boardList[y][x] = self.xCat

    board = Image.new('RGBA', (3 * self.blank.width, 3 * self.blank.height)) #produces a new image by sticking the image for each square together
    for i in range(3):
      for j in range(3):
        board.paste(self.boardList[i][j],
        ((j * self.blank.width), (i * self.blank.height)))
    self.board = board
    self.rounds += 1

  def checkWinner(self): #checks for a winner
    #horisontal winner
    for i in range(3):
      if self.boardList[i][0] != self.blank and self.boardList[i][0] == self.boardList[i][1] and self.boardList[i][1] == self.boardList[i][2]:
        winner = True
        return winner
#vertical winner
    for j in range(3):
      if self.boardList[0][j] != self.blank and self.boardList[0][j] == self.boardList[1][j] and self.boardList[1][j] == self.boardList[2][j]:
        winner = True
        return winner
#diagonal rightwards winner
    if self.boardList[0][0] != self.blank and self.boardList[0][0] == self.boardList[1][1] and self.boardList[1][1] == self.boardList[2][2]:
      winner = True
      return winner

#diagonal leftwards winner
    if self.boardList[0][2] != self.blank and self.boardList[0][2] == self.boardList[1][1] and self.boardList[1][1] == self.boardList[2][0]:
      winner = True
      return winner
    
    winner = False
    return winner

  def checkTie(self): #checks for a tie
    spaces = 0
    for i in range(3):
      for j in range(3):
        if self.boardList[i][j] == self.blank:
          spaces += 1
    if spaces == 0:
      tie = True
      return tie
    else:
      tie = False
      return tie
  
  def getRounds(self):
    return self.rounds

  def AIMove(self): #for computer generated move
    movesPos = []
    movesProb = [] 

    for y in range(3): #records all the blank squares
      for x in range(3):
        if self.boardList[y][x] == self.blank:
          movesPos.append([y, x])
    print(movesPos)

#checking to see if there are two in a row of any symbols - it will be more likely that the bot will play the winning move/block the opponents winning move
    for i in range(3):
      for j in range(2):
        #horisontal
        if self.boardList[i][j] != self.blank and self.boardList[i][j] == self.boardList[i][j + 1] or (self.boardList[i][0] != self.blank and self.boardList[i][0] == self.boardList[i][2]):
          try:
            x = self.boardList[i].index(self.blank)
            for k in range(80):
              movesProb.append([i, x]) #the move is added to the array of possible moves 80 times
          except:
            pass
        #vertical
        if (self.boardList[j][i] != self.blank and self.boardList[j][i] == self.boardList[j + 1][i]) or (self.boardList[0][i] != self.blank and self.boardList[0][i] == self.boardList[2][i]):
          if j == 0 and self.boardList[j + 2][i] == self.blank:
            for k in range(80):
              movesProb.append([1, i])
          if j == 0 and self.boardList[1][i] == self.blank:
            for k in range(80):
              movesProb.append([1, i])
          if j == 1 and self.boardList[j - 1][i] == self.blank:
            for k in range(80):
             movesProb.append([0, i])
    #diagonal rightwards
    if self.boardList[0][0] != self.blank and self.boardList[0][0] == self.boardList[1][1]:
      if self.boardList[2][2] == self.blank:
        for k in range(80):
          movesProb.append([2, 2])
    if self.boardList[1][1] != self.blank and self.boardList[2][2] == self.boardList[1][1]:
      if self.boardList[0][0] == self.blank:
        for k in range(80):
          movesProb.append([0, 0])
    if self.boardList[0][0] != self.blank and self.boardList[2][2] == self.boardList[0][0]:
      if self.boardList[1][1] == self.blank:
        for k in range(80):
          movesProb.append([1, 1])
    #diagonal leftwards
    if self.boardList[0][2] != self.blank and self.boardList[0][2] == self.boardList[1][1]:
      if self.boardList[2][0] == self.blank:
        for k in range(80):
          movesProb.append([2, 0])
    if self.boardList[1][1] != self.blank and self.boardList[2][0] == self.boardList[1][1]:
      if self.boardList[0][2] == self.blank:
        for k in range(80):
           movesProb.append([2, 2])
    if self.boardList[0][2] != self.blank and self.boardList[2][0] == self.boardList[0][2]:
      if self.boardList[1][1] == self.blank:
        for k in range(80):
          movesProb.append([1, 1])

    movesProbLen = len(movesProb)
    print(movesProbLen)
    while movesProbLen <= 100:
      movesProb.append(random.choice(movesPos)) #the rest of the array will be filled with random moves
      movesProbLen += 1

    botMove = random.choice(movesProb)
    return botMove
