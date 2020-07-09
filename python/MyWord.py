# prints block letters in Minecraft
# requires AsciiLetters.py
# usage: In minecraft, open the command console and type the command below
# /py MyWord <word>
# import lines below for Raspberry Pi
# import minecraft.minecraft as minecraft
# import minecraft.block as block
# import lines below of raspberry jam mod
import mcpi.minecraft as minecraft
import mcpi.block as block
import sys
import time
import random
from AsciiLetters import letters


# parameters for program
LETTERBLOCKID = block.TNT.id
LETTERBLOCKDATA = 1
LINEHEIGHT = 5 # height of each letter
LETTERWIDTH = 3 # width of each letter
VERTICAL_HEIGHT = 10 # height of line above current position

# helper function
def positionString(pos):
    return "[{x},{y},{z}]".format(x=pos.x,y=pos.y,z=pos.z)

#Class for creating text in minecraft
class MinecraftText:
    def __init__(self, mc):
        self.mc = mc

    #writes a line to minecraft at the next position
    def writeNextLine(self, line, pos):
        linepos = minecraft.Vec3(0,0,0)
        linepos.x, linepos.y, linepos.z = pos.x, pos.y + VERTICAL_HEIGHT, pos.z
        self.writeLineToMC(line, linepos)

    #writes a line of text into minecraft
    def writeLineToMC(self, line, pos):
        currentCursor = pos
        #setup x and z directions
        xDirection, zDirection = 1, 0
        #make line lower case
        line = line.lower()
        #write the line to minecraft  
        for character in line:
            # self.mc.postToChat("writing " + character + " at " + positionString(currentCursor))
            # create the character in minecraft
            self.writeLetterToMC(character, currentCursor, xDirection, zDirection)
            # move the 'cursor' on
            currentCursor.x = currentCursor.x + LETTERWIDTH + 1
                
    #create a letter in minecraft
    def writeLetterToMC(self, character, cursorTopLeft, xDirection, zDirection):
        # the current position is where we have reached in creating the letter
        currentPos = minecraft.Vec3(cursorTopLeft.x, cursorTopLeft.y, cursorTopLeft.z)
    
        # is the character in my letter list?
        if (character in letters.keys()):
            # get the hashes for the character
            letterString = letters[character]
            #loop through all the hashes, creating block
            for digit in letterString:
                if digit == "#":
                    # print "create block x = " + str(currentPos.x)  + " y = " + str(currentPos.y) + " z = " + str(currentPos.z)
                    self.mc.setBlock(currentPos.x, currentPos.y, currentPos.z, LETTERBLOCKID, LETTERBLOCKDATA)
                    currentPos.x = currentPos.x + xDirection
                    currentPos.z = currentPos.z + zDirection
                if digit == " ":
                    self.mc.setBlock(currentPos.x, currentPos.y, currentPos.z, block.AIR.id)
                    currentPos.x = currentPos.x + xDirection
                    currentPos.z = currentPos.z + zDirection
                if digit == "\n":
                    currentPos.y = currentPos.y - 1
                    currentPos.x = cursorTopLeft.x
                    currentPos.z = cursorTopLeft.z


# main program
if __name__=='__main__':
    if len(sys.argv) >= 2:
        msg = sys.argv[1]
    else:
        msg = "hello there"
    mc = minecraft.Minecraft()
    mcText = MinecraftText(mc)
    pos = mc.player.getTilePos()
    # mc.postToChat(msg + positionString(pos))
    mcText.writeNextLine(msg, pos)
