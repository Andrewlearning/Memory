# coding: utf-8
# to select tiles using a regular cursor.
# There is no player O. A tile flashes when an
# occupied tile is selected, but there is no win or draw
# indication at the end. The game runs until the player
# closes the window.

from uagame import Window
import pygame, time, random
from pygame.locals import *


# User-defined functions

def main():
    window = Window('Memory', 500, 400)
    window.set_auto_update(False)
    game = Game(window)
    game.play()
    window.close()


# User-defined classes
class Tile:
    window = None
    fg_color = pygame.Color("black")
    border_width = 1
    back_image = pygame.image.load('pictures/image0.bmp')

    # ALL class methods need @classmethod on the line
    # before they are defined.
    @classmethod
    def set_window(cls, window):
        # All class methods use cls instead of self.
        # cls is the CLASS which is calling the method.
        # in our case, this will always be Tile.
        cls.window = window

    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.flashing = False
        self.content = ""
        self.image = image
        self.is_flipped = False


    def __eq__(self, other_tile):
        if self.image == other_tile.image:
            print('return true')
            return True
        else:
            print('i am in eq function is flipped is true')
            self.is_flipped = True
           # print('is flipped true,WAIT................')

            #time.sleep(5)
            #self.is_flipped = False
            #time.sleep(5)
            #print('is flipped fals，WAIT.........')
            #time.sleep(5)


    def draw(self):
        x = self.rect.x
        y = self.rect.y
        my_surface = Tile.window.get_surface()
        if self.is_flipped:
            my_surface.blit(self.image, (x, y))
        else:
            my_surface.blit(Tile.back_image, (x, y))

        pygame.draw.rect(Tile.window.get_surface(), Tile.fg_color, self.rect, Tile.border_width)

    def select(self, pos):
        """
        This method checks to see if the the provided position is inside the tile's borders.
        If the tile is clicked update the content of the tile
        Remember the "content" is what we want to draw in the center of the tile.
        in our case this will either be nothing, an X, or an O
        """
        return self.rect.collidepoint(pos) and not self.is_flipped

    def flip(self):
        self.is_flipped = True



class Game:
    # An object in this class represents a complete game.


    def __init__(self, window):
        # Initialize a Game.
        # - self is the Game to initialize
        # - window is the uagame window object
        self.judge = False
        self.window = window
        self.pause_time = 0.04  # smaller is faster game
        self.close_clicked = False
        self.continue_game = True
        self.bg_color = pygame.Color('black')
        # Here, we're calling the class method set_window
        # notice we need to use the class  (Tile) to call the method
        # We need to do this before we create any tiles that need
        # to use window.
        Tile.set_window(self.window)
        #judge_click = Tile.select()
        self.images = self.create_images()
        #self.images0 = self.create_image0()
        self.create_board()
        self.score = 0
        self.window.set_font_size(80)
        self.judgelist = []
        self.two_tiles = True#表示当有翻开两块砖头的时候，就不可以继续翻开了，在handle_event 里使用。
        self.pos = []
        #为什么放在这里不可以？？？？
        # self.judge_sameimage()

    def create_board(self):
        # Creates the board. Our board is nested lists
        # where each list is a row of tiles.
        self.board = []

        for row_num in range(4):
            new_row = self.create_row(row_num)
            # remember that append MODIFIES self.board to
            # add the new_row to the end of the list we use
            # to represent our board
            self.board.append(new_row)

    def create_images(self):
        filenames = ['pictures/image1.bmp', 'pictures/image2.bmp', 'pictures/image3.bmp', 'pictures/image4.bmp',
                     'pictures/image5.bmp', 'pictures/image6.bmp', 'pictures/image7.bmp', 'pictures/image8.bmp']
        images = []

        for file in filenames:
            image_obj = pygame.image.load(file)
            images.append(image_obj)
            images.append(image_obj)
        random.shuffle(images)
        return images


    def create_row(self, row_num):

        row = []
        width = self.window.get_width() / 5
        height = self.window.get_height() / 4
        i = 4 * row_num
        for col_num in range(4):
            x = col_num * width
            y = row_num * height
            new_tile = Tile(x,y, width, height, self.images[i]) #这里的X,Y应该换成 POS
            i = i + 1
            row.append(new_tile)
        return row

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_event()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time)  # set game velocity by pausing

    def handle_event(self):
        # Handle each user event by changing the game state
        # appropriately.
        # - self is the Game whose events will be handled

        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True
        elif event.type == MOUSEBUTTONDOWN and self.two_tiles:
            # for each tile, check if it's been clicked.
            # 不太懂，问问老师？？
            for row in self.board:
                 for tile in row:
                    judge = tile.select(event.pos)
                    self.pos.append(event.pos)
                    if judge:
                        tile.flip()
                        if len(self.judgelist) == 0:
                            self.judgelist.append(tile)
                        elif len(self.judgelist) == 1:
                            if self.judgelist[0].rect != tile.rect:
                                print('edison')
                                self.judgelist.append(tile)


    def judge_sameimage(self):
        if len(self.judgelist) == 2 and self.judgelist[0]:
            self.two_tiles = False
            if self.judgelist[0] == self.judgelist[1]:
                #正确，无动于衷
                self.two_tiles = True
                self.judgelist = []
            else:
                #两个图片不匹配，这里需要 填充image0，且要清空self.jughelist，time.sleep,不能翻图片
                self.two_tiles = False
                for tile in self.judgelist:
                    tile.is_flipped = False
                time.sleep(1)
                self.judgelist = []
                self.two_tiles = True





    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        self.window.clear()
        # Draw anything you need to draw in between
        # these two lines
        # ---------------------#
        self.draw_board()
        self.window.draw_string(str(self.score), 430,0)
        # ---------------------#
        self.window.update()

    def draw_board(self):
        for row in self.board:
            for tile in row:
                tile.draw()

    def update(self):
        self.score = pygame.time.get_ticks()//1000
        self.judge_sameimage()


    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        # your code will look something like this, where you choose
        # what boolean logic to put into your if statement
        # to determine if the game is over (ie. the player
        # has won, or lost, or run out of time, etc.)

        # if ________:
        #   self.continue_game = False
        pass


main()