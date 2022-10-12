import discord
from discord.ext import commands
import os
import asyncio
import random
from facts import fracksFacts
from ticTacToe import tttClass

bot = commands.Bot(command_prefix="<3", help_command = None)

@bot.event #to know when the bot is ready and running
async def on_ready():
  print("bot is ready") 

@bot.listen #to ensure that the user is using the correct channel for the bot
async def on_message(ctx):
  if (ctx.content.startswith("<3") == True and ctx.channel.id != '''bot channel ID''' and ctx.author.id != '''bot ID'''): #replace the comments with your bot/channel IDs
    wrongChannel = await ctx.channel.send("Please only use commands in the #YOURBOTCHANNEL channel")
    await asyncio.sleep(2)
    await wrongChannel.delete()
    return

@bot.command()
async def ttt(ctx, recipient: discord.Member = None):
  if not recipient: #to make sure the user has tagged someone to play
    await ctx.send("please mention the user you would like to play with (<3ttt @bot)")
    return
  
  author = ctx.author #sets the author from the bot command message
  recipient = recipient #sets the recipient from the bot command message
  newGame = tttClass() #creates a newGame object of the tic tac toe class
  newGame.editBoard(0, 0) #creates the blank board
  endGame = False
  
  while endGame == False:
    embedList = newGame.playerMove(newGame.board, author, recipient) #prints out the board and prompts the move
    await ctx.channel.send(f"{newGame.user.mention} choose your move")
    await ctx.channel.send(file = embedList[0], embed = embedList[1])

    if newGame.userId != '''bot ID''': #replace with your bot ID -> checks to see whether the user is playing with another user or with the bot

      responseCheck = False #loop to see if the response is valid- from the correct user and in the correct channel
      while responseCheck == False:
      
        def check(msg):
          return (msg.author == newGame.user or msg.author == newGame.player2) and msg.channel.id == ctx.channel.id
        
        message = await bot.wait_for('message', check = check) #waits for the check function to return true

        if(len(message.content) == 3): #checks if the move is valid
          try:
            y = int(message.content[0]) - 1
            x = int(message.content[2]) - 1
            if newGame.boardList[y][x] != newGame.blank:
              await ctx.channel.send("this spot is taken, try again")
            else:
              responseCheck = True
          except ValueError: #if the input is not an integer this error rises
            await ctx.channel.send("invalid format (NOT INTEGERS). please send the desired row and column: 'y x'")
        elif(message.content == "<3end"): #checks to see if someone has ended the game
          await ctx.channel.send("game ended")
          return
        else:
          await ctx.channel.send("invalid format (TOO MANY INPUTS). please send the desired row and column: 'y x'") #if there are too many inputs (incorrect format) this error arises
          
    else: #if the user decides to play against the bot
      await asyncio.sleep(2)
      botMove = newGame.AIMove() #calls the function for the bot to create a move
      y = botMove[0]
      x = botMove[1]
      await ctx.channel.send(f"{y + 1} {x + 1}") #the bot will send its move into the channel
    
    newGame.editBoard(y, x) #the coordinate inputs from the players are sent into the function to edit the board according to their move
    newGame.winner = newGame.checkWinner() #checks if theres a winner
    newGame.tie = newGame.checkTie() #checks if theres a tie
    endGame = newGame.winner or newGame.tie #if one is true the game ends

#displays the winner:
  if newGame.winner == True: 
    if (newGame.rounds - 1) % 2 == 0:
      playerWinner = author
    else:
      playerWinner = recipient

    await ctx.channel.send(f"{playerWinner.mention} has won")
    embed = discord.Embed(title=f" ⋆ ˚｡⋆୨୧˚ congratulations {playerWinner.display_name}! ˚୨୧⋆｡˚ ⋆",     description="............................................................................................", color=0xffccdb)
    embed.set_thumbnail(url="https://i.imgur.com/uz1hkjP.png")
    embed.set_image(url = playerWinner.avatar_url)
    await ctx.send(embed=embed)

#displays the tie:
  if newGame.tie == True:
    embed = discord.Embed(title=f" ⋆ ˚｡⋆୨୧˚ it's a tie! ˚୨୧⋆｡˚ ⋆",     description="............................................................................................", color=0xffccdb)
    embed.set_thumbnail(url="https://i.imgur.com/uz1hkjP.png")
    await ctx.send(embed=embed)

@ttt.error #if the user tags a non existing user
async def tttError(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.channel.send("user not found, try again")

bot.run(os.getenv("TOKEN"))