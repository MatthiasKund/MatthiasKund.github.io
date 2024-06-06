import pygame
import time
import random

pygame.init()

# Ekraani suurus
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Värvid
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Mängu kella seaded
clock = pygame.time.Clock()
snake_block = 10
initial_snake_speed = 20
hard_mode_speed = 30  # Hard mode speed

# Fondid
font_style = pygame.font.SysFont(None, 50)

# Punktide näitamise funktsioon
def score_display(score):
    value = font_style.render("Sinu õunad: " + str(score), True, black)
    screen.blit(value, [0, 0])

# Taimeri näitamise funktsioon
def timer_display(elapsed_time):
    timer_text = font_style.render("aeg: " + str(elapsed_time), True, black)
    screen.blit(timer_text, [screen_width - 150, 0])

# Meie ussi joonistamise funktsioon
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

# Mängu sõnumi kuvamise funktsioon
def message(msg, color, position=None):
    mesg = font_style.render(msg, True, color)
    if position:
        screen.blit(mesg, position)
    else:
        screen.blit(mesg, [screen_width / 6, screen_height / 3])

# Laadimisekraani funktsioon
def loading_screen():
    screen.fill(black)
    message("Loading...", green)
    pygame.display.update()
    time.sleep(2)

# Algusekraani funktsioon
def game_intro():
    intro = True
    while intro:
        screen.fill(white)
        message("Ussimäng", green)
        easy_button = font_style.render("Easy", True, black)
        hard_button = font_style.render("Hard", True, black)
        screen.blit(easy_button, [screen_width / 2 - 50, screen_height / 2 - 50])
        screen.blit(hard_button, [screen_width / 2 - 50, screen_height / 2 + 50])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if screen_width / 2 - 50 <= mouse_pos[0] <= screen_width / 2 + 50:
                    if screen_height / 2 - 50 <= mouse_pos[1] <= screen_height / 2:
                        return initial_snake_speed, 10  # Easy mode, walls spawn every 10 seconds
                    elif screen_height / 2 + 50 <= mouse_pos[1] <= screen_height / 2 + 100:
                        return hard_mode_speed, 5  # Hard mode, walls spawn every 5 seconds

# Mängu peamine funktsioon
def gameLoop(snake_speed, wall_spawn_interval):
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    start_time = time.time()
    wall_timer = start_time

    walls = []

    last_move_time = time.time()
    move_interval = 1.0 / snake_speed  # Time interval between snake moves

    while not game_over:

        while game_close == True:
            screen.fill(black)
            elapsed_time = int(death_time - start_time)  # Calculate the elapsed time at death
            message("you died! Q to quit, C to continue", green)
            score_display(length_of_snake - 1)
            message(f"Elasite: {elapsed_time} sekundit", green, [screen_width / 6, screen_height / 2])
            message(f"Sõid õunu: {length_of_snake - 1}", green, [screen_width / 6, screen_height / 1.5])
            timer_display(elapsed_time)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(snake_speed, wall_spawn_interval)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

            # Destroy all red walls if the player presses 'D' and they have been alive for more than 120 seconds
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d and time.time() - start_time > 120:
                walls.clear()

        if time.time() - last_move_time > move_interval:
            if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
                death_time = time.time()  # Record the time of death
                game_close = True
            x1 += x1_change
            y1 += y1_change
            last_move_time = time.time()

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    death_time = time.time()  # Record the time of death
                    game_close = True

            # Check for collision with walls
            snake_rect = pygame.Rect(x1, y1, snake_block, snake_block)
            for wall in walls:
                if snake_rect.colliderect(wall):
                    death_time = time.time()  # Record the time of death
                    game_close = True

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
                length_of_snake += 1

        screen.fill(white)
        pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block])

        our_snake(snake_block, snake_list)
        elapsed_time = int(time.time() - start_time)
        score_display(length_of_snake - 1)
        timer_display(elapsed_time)

        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, red, wall)

        # Display the option to destroy walls after 120 seconds
        if elapsed_time > 120:
            message("Press D to destroy all red walls", blue, [screen_width / 3, screen_height - 50])

        pygame.display.update()

        # Kontrolli, kas on möödunud wall_spawn_interval sekundit ja lisa sein
        if time.time() - wall_timer > wall_spawn_interval:
            wall_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            wall_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            wall_width = random.choice([10, 20, 30, 40, 50])
            wall_height = random.choice([10, 20, 30, 40, 50])
            walls.append(pygame.Rect(wall_x, wall_y, wall_width, wall_height))
            wall_timer = time.time()  # Lähtesta taimer

        clock.tick(120)  # Set to 120 FPS

    pygame.quit()
    quit()

# Alusta laadimisekraanist
loading_screen()
# Algusekraanilt vali raskusaste
snake_speed, wall_spawn_interval = game_intro()
# Alusta mängu
gameLoop(snake_speed, wall_spawn_interval)

