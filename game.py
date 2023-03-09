import pygame
from piece import Piece 
from board import Board 
import os
from solver import Solver
from time import sleep

class Game:
    def __init__(self, size, prob):
        self.board = Board(size, prob)
        pygame.init()
        # self.sizeScreen = 800, 800  # original setting is too large for my Macbook
        self.sizeScreen = 600, 600
        # set pygame console dimension
        self.screen = pygame.display.set_mode(self.sizeScreen)
        # calculate each piece size
        self.pieceSize = (self.sizeScreen[0] / size[1], self.sizeScreen[1] / size[0]) 
        self.loadPictures()
        self.solver = Solver(self.board)

    def loadPictures(self):
        self.images = {}   # Create a empty dictionary
        imagesDirectory = "images"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue
            path = imagesDirectory + r"/" + fileName 
            img = pygame.image.load(path)
            # convert() change the pixel format of an image with no arguments, 
            # to create a copy that will draw more quickly on the screen.
            img = img.convert()
            img = pygame.transform.scale(img, (int(self.pieceSize[0]), int(self.pieceSize[1])))
            self.images[fileName.split(".")[0]] = img
    
    # The run method let the game object to run         
    def run(self):
        running = True
        while running:
            # infinite loop to detect the user input key-events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.getWon() or self.board.getLost()):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.handleClick(pygame.mouse.get_pos(), rightClick)
                if event.type == pygame.KEYDOWN:
                    self.solver.move()
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            
            if self.board.getWon():
                self.win_sound()
                running = False
            elif self.board.getLost():
                self.loss_sound()
                running = False
                g = Game((15,15), 0.2)
                g.run()
        pygame.quit()
        
    def draw(self):
        topLeft = (0, 0)
        for row in self.board.getBoard():
            for piece in row:
                rect = pygame.Rect(topLeft, self.pieceSize)
                image = self.images[self.getImageString(piece)]
                self.screen.blit(image, topLeft) 
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    def getImageString(self, piece):
        if piece.getClicked():
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'
        if (self.board.getLost()):
            if (piece.getHasBomb()):
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.getFlagged() else 'empty-block'
        return 'flag' if piece.getFlagged() else 'empty-block'

    def handleClick(self, position, flag):
        index = tuple(int(pos // size) for pos, size in zip(position, self.pieceSize))[::-1] 
        self.board.handleClick(self.board.getPiece(index), flag)

    def win_sound(self):
        sound = pygame.mixer.Sound('win.wav')
        sound.play()
        sleep(3)
   

    def loss_sound(self):
        sound = pygame.mixer.Sound('loss.mp3')
        sound.play()
        sleep(3)


