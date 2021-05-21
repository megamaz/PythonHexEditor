import os
import sys
import time
import math
import getpass
import keyboard
from PIL import Image

specialCharacters = [155,127] # TODO add more

def waitForKeyPress(keys) -> str:
    while 1:
        for x in keys:
            result = keyboard.is_pressed(x)
            if result:
                return x

def waitForKeyRelease(key) -> str:
    while 1:
        result = keyboard.is_pressed(key)
        if not result:
            return key

def modifyBytes(index, newValue, array):
    hexData = list(array)
    hexData[index] = newValue
    hexData = bytes(hexData)
    return hexData

def displayHexData(data, headpos, start, lines, copyInd, found):

    finalString = ""

    returnedData = None

    hexData = data

    currentLineData = []

    startIndex = (start*16)-(16*lines)
    if startIndex < 0:
        startIndex = 0
    

    endIndex = (start*16)+(16*(lines+1))
    if endIndex > len(hexData):
        endIndex = len(hexData) - 1


    bytesWritten = startIndex

    highlightsRemaining = -1
    for b in hexData[startIndex:endIndex]:

        highlit = bytesWritten == headpos
        
        dataPrinted = hex(b)[2:]

        lineAddress = hex(bytesWritten)[2:]

        if len(lineAddress) < 8:
            lineAddress = ("0"*(8-len(lineAddress))) + lineAddress
        if bytesWritten % 16 == 0:
            finalString += lineAddress + "| "

        if len(dataPrinted) == 1:
            dataPrinted = f"0{dataPrinted}"

        # bad way to do it but it works
        before = ""
        end = ""
        contentsToFind = [hex(int(x))[2:] for x in hexData[bytesWritten:bytesWritten+len(found[1])]]
        if highlit:
            before = "\u001b[47m\u001b[30;1m"
            end = "\u001b[0m "

        elif contentsToFind == found[1] or highlightsRemaining >= 0:
            before = "\u001b[43m\u001b[30m"
            end = "\u001b[0m "
            if highlightsRemaining == -1:
                returnedData = bytesWritten
                highlightsRemaining = len(found[1])-1
            highlightsRemaining -= 1
        else:
            before = ""
            end = " "
        finalString += f'{before}{dataPrinted}{end}'
        
        bytesWritten += 1
        if int(dataPrinted, 16) <= 32 or int(dataPrinted, 16) in specialCharacters:
            currentLineData.append(".")
        else:
            currentLineData.append(fr"{chr(b)}")
        
        currentLineData[-1] = currentLineData[-1].replace(" ", '')
        currentLineData[-1] = f"{before}{currentLineData[-1]}{end[:-1]}"

        if bytesWritten % 16 == 0:
            finalString += f"| {''.join(currentLineData)}\n"
            currentLineData = []
    if bytesWritten % 16 != 0:
        finalString += "   " * (16 - (bytesWritten%16))
        finalString += f"| {''.join(currentLineData)}"
    finalString += "\n"

    hexCode = ""
    if copyInd is None:
        hexCode = "None"
    else:
        hexCode = hex(copyInd)[2:]
        if len(hexCode) == 1:
            hexCode = "0" + hexCode
    finalString += f"""

Copied byte: {hexCode}

CONTROLS
Arrows - move head position
enter  - change highliter byte
c      - Copy current byte
v      - paste copied byte
i      - view current file as B/W image
o      - view current file as RGB image
g      - go to adress
f      - find (start with 0x to find byte, otherwise find text)"""

    os.system("cls")

    print(finalString)

    return returnedData

def main(*args):

    left = "left"
    right = "right"
    up = "up"
    down = "down"
    enter = "enter"
    copy = "c"
    paste = "v"
    bwImage = "i"
    RGBImage = "o"
    goto = "g"
    find = "f"

    copiedContent = None
    foundContent = (None, [None])
    wentToResult = False
    # 1st item = 0/1
    # 0 = byte
    # 1 = text
    # 2nd item list(str) content

    # read args
    if len(args[0]) == 1:
        sys.stdout.write("Specify a file to read.")
        exit()
    
    linesToWrite = 5
    if len(args[0]) == 3:
        try:
            linesToWrite = int(args[0][2])
        except ValueError:
            sys.stdout.write("Incorrect number passed.")
        


    if not os.path.exists(args[0][1]):
        raise FileNotFoundError("This file does not exist.")
    
    hexData = open(args[0][1], 'rb').read()
    
    headpos = 0
    
    displayHexData(hexData, 0, 0, linesToWrite, None, foundContent)


    while True:
        try:
            key = waitForKeyPress([left, right, up, down, enter, copy, paste, bwImage, RGBImage, goto, find])
            if key == left and headpos != 0:
                headpos -= 1
            elif key == right and headpos != len(hexData)-2:
                headpos += 1
            elif key == up and headpos >= 16:
                headpos -= 16
            elif key == down and headpos <= len(hexData)-17:
                headpos += 16
            elif key == enter:
                getpass.getpass("") # otherwise it cancels out of the input for some fucking reason
                newHex = input("Enter new Hex value: ")
                try:
                    hexVal = int(newHex, 16)
                    hexData = modifyBytes(headpos, hexVal, hexData)

                except ValueError:
                    sys.stdout.write("Incorrect hex value.\n")
            elif key == copy:
                copiedContent = hexData[headpos]
            elif key == paste:
                if copiedContent is None:
                    print("You don't have anything copied.")
                else:
                    hexData = modifyBytes(headpos, int(copiedContent), hexData)
            
            elif key == bwImage:
                print("Transforming to BW Image...")
                # find best size. This will be a square.
                size = math.ceil(math.sqrt(len(hexData)))

                bw = Image.new("RGB", (size, size))

                for x in range(len(hexData)):
                    # y value = ground(x/size)
                    # x value = x - (y*size)
                    y = int(x/size)
                    xPos = 0 if x == 0 else x - (y*size)
                    col = int(hexData[x])
                    bw.putpixel((xPos, y), (col, col, col))
                if size < 100:
                    bw = bw.resize((size*10, size*10))
                bw.save(input("Save as: "))
            
            elif key == RGBImage:
                print("Transforming to RGB Image...")
                # find best size. This will be a square.
                # since byte 1 is used for R, byte 2 for G, and 3 for B,
                # then 4 for R and so on the size will be divided by 3

                size = math.ceil(math.sqrt(len(hexData)/3))
                rgb = Image.new("RGB", (size, size))
                col = []
                xVal = 0
                for x in range(len(hexData)):
                    # add value to color
                    col.append(int(hexData[x]))
                    if (x+1) % 3 == 0:
                        # all 3 colors are there
                        yPos = int(xVal/size)
                        xPos = 0 if xVal == 0 else xVal - (yPos*size)
                        # print(f"Plotting at ({xPos}, {yPos}) on {size}")
                        rgb.putpixel((xPos, yPos), tuple(col))
                        col = []

                        xVal += 1
                rgb.save(input("Save as: "))

            elif key == goto:
                headpos = int(input("New address: "), 16)
            
            elif key == find:
                wentToResult = False
                search = input("Search for: ")
                if search.startswith("0x"):
                    if len(search) != 4:
                        print("invalid byte")
                        waitForKeyRelease(enter)
                    else:
                        foundContent = (0, [search[2:]])
                else:
                    foundContent = (1, [hex(ord(x))[2:] for x in search])
                    for x in range(len(foundContent[1])):
                        if len(foundContent[1][x]) == 1:
                            foundContent[1][x] = "0" + foundContent[1][x]
                            

            result = displayHexData(hexData, headpos, int(headpos/16), linesToWrite, copiedContent, foundContent)
            if result is not None and not wentToResult:
                wentToResult = True
                headpos = result

            waitForKeyRelease(key)

        except KeyboardInterrupt:
            write = None
            while write is None:
                write = input("Write to file? (y/n) ")
                write = True if write.lower().startswith("y") else False if write.lower().startswith("n") else None
            if write:
                originalFile = args[0][1]
                with open(originalFile, 'wb') as writeBytes:
                    writeBytes.write(hexData)
                sys.stdout.write("Operation complete.\n")
            
            quit()



if __name__ == "__main__":
    time.sleep(0.1)
    main(sys.argv)