# This is my Connect Four game.
# Astro 98 DeCal, Spring 2015
# Python for Astronomers

import numpy as nim
from graphics import *
import time


#Initial array
connect = nim.zeros((6,7))

#Size initializations
xsize = 700
ysize = (6*xsize)/7 + 90    
circleSize = 48            

#Animation intializations.
stepsize = 130
timesize = 0.10

keeper = {"-1": "blue", "0": "dark red", "1": "gold"} #Keeper of the colors.


#This function is to reverse the y-coordinate.
def rev(it): return ysize - it


#This function checks for four-in-a-row.
def check(dummy):
    four = nim.zeros((4,4))
    for i in range(3):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    four[k][l] = dummy[i+k][j+l]
        
            hori = nim.diagonal((nim.dot(four,abs(four.T))))
            verti = nim.diagonal((nim.dot(abs(four.T),four)))
            diag1 = nim.trace(four)
            diag2 = nim.trace(four[::-1])
            #print four
    
            if ((nim.amax(hori) == 4) or
                (nim.amax(verti) == 4) or
                (diag1 == 4) or
                (diag2 == 4)
                ):
                return 1
                            
            elif ((nim.amin(hori) == -4) or
                (nim.amin(verti) == -4) or
                (diag1 == -4) or
                (diag2 == -4)
                ):
                return -1
    return 0


#The main function where all the shapes are plotted.
def zack():
    
    #Setting the environment.
    win = GraphWin("Connect Four", xsize+400, ysize)
    
    #Making the red "background" rectangle.
    rect = Rectangle(Point(200, rev(45)), Point(xsize+200, rev(ysize-45)))
    rect.setFill("red")
    rect.setOutline("red")
    rect.draw(win)
    
    #Drawing the numbers.
    for it in range(7):
        n = it + 1
        message = Text(Point(200+xsize*(2*n-1)/14, rev(25)), str(n))
        message.draw(win)
        
    #The game directions.
    message = Text(Point(xsize+300,rev(4*ysize/5)),"Press a key between")
    message.draw(win)
    message = Text(Point(xsize+300,rev(4*ysize/5 - 20)),"1 and 7 to play.")
    message.draw(win)
    message = Text(Point(xsize+300,rev(4*ysize/5 - 60)),"Press  q  during")
    message.draw(win)
    message = Text(Point(xsize+300,rev(4*ysize/5 - 80)),"gameplay to quit.")
    message.draw(win)
    message = Text(Point(xsize+300,rev(4*ysize/5 - 120)),"Press  r  to restart.")
    message.draw(win)
    message = Text(Point(xsize+300,rev(4*ysize/5 - 160)),"Have fun!")
    message.draw(win)


    #The function where the game matrix is plotted into circles.
    def plotter():
        for i in range(6):
            for j in range(7):
                pt = Point(200+xsize*(2*j+1)/14, 45+(ysize-90)*(2*i+1)/12)
                c = Circle(pt, circleSize)
                c.setFill(keeper[str(int(connect[i][j]))])
                c.setOutline(keeper[str(int(connect[i][j]))])
                c.draw(win)
                

                
    #This function takes a particular column from connect.
    def column(c):
        return nim.transpose(connect)[c]

                
    #Find the row of connect that the disk should fall on.
    def row(v):
        for it in range(6)[::-1]:
            if (v[0] != 0):
                return 17
            if (v[it] == 0):
                return it
                break
    
        
    #This while loop makes the gameplay mechanics.   
    def zack2(): 
        
        turn = 1 #Keeps track of whose turn it is.

        winner = 0 #Decides when the game ends and who the winner is.
        
        while (winner == 0):
            
            #This plots the new matrix of disks.
            plotter()
                
            #This indicates whose turn it is.
            if(turn == 1):
                player = Text(Point(200+xsize/2, rev(ysize-20)),
                        "Gold Player's Turn")
                player.setTextColor("gold")
            if(turn == -1):
                player = Text(Point(200+xsize/2, rev(ysize-20)),
                        "Blue Player's Turn")
                player.setTextColor("blue")
            player.setStyle("bold")
            player.setSize(28)
            player.draw(win)
        
            
            #This takes the proper key input.
            key = win.getKey()
            while ((key != "q") and (key != "1") and (key != "2") and (key != "3")
                and (key != "4") and (key != "5") and (key != "6") and (key != "7")
                and (key != "r")
            ):
    
                key = win.getKey()
            
            
            #This gives the player a chance to quit or restart.
            if (key == "q"):
                win.close()
                winner = 2
                
            elif (key == "r"):
                for i in range(6):
                    for j in range(7):
                        connect[i][j] = 0
                player.undraw()
                turn = 1
                
            else:
            
            
                #This gives the index of the new disk to be placed.
                c = int(key) - 1
                r = row(column(c))
                
                #This removes the player text.
                player.undraw()

                
                #This prevents disks from overfilling at the top.
                if (r == 17): continue
            
                #This changes the corresponding element in the matrix.
                if (turn == 1):
                    connect[r][c] = 1
                if (turn == -1):
                    connect[r][c] = -1
                turn = -turn
                
                #This is the animation of the falling disk.
                startheight = ysize - 30
                endheight = ysize - (45+(ysize-90)*(2*r+1)/12)
                start = Point(200+xsize*(2*c+1)/14, rev(startheight))

                distance = startheight - endheight
                iterations = distance/stepsize
                
                c = Circle(start, circleSize)
                c.setFill(keeper[str(int(-turn))])
                c.setOutline(keeper[str(int(-turn))])
                c.draw(win)
                for it in range(int(iterations)):
                    c.move(0,stepsize)
                    time.sleep(timesize)
                c.undraw()
                
                
                #This decides the winner (if there is one).
                winner = check(connect)
                
        
        #This is the end-game text.
        if (win.isOpen() == True):
            plotter()
            if(winner == 1):
                player = Text(Point(200+xsize/2, rev(ysize-20)),
                        "Gold Player Wins!")
                player.setTextColor("gold")
            if(winner == -1):
                player = Text(Point(200+xsize/2, rev(ysize-20)),
                        "Blue Player Wins!")
                player.setTextColor("blue")
            player.setStyle("bold")
            player.setSize(28)
            player.draw(win)
            
            
            #Post-game window-closing.
            key = win.getKey()   
            while ((key != "q") and (key != "r")):
                key = win.getKey()
            if (key == "q"): win.close()
            elif (key == "r"): 
                for i in range(6):
                        for j in range(7):
                            connect[i][j] = 0
                player.undraw()
                zack2()
    
    #Calling the while loop.        
    zack2()


#Calling the main function.
zack()

