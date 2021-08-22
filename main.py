import pygame, random
from pygame.math import Vector2
from pygame import mixer

pygame.init()

# Creating the Display Grid
box_size = 40
box_number = 20

# Creating some Display Variables
width = (box_size * box_number)
height = (box_size * box_number)
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("img/head_down.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake")
running = True
clock = pygame.time.Clock()

# Importing Some Sound Variables
crunch_sound = pygame.mixer.Sound("sound/crunch.wav")

# Colors
LAWNGREEN = (175, 227, 73)
DIMMED_LAWNGREEN = (168, 222, 65)

# Creating the Class for the Fruit
class FRUIT:
    def __init__(self):
        self.x = random.randint(0, box_number - 1)
        self.y = random.randint(0, box_number - 1)
        self.position = Vector2(self.x , self.y)

        # Randomizing the Fruit Before Importing
        self.fruit_list = [
            pygame.image.load("img/foods/apple.png").convert_alpha(),
            pygame.image.load("img/foods/passion-fruit.png").convert_alpha(),
            pygame.image.load("img/foods/watermelon.png").convert_alpha(),
            pygame.image.load("img/foods/pineapple.png").convert_alpha(),
            pygame.image.load("img/foods/mushroom.png").convert_alpha(),
            pygame.image.load("img/foods/orange.png").convert_alpha(),
            pygame.image.load("img/foods/rice.png").convert_alpha(),
            pygame.image.load("img/foods/grape.png").convert_alpha()
        ]
        self.fruit = random.choice(self.fruit_list)

    # Creating the Function to Draw the Fruit on the Screen
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.x * box_size), int(self.y * box_size), box_size, box_size)
        screen.blit(self.fruit, fruit_rect)

    # Creating the Function to Respawn the Fruit after Collision
    def randomize_fruit_position(self):
        self.x = random.randint(0, box_number - 1)
        self.y = random.randint(0, box_number - 1)
        self.position = Vector2(self.x , self.y)
        self.fruit_list = self.fruit_list[:]
        self.fruit = random.choice(self.fruit_list)
        
# Creating the Class for the Snake
class SNAKE:
    def __init__(self):
        self.snake_body = [
            Vector2(6, 9),
            Vector2(5, 9),
            Vector2(4, 9)
        ]
        
        self.direction = Vector2(1, 0)
        self.add_block = False

        # Importing the Snake Head Graphics
        self.head_down = pygame.image.load("img/head_down.png").convert_alpha()
        self.head_left = pygame.image.load("img/head_left.png").convert_alpha()
        self.head_right = pygame.image.load("img/head_right.png").convert_alpha()
        self.head_up = pygame.image.load("img/head_up.png").convert_alpha()
        
        # Importing the Snake Tail Graphics
        self.tail_down = pygame.image.load("img/tail_down.png").convert_alpha()
        self.tail_left = pygame.image.load("img/tail_left.png").convert_alpha()
        self.tail_right = pygame.image.load("img/tail_right.png").convert_alpha()
        self.tail_up = pygame.image.load("img/tail_up.png").convert_alpha()

        # Importing the Body Graphics
        self.body_horizontal = pygame.image.load("img/body_horizontal.png").convert_alpha()
        self.body_vertical = pygame.image.load("img/body_vertical.png").convert_alpha()

        # Importing the Body Corner Graphics
        self.body_bl = pygame.image.load("img/body_bl.png").convert_alpha()
        self.body_br = pygame.image.load("img/body_br.png").convert_alpha()
        self.body_tl = pygame.image.load("img/body_tl.png").convert_alpha()
        self.body_tr = pygame.image.load("img/body_tr.png").convert_alpha()


    # Creating the Function to Draw the Snake on the Screen
    def draw_snake(self):
        # Calling the Functions to Update the Snake Body Part Graphics
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index, each_block in enumerate(self.snake_body):
            snake_rect = pygame.Rect(int(each_block.x * box_size), int(each_block.y * box_size), box_size, box_size)

            # Creating the Conditions to Draw the Snake Head and Tail
            if index == 0:
                screen.blit(self.head, snake_rect)
            elif index == len(self.snake_body) - 1:
                screen.blit(self.tail, snake_rect)
                
            # Creating the Condition to Draw the Snake Body 
            else:
                next_block = self.snake_body[index + 1] - each_block
                previous_block = self.snake_body[index - 1] - each_block
                if next_block.x == previous_block.x : screen.blit(self.body_vertical, snake_rect)
                if next_block.y == previous_block.y : screen.blit(self.body_horizontal, snake_rect)

    # Creating the Function to Update the Head Graphics
    def update_head_graphics(self):
        self.the_head_vector = self.snake_body[0] - self.snake_body[1]
        if self.the_head_vector == Vector2(1, 0) : self.head = self.head_right
        if self.the_head_vector == Vector2(-1, 0) : self.head = self.head_left
        if self.the_head_vector == Vector2(0, 1) : self.head = self.head_down
        if self.the_head_vector == Vector2(0, -1) : self.head = self.head_up
        
    # Creating the Function to Update the Tail Graphics
    def update_tail_graphics(self):
        self.the_tail_vector = self.snake_body[-2] - self.snake_body[-1]
        if self.the_tail_vector == Vector2(1, 0) : self.tail = self.tail_left
        if self.the_tail_vector == Vector2(-1, 0) : self.tail = self.tail_right
        if self.the_tail_vector == Vector2(0, -1) : self.tail = self.tail_down
        if self.the_tail_vector == Vector2(0, 1) : self.tail = self.tail_up
            
    # Creating the Function to Move the snake
    def move_snake(self):
        if self.add_block == False:
            snake_body_copy = self.snake_body[: - 1]
            snake_body_copy.insert(0, self.snake_body[0] + self.direction)
            self.snake_body = snake_body_copy[:]
        else:
            snake_body_copy = self.snake_body[:]
            snake_body_copy.insert(0, self.snake_body[0] + self.direction)
            self.snake_body = snake_body_copy[:]
            self.add_block = False

# Creating the Class for the Main logic of the Game
class MAIN:
    def __init__(self):
        self.fruit = FRUIT()
        self.snake = SNAKE()

    # Creating the Function to Draw elements on the Screen
    def draw_element(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.check_collision()
        self.no_spawning_on_snake_body()
        self.game_over()

    # Creating the Function to Update the Screen
    def update_screen(self):
        self.snake.move_snake()
        
    # Creating the Function to Check for Collision
    def check_collision(self):
        if self.fruit.position == self.snake.snake_body[0]:
            self.fruit.randomize_fruit_position()
            crunch_sound.play()
            self.snake.add_block = True
            
    # Creating a Function to Respawn the Fruit if it spawns on the Snake Body
    def no_spawning_on_snake_body(self):
        for any_block in self.snake.snake_body:
            if self.fruit.position == any_block:
                self.fruit.randomize_fruit_position()
            
    # Creating the Function to Over the Game
    def game_over(self):
        global running
        # Overing the Game after hitting the Game Boundary
        if not 0 <= self.snake.snake_body[0].x < box_number or not 0 <= self.snake.snake_body[0].y < box_number:
            running = False
            
        # Overing the Game hitting Own body
        for any_block in self.snake.snake_body[1:]:
            if self.snake.snake_body[0] == any_block:
                running = False


# Assigning the Classes
main_game = MAIN()

# Creating the Userevent to Move the Snake
SNAKE_MOVE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_MOVE, 200)


# Creating the Main Loop of the Game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Using the Userevent to Call the Snake move Function
        if event.type == SNAKE_MOVE:
            main_game.snake.move_snake()
        # Creating the Snake Movement Keys
        if event.type == pygame.KEYDOWN:
            # Creating the Condition for the Snake not to Reverse its Direction
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    # Filling the Screen With Colors
    screen.fill(LAWNGREEN)
    
    # Calling the Function to Draw elements on the Screen
    main_game.draw_element()
    
    # Updating the Display
    pygame.display.update()

    # Setting a Fixed FPS
    clock.tick(60)