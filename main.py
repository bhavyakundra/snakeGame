import pygame
from pygame.locals import *
import time
import random
import tkinter as tk
from tkinter import ttk



SIZE = 40
BACKGROUND_COLOR = (130, 224, 201)

class  Screen:
    speed = 0.2
    def __init__(self):
        pygame.init()
        # root window
        root = tk.Tk()
        def start_game():
            if level.get()=='Easy':
                Screen.speed = 0.3
                Game.score = 1
            elif level.get()=='Medium':
                Screen.speed = 0.1
                Game.score = 2
            else:
                Screen.speed = 0.05
                Game.score = 4

            root.destroy()
            Game().run()



            
        root.geometry('1000x700')
        root.resizable(False, False)
        root.title('Snake Game')

        # enter_button

        enter_button = ttk.Button(root,text='Start Game',command=start_game)
        enter_button.place(relx=0.5, rely=0.5, anchor='center')
        level = ttk.Combobox(root,values=["Easy", "Medium","Hard"])
        level.place(relx=0.5, rely=0.6, anchor='center')
        level.current(0)
        root.mainloop()

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,23)*SIZE
        self.y = random.randint(1,15)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [120]
        self.y = [120]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
            if self.x[0]<0:
                self.x[0]=960

        if self.direction == 'right':
            self.x[0] += SIZE
            if self.x[0]>960:
                self.x[0]=0
        if self.direction == 'up':
            self.y[0] -= SIZE
            if self.y[0]<0:
                self.y[0]=680
        if self.direction == 'down':
            self.y[0] += SIZE
            if self.y[0]>680:
                self.y[0]=0

        self.draw()

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    score = 1
    def __init__(self):
        self.surface = pygame.display.set_mode((1000, 720))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        print(x1,'x1',y1,'y1',x2,'x2',y2,'y2')
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()


        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision Occured"

    # def save_snake(self):
    #     print('qqqqqqqqqq')
        # for i in range(0,self.snake.length):
        #     if self.snake.x[0] + SIZE == self.snake.x[i]:
        #         print('aaaaaa')
        #     if self.snake.y[0] + SIZE == self.snake.y[i]:
        #         print('fffffff')
        #     if self.snake.y[0] + SIZE == self.snake.y[i]:
        #         print('fffffff')


    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length * self.score}",True,(0,0,0))
        self.surface.blit(score,(850,10))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length * self.score}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

    def run(self):
        running = True
        pause = False





        while running:
            if not pause:
            
                if self.snake.x[0]>self.apple.x and self.snake.direction != 'right':
                    for i in range(0,self.snake.length):
                        if self.snake.x[0] + SIZE == self.snake.x[i]:
                            self.snake.move_up()
                            print('firstup')
                            if self.snake.y[0] + SIZE == self.snake.y[i]:
                                self.snake.move_left()
                                print('fffffff')
                            else:
                                print('222222222222222up')
                                self.snake.move_up() 
                        else:
                            print('left3errrrrrrrrrrrrrrrrr')
                            self.snake.move_left()
                    print('xless')
                elif self.snake.y[0]>self.apple.y and self.snake.direction != 'down':
                    for i in range(0,self.snake.length):
                        if self.snake.y[0] + SIZE == self.snake.y[i]:
                            self.snake.move_left()
                            if self.snake.x[0] + SIZE == self.snake.x[i]:
                                self.snake.move_down()
                            else:
                                self.snake.move_left()
                        else:
                            self.snake.move_up()
                            print('snakeyless')
                    # else:
                    #     if self.snake.direction != 'down':
                    #         self.snake.move_up()
                    #         print('snakeygreater')
                    
                elif self.snake.x[0]<self.apple.x and self.snake.direction != 'left':
                    for i in range(0,self.snake.length):
                        if self.snake.x[0] + SIZE == self.snake.x[i]:
                            self.snake.move_up()
                            if self.snake.y[0] + SIZE == self.snake.y[i]:
                                self.snake.move_left()
                            else:
                                self.snake.move_up()
                        else:
                            self.snake.move_right()
                    # self.snake.move_right()
                    # print('pppppppppp111')
                elif self.snake.y[0]<self.apple.y and self.snake.direction != 'up':
                    for i in range(0,self.snake.length):
                        if self.snake.y[0] + SIZE == self.snake.y[i]:
                            self.snake.move_left()
                            if self.snake.x[0] + SIZE == self.snake.x[i]:
                                self.snake.move_up()
                            else:
                                self.snake.move_left
                        else:
                            self.snake.move_down()
                    # self.snake.move_down()
                    # print('appleygreater')  
                    # else:
                    #     if self.snake.direction != 'up':
                    #         self.snake.move_down()
                    #         print('appleyless')
                 
            
            

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

            #         if not pause:
            #             
            #                 if event.key == K_LEFT:
            #                     self.snake.move_left()
                    
                                

            #             if self.snake.direction != 'left':

            #                 if event.key == K_RIGHT:
            #                     self.snake.move_right()

            #             if self.snake.direction != 'down':
            #                 if event.key == K_UP:
            #                     self.snake.move_up()

            #             if self.snake.direction != 'up':

            #                 if event.key == K_DOWN:
            #                     self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(Screen.speed)

if __name__ == '__main__':
    game = Screen()
    # game.run()