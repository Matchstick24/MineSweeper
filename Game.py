import pygame
import random

import pygame.locals

pygame.init()

# Setup

ScreenX, ScreenY = 20 * 45 - 30, 15 * 45 - 30
Name = "MineSweeper"
Fps = 60
BackGroundColour = (100, 10, 10)
CellSize = 40
Offset = 5
Size, Mines = 15, 20
CellColour = (214, 58, 50)
Background_Scale = (4 * 45, 14 * 45 - 30)
Background_Pos = (665, 25)
TextFont = pygame.font.SysFont("Arial", CellSize - 5)

Screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption(Name)

# Variables

Running = True
Clock = pygame.time.Clock()
CurrentGame = False
Mouse_LeftDown = False
Mouse_RightDown = False
Wins = 0
Loses = 0

# Main

def DrawText(Text, Font, Colour, x, y):

    Image = Font.render(str(Text), True, Colour)
    Screen.blit(Image, (x, y))

class Game:

    def __init__(self, Size : int, Mines : int):
        
        self.GameOver = False
        self.Size = Size
        self.Flags = Mines
        Rects = {}
        Grid = {}

        # Setup

        def Setup(Grid, Rects):

            for x in range(0, Size + 1):

                Grid[x] = {}
                Rects[x] = {}

                for y in range(0, Size + 1):

                    Grid[x][y] = 0
                    Rects[x][y] = {

                        "Rect" : pygame.Rect(x * CellSize + Offset, y * CellSize + Offset, CellSize - Offset, CellSize - Offset),
                        "Image" : False,
                        "Explored" : False,

                    }

        def SetUpMines(Grid):

            global MinesOnField, Placed

            MinesOnField = 0
            Placed = {}

            for x in range(0, Size + 1):
                Placed[x] = {}
                for y in range(0, Size + 1):
                    Placed[x][y] = False

            def ChoseRandom():

                global MinesOnField, Placed
                RandomX, RandomY = random.randint(0, Size - 1), random.randint(0, Size - 1)

                if Placed[RandomX][RandomY]: # Not Already A Mine
                    return

                MinesOnField += 1
                Placed[RandomX][RandomY] = True

            while MinesOnField < Mines:

                ChoseRandom()

            for x in range(0, Size + 1):
                for y in range(0, Size + 1):
                    if Placed[x][y]:
                        Grid[x][y] = 9

            del Placed

        def SetUpValues(Grid):

            for x in range(0, Size + 1):
                for y in range(0, Size + 1):
                    if Grid[x][y] == 9: # Is A Mine

                        if x - 1 > -1 and Grid[x - 1][y] != 9: # Left
                            Grid[x - 1][y] += 1
                        if x + 1 <= Size and Grid[x + 1][y] != 9: # Right
                            Grid[x + 1][y] += 1
                        if y + 1 <= Size and Grid[x][y + 1] != 9: # Bottom
                            Grid[x][y + 1] += 1
                        if y - 1 > -1 and Grid[x][y - 1] != 9: # Top
                            Grid[x][y - 1] += 1
                        if x - 1 > -1 and y - 1 > -1 and Grid[x - 1][y - 1] != 9: # TopLeft
                            Grid[x - 1][y - 1] += 1
                        if x + 1 <= Size and y - 1 > -1 and Grid[x + 1][y - 1] != 9: # TopRight
                            Grid[x + 1][y - 1] += 1
                        if y + 1 <= Size and x - 1 > -1 and Grid[x - 1][y + 1] != 9: # BottomLeft
                            Grid[x - 1][y + 1] += 1
                        if y + 1 <= Size and x + 1 <= Size and Grid[x + 1][y + 1] != 9: # BottomRight
                            Grid[x + 1][y + 1] += 1

        Setup(Grid, Rects)   
        SetUpMines(Grid)   
        SetUpValues(Grid)

        self.Grid, self.Rects = Grid, Rects
        del Grid, Rects

    def _Sort(self, CurrentX, CurrentY): # Not the best when it comes to perfomance, but a quick solution.

        Rects = self.Rects
        Grid = self.Grid
    
        def SetNeighbours(x, y): 

            if x - 1 > -1 and not Rects[x - 1][y]["Explored"]: # Left
                Rects[x - 1][y]["Image"] = "Images/Searched.bmp"

            if x + 1 <= Size - 1 and not Rects[x + 1][y]["Explored"]: # Right
                Rects[x + 1][y]["Image"] = "Images/Searched.bmp"

            if y + 1 <= Size - 1 and not Rects[x][y + 1]["Explored"]: # Bottom
                Rects[x][y + 1]["Image"] = "Images/Searched.bmp"

            if y - 1 > -1 and not Rects[x][y - 1]["Explored"]: # Top
                Rects[x][y - 1]["Image"] = "Images/Searched.bmp"

            if x - 1 > -1 and y - 1 > -1 and not Rects[x - 1][y - 1]["Explored"]: # TopLeft
                Rects[x - 1][y - 1]["Image"] = "Images/Searched.bmp"

            if x + 1 <= Size - 1 and y - 1 > -1 and not Rects[x + 1][y - 1]["Explored"]: # TopRight
                Rects[x + 1][y - 1]["Image"] = "Images/Searched.bmp"

            if y + 1 <= Size - 1 and x - 1 > -1 and not Rects[x - 1][y + 1]["Explored"]: # BottomLeft
                Rects[x - 1][y + 1]["Image"] = "Images/Searched.bmp"

            if y + 1 <= Size - 1 and x + 1 <= Size - 1 and not Rects[x + 1][y + 1]["Explored"]: # BottomRight
                Rects[x + 1][y + 1]["Image"] = "Images/Searched.bmp"

        def GetNeighbours(x, y):     

            Rects[x][y]["Explored"] = True
            Rects[x][y]["Image"] = "Images/Searched.bmp"

            Neighbours = []

            if x - 1 > -1 and Grid[x - 1][y] == 0 and not Rects[x - 1][y]["Explored"]: # Left
                Neighbours.append((x - 1, y))

            if x + 1 <= Size and Grid[x + 1][y] == 0 and not Rects[x + 1][y]["Explored"]: # Right
                Neighbours.append((x + 1, y))

            if y + 1 <= Size and Grid[x][y + 1] == 0 and not Rects[x][y + 1]["Explored"]: # Bottom
                Neighbours.append((x, y + 1))

            if y - 1 > -1 and Grid[x][y - 1] == 0 and not Rects[x][y - 1]["Explored"]: # Top
                Neighbours.append((x, y - 1))

            if x - 1 > -1 and y - 1 > -1 and Grid[x - 1][y - 1] == 0 and not Rects[x - 1][y - 1]["Explored"]: # TopLeft             
                Neighbours.append((x - 1, y - 1))

            if x + 1 <= Size and y - 1 > -1 and Grid[x + 1][y - 1] == 0 and not Rects[x + 1][y - 1]["Explored"]: # TopRight
                Neighbours.append((x + 1, y - 1))

            if y + 1 <= Size and x - 1 > -1 and Grid[x - 1][y + 1] == 0 and not Rects[x - 1][y + 1]["Explored"]: # BottomLeft     
                Neighbours.append((x - 1, y + 1))

            if y + 1 <= Size and x + 1 <= Size and Grid[x + 1][y + 1] == 0 and not Rects[x + 1][y + 1]["Explored"]: # BottomRight    
                Neighbours.append((x + 1, x + 1))

            for Neighbour in Neighbours:
                
                NeighbourX, NeighbourY = Neighbour

                if Grid[NeighbourX][NeighbourY] != 0:
                    continue

                SetNeighbours(NeighbourX, NeighbourY)
                GetNeighbours(NeighbourX, NeighbourY)

            if x - 1 > -1 and not Rects[x - 1][y]["Explored"]: # Left
                Rects[x - 1][y]["Explored"] = True

            if x + 1 <= Size and not Rects[x + 1][y]["Explored"]: # Right
                Rects[x + 1][y]["Explored"] = True

            if y + 1 <= Size and not Rects[x][y + 1]["Explored"]: # Bottom
                Rects[x][y + 1]["Explored"] = True

            if y - 1 > -1 and not Rects[x][y - 1]["Explored"]: # Top
                Rects[x][y - 1]["Explored"] = True

            if x - 1 > -1 and y - 1 > -1 and not Rects[x - 1][y - 1]["Explored"]: # TopLeft             
                Rects[x - 1][y - 1]["Explored"] = True

            if x + 1 <= Size and y - 1 > -1 and not Rects[x + 1][y - 1]["Explored"]: # TopRight
                Rects[x + 1][y - 1]["Explored"] = True

            if y + 1 <= Size and x - 1 > -1 and not Rects[x - 1][y + 1]["Explored"]: # BottomLeft     
                Rects[x - 1][y + 1]["Explored"] = True

            if y + 1 <= Size and x + 1 <= Size and not Rects[x + 1][y + 1]["Explored"]: # BottomRight    
                Rects[x + 1][y + 1]["Explored"] = True

        Rects[CurrentX][CurrentY]["Explored"] = True

        SetNeighbours(CurrentX, CurrentY)
        GetNeighbours(CurrentX, CurrentY)

    def _Controls(self):
        
        Size = self.Size
        Rects = self.Rects
        Grid = self.Grid

        MousePos = pygame.mouse.get_pos()
        NumberOfTimesExited = 0
        
        for x in range(0, Size + 1):
            for y in range(0, Size + 1):

                Rect = Rects[x][y]
                
                if Rect["Explored"]:
                    
                    NumberOfTimesExited += 1
                    continue

                if Rect["Rect"].collidepoint(MousePos) and Mouse_RightDown and not Rect["Explored"] and self.Flags >= 1: # Flag

                    Rect["Explored"] = True
                    Rect["Image"] = "Images/Flag.bmp"
                    self.Flags -= 1
                
                elif Rect["Rect"].collidepoint(MousePos) and Mouse_LeftDown and not Rect["Explored"]: # Click

                    if Grid[x][y] == 9: # Mine

                        global Loses

                        Loses += 1
                        self.GameOver = True
                    
                    if Grid[x][y] == 0: # Clear
                        self._Sort(x, y)
        
                    Rect["Explored"] = True
                    Rect["Image"] = "Images/Searched.bmp"

        if NumberOfTimesExited == Size ** 2:
            self.GameOver = True

    def OnUpdate(self):

        self._Controls()

        Size = self.Size
        Grid = self.Grid
        Rects = self.Rects

        global Won

        Won = True
        
        for x in range(0, Size + 1):
            for y in range(0, Size + 1):

                if not Rects[x][y]["Explored"]:
                    Won = False
                
                if Rects[x][y]["Image"]:
                    Screen.blit(pygame.transform.scale(pygame.image.load(Rects[x][y]["Image"]).convert_alpha(), (CellSize - Offset, CellSize - Offset)), (x * CellSize + Offset, y * CellSize + Offset))
                else:
                    pygame.draw.rect(Screen, CellColour, Rects[x][y]["Rect"])

                if Grid[x][y] == 0 or Grid[x][y] == 9: continue
                if not Rects[x][y]["Explored"] or Rects[x][y]["Image"] == "Images/Flag.bmp": continue
                DrawText(Grid[x][y], TextFont, (0, 0, 0), x * CellSize + Offset, y * CellSize + Offset)

        if Won:

            global Wins

            Wins += 1
            self.GameOver = True

while Running:

    # Main

    if not CurrentGame:
        CurrentGame = Game(Size, Mines) # New Game

    if CurrentGame.GameOver:
        del CurrentGame
        CurrentGame = False

    # Controls

    for Event in pygame.event.get():
        
        if Event.type == pygame.QUIT:
            Running = False
        elif Event.type == pygame.MOUSEBUTTONDOWN:
            
            if Event.button == 1: Mouse_LeftDown = True
            elif Event.button == 3: Mouse_RightDown = True

        elif Event.type == pygame.MOUSEBUTTONUP:

            if Event.button == 1: Mouse_LeftDown = False
            elif Event.button == 3: Mouse_RightDown = False
    
    # Render

    Screen.fill(BackGroundColour)

    if CurrentGame:
        CurrentGame.OnUpdate()

    Background_Image = pygame.transform.scale(pygame.image.load("Images/Background.bmp").convert_alpha(), Background_Scale)
    Background_Image.set_colorkey((255, 255, 255))
    Screen.blit(Background_Image, Background_Pos)

    # Text

    DrawText(f"Wins : {Wins}", pygame.font.SysFont("Airial", 40), (255, 255, 255), Background_Pos[0] + 30, Background_Pos[1] + 40)
    DrawText(f"Loses : {Loses}", pygame.font.SysFont("Airial", 40), (255, 255, 255), Background_Pos[0] + 30, Background_Pos[1] + 100)
    DrawText(f"Mines : {Mines}", pygame.font.SysFont("Airial", 40), (255, 255, 255), Background_Pos[0] + 30, Background_Pos[1] + 160)
    DrawText(f"Flags : {CurrentGame and CurrentGame.Flags or Mines}", pygame.font.SysFont("Airial", 40), (255, 255, 255), Background_Pos[0] + 30, Background_Pos[1] + 220)

    pygame.display.flip()
    Clock.tick(Fps)

pygame.quit()