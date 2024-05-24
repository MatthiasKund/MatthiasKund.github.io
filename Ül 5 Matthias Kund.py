import pygame
import sys

# Inicialiseeri Pygame
pygame.init()

# Ekraani mõõtmed
screen_width = 640
screen_height = 480

# Värvid
background_color = (200, 200, 200)
white = (255, 255, 255)
black = (0, 0, 0)

# Mängu kiirus
fps = 60
clock = pygame.time.Clock()

# Ekraani loomine
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping-Pong Mäng")

# Laadi palli ja aluse pildid
ball_image = pygame.image.load('ball.png')
ball_image = pygame.transform.scale(ball_image, (20, 20))
pad_image = pygame.image.load('pad.png')
pad_image = pygame.transform.scale(pad_image, (120, 20))

# Palli algseis
ball_rect = ball_image.get_rect()
ball_rect.x = screen_width // 2
ball_rect.y = screen_height // 2
ball_speed_x = 4
ball_speed_y = 4

# Aluse algseis
pad_rect = pad_image.get_rect()
pad_rect.x = screen_width // 2 - pad_rect.width // 2
pad_rect.y = screen_height // 1.5
pad_speed = 5
pad_direction = 1

# Punktid
score = 0
font = pygame.font.Font(None, 36)

# Peamine mängu tsükkel
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Palli liikumine
    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y

    # Palli põrkumine seintega
    if ball_rect.left <= 0 or ball_rect.right >= screen_width:
        ball_speed_x *= -1
    if ball_rect.top <= 0:
        ball_speed_y *= -1
    if ball_rect.bottom >= screen_height:
        ball_speed_y *= -1
        score -= 1  # Negatiivne punkt, kui pall puudub alumist äärt

    # Aluse liikumine
    pad_rect.x += pad_speed * pad_direction
    if pad_rect.left <= 0 or pad_rect.right >= screen_width:
        pad_direction *= -1

    # Kokkupõrke tuvastamine alusega
    if pad_rect.colliderect(ball_rect) and ball_speed_y > 0:
        ball_speed_y *= -1
        score += 1  # Positiivne punkt, kui pall puutub alust

    # Tausta värvimine
    screen.fill(background_color)

    # Punktide kuvamine
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    # Palli ja aluse kuvamine
    screen.blit(ball_image, ball_rect)
    screen.blit(pad_image, pad_rect)

    # Ekraani uuendamine
    pygame.display.flip()
    clock.tick(fps)
