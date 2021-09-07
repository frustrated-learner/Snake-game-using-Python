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

# Importing The Sounds
crunch_sound = pygame.mixer.Sound("sound/crunch.wav")

# Importing the Score Font
font = pygame.font.Font("font/font.ttf", 25)

# Creating the Game active Variables
GAME_ACTIVE = False
GAME_OVER = False

# Colors
GRASS = (175, 227, 73)
DIMMED_GRASS = (168, 222, 65)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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

                # Creating the Condition to Draw the Snake Body Corners
                else:
                    if next_block.x == 1 and previous_block.y == 1 or next_block.y == 1 and previous_block.x == 1: 
                        screen.blit(self.body_br, snake_rect)
                    if next_block.x == -1 and previous_block.y == -1 or next_block.y == -1 and previous_block.x == -1: 
                        screen.blit(self.body_tl, snake_rect)
                    if next_block.x == -1 and previous_block.y == 1 or next_block.y == 1 and previous_block.x == -1: 
                        screen.blit(self.body_bl, snake_rect)
                    if next_block.x == 1 and previous_block.y == -1 or next_block.y == -1 and previous_block.x == 1: 
                        screen.blit(self.body_tr, snake_rect)

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

    # Creating the Function to Add the Welcome Screen
    def draw_welcome_screen(self):
        # Importing the Welcome Screen
        self.welcome_screen = pygame.image.load("img/welcome_screen.png").convert_alpha()
        self.welcome_screen_x = 170
        self.welcome_screen_y = 310

        # Drawing the Welcome Screen on the Screen
        screen.blit(self.welcome_screen, (self.welcome_screen_x, self.welcome_screen_y))

    # Creating the Function to Draw elements on the Screen
    def draw_element(self):
        global GAME_OVER
        self.draw_grass_checkboard()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.check_collision()
        self.no_spawning_on_snake_body()
        self.game_over()
        self.draw_score()
        
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
        global GAME_OVER
        # Overing the Game after hitting the Game Boundary
        if not 0 <= self.snake.snake_body[0].x < box_number or not 0 <= self.snake.snake_body[0].y < box_number:
            GAME_OVER = True
            
        # Overing the Game hitting Own body
        for any_block in self.snake.snake_body[1:]:
            if self.snake.snake_body[0] == any_block:
                GAME_OVER = True
    
    # Creating the Function to Draw the Game over Screen
    def draw_game_over_screen(self):
        self.game_over_screen = pygame.image.load("img/game_over.png").convert_alpha()
        self.game_over_screen_x = 170
        self.game_over_screen_y = 310

        # Drawing the Game Over Screen on the Screen
        screen.blit(self.game_over_screen, (self.game_over_screen_x, self.game_over_screen_y))

    # Creating the Function to Draw the Grass checkboard on the Screen
    def draw_grass_checkboard(self):
        for row in range(box_number):
            if row % 2 == 0:
                for column in range(box_number):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(column * box_size, row * box_size, box_size, box_size)
                        pygame.draw.rect(screen, DIMMED_GRASS, grass_rect)
            else:
                for column in range(box_number):
                    if column % 2 != 0:
                        grass_rect = pygame.Rect(column * box_size, row * box_size, box_size, box_size)
                        pygame.draw.rect(screen, DIMMED_GRASS, grass_rect)

    # Creating the Function to Draw the Score on the Screen
    def draw_score(self):
        # Creating the Variables for the Score
        self.score_value = str(len(self.snake.snake_body) - 3)
        self.score_x = box_number * box_size - 40
        self.score_y = box_number * box_size - 40

        # Creating the Variables for the Fruit
        self.fruit_x = box_number * box_size - 70
        self.fruit_y = box_number * box_size - 40

        # Creating a Background rect for the  Score
        bg_rect = pygame.Rect((self.fruit_x - 22), (self.score_y - 20), (box_size * 2 - 10), (box_size))
        pygame.draw.rect(screen, GRASS, bg_rect)
        pygame.draw.rect(screen, BLACK, bg_rect, 2)

        # Rendering the Score
        self.score_surface = font.render(self.score_value, True, BLACK)
        self.score_rect = self.score_surface.get_rect(center = (self.score_x, self.score_y))
        screen.blit(self.score_surface, self.score_rect)

        # Rendering the Fruit
        self.fruit_surface = self.fruit.fruit_list[0]
        self.fruit_rect = self.fruit_surface.get_rect(center = (self.fruit_x, self.fruit_y))
        screen.blit(self.fruit_surface, self.fruit_rect)

    # Creating the Function to Show to the Score after Game Over
    def show_you_scored(self):
        font = pygame.font.Font("font/font.ttf", 40)
        
        self.you_scored = str("You scored : " + self.score_value)
        self.you_scored_x = 260
        self.you_scored_y = 450

        # Rendering the You Scored
        self.you_scored_surface = font.render(self.you_scored, True, RED)
        screen.blit(self.you_scored_surface, (self.you_scored_x, self.you_scored_y))

    # Creating the Function to Reset the Snake, Fruit Position after the Game Over
    def reset_everything(self):
        global GAME_OVER
        GAME_OVER = False
        self.fruit.position == main_game.snake.snake_body[0]
        self.snake.snake_body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.snake.direction = Vector2(1, 0)
        self.fruit.x = random.randint(0, box_number - 1)
        self.fruit.y = random.randint(0, box_number - 1)
        self.fruit.position = Vector2(main_game.fruit.x , main_game.fruit.y)
        self.fruit.fruit = random.choice(main_game.fruit.fruit_list)


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
        if event.type == SNAKE_MOVE and GAME_ACTIVE == True and GAME_OVER == False:
            main_game.snake.move_snake()
        # Creating the Snake Movement Keys
        if event.type == pygame.KEYDOWN:
            # Creating the Key to Start the Game
            if event.key == pygame.K_SPACE:
                GAME_ACTIVE = True
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
            # Creating the Game restarting key
            if GAME_OVER == True:
                if event.key == pygame.K_SPACE:
                    main_game.reset_everything()
                    

    # Filling the Screen With Colors
    screen.fill(GRASS)
    
    # Checking the Game is Active or Not
    if GAME_ACTIVE == False:
        # Calling the Function to Draw the Welcome Screen
        main_game.draw_welcome_screen()
    elif GAME_OVER == True:
        # Calling the Function to Draw the Game over Screen
        main_game.draw_game_over_screen()
        main_game.show_you_scored()
    else:
        # Calling the Function to Draw elements on the Screen
        main_game.draw_element()
    
    # Updating the Display
    pygame.display.update()

    # Setting a Fixed FPS
    clock.tick(60)