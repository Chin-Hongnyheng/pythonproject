import pygame
import random
import time
import sys ## provide some variable and function that interact strongly with interpreter
from pygame.math import Vector2

pygame.init()
title_font = pygame.font.Font(None, 40)
score_font = pygame.font.Font(None ,40)
## set a display screen to play snake game.
cell_size = 20
number_of_cell = 35

## define some color
Black_color = (0,0,0)
white_color = (255,255,255)
red_color= (255,0,0)
yellow_color = (255,255,0)

width_display = cell_size*number_of_cell
height_display = cell_size*number_of_cell
OFFSET = 75

##food
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body) ## coordinate of food in cell
        
    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size,OFFSET + self.position.y*cell_size, cell_size, cell_size)##pixel
        screen.blit(food_surface, food_rect) ## to load an image of apple
    def generate_random_cell(self):
        x = random.randint(0, number_of_cell -1)
        y = random.randint(0, number_of_cell -1)
        return Vector2(x,y)
        
    def generate_random_pos(self,snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        
        return position
        

class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0) ## move to right
        self.add_segment = False ##to add more initial element when snake eat apple
        self.eat_food = pygame.mixer.Sound("Projectpython/eatfood.wav")
        self.hit_wall = pygame.mixer.Sound("Projectpython/hitwall.wav")
    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cell_size,OFFSET + segment.y * cell_size,cell_size,cell_size)
            pygame.draw.rect(screen,red_color, segment_rect,0,7)
    def update(self):
        self.body.insert(0, self.body[0] + self.direction) ## to insert a first element of the snake body when snake move direction
            ## 0 mean the new element add to the list
        if self.add_segment == True:
            self.add_segment = False

        else:
            self.body = self.body[:-1] ##remove the last segment of the snake body
    def reset(self): ##move the snake to original position
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
        
        
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "Running"
        self.score = 0
    def draw(self):
        self.food.draw()
        self.snake.draw()
    def update(self):
        if self.state == "Running":
            self.snake.update()
            self.check_collision()
            self.check_collision_outside_grid()
            self.check_collision_with_tail()
    def check_collision(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score +=1
            self.snake.eat_food.play()
    def check_collision_outside_grid(self):
        if self.snake.body[0].x == number_of_cell or self.snake.body[0].x ==-1:
            self.game_over()
        if self.snake.body[0].y == number_of_cell or self.snake.body[0].y ==-1:
            self.game_over()
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "Stopped"
        self.score = 0
        self.snake.hit_wall.play()
    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:] ##it mean if snake = a b c d so snake body[1:]=b c d
        if self.snake.body[0] in headless_body: ## it mean if a head part collide with another part of the body game is over
            self.game_over()




## definition
screen = pygame.display.set_mode((2*OFFSET + width_display , 2*OFFSET + height_display))
pygame.display.set_caption("The snake game")
## set the smoothness of the object
clock = pygame.time.Clock()##control framework of game
game = Game()
food_surface = pygame.image.load("Projectpython/apple.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 70)##snake update event every 2 ms not 60s




R=True
## this loop execute 60 time per second
while R :
    ## to exit the window
    for event in pygame.event.get(): ##get all event while controlling ur keyboard
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit() ## stop playing game
            sys.exit()
     
          
    
    if event.type == pygame.KEYDOWN: ## represent a key press event
        if game.state == "Stopped":
            game.state = "Running"
        if event.key == pygame.K_UP and game.snake.direction != Vector2(0,1): ## if a snake move upward we dont allow a snake to move downward
            game.snake.direction = Vector2(0, -1)
        if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,-1):
            game.snake.direction = Vector2(0, 1)
        if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,0):
            game.snake.direction = Vector2(-1,0)
        if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,0):
            game.snake.direction = Vector2(1,0)
        
             
    
    
    screen.fill(Black_color)
    pygame.draw.rect(screen, white_color,(OFFSET-5,OFFSET-5,width_display+10,height_display+10),5)
    game.draw()
    #display a title
    title_surface = title_font.render("The snake game",True,yellow_color)
    score_surface = score_font.render(str(game.score),True,yellow_color)
    screen.blit(title_surface, (OFFSET+20,10))
    screen.blit(score_surface,(OFFSET-5,OFFSET + 10 + height_display))
    
    
    pygame.display.update() ##black screen
    clock.tick(60) ## tell the clock object how much game should run so it run 60times/second
