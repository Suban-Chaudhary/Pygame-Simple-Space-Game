import pygame
import os
pygame.init()
pygame.mixer.init()
pygame.font.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
TITLE = pygame.display.set_caption("Hello from the other side.")
BORDER = pygame.Rect((WIDTH/2)-5, 0, 10, HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 7

WHITE = (255, 255, 255)
LIGHT_SALMON = (255,160,122)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
HEALTH_FONT = pygame.font.SysFont('comicsans', 50)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

SPACESHIP_HEIGHT = 55
SPACESHIP_WIDTH = 40

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

yellow_bullets = []
red_bullets = []
max_bullets = 2
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets","Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets","Gun+Silencer.mp3"))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.fill(WHITE)
    WIN.blit(SPACE_IMAGE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health),1 , WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health),1 , WHITE)

    WIN.blit(red_health_text,(10, 10))
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(yellow, keys_pressed):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x:
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL < WIDTH - yellow.width:
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL < HEIGHT - yellow.height:
        yellow.y += VEL

def red_handle_movement(red, keys_pressed):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL < BORDER.x + BORDER.width - red.width:
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL < HEIGHT - red.height:
        red.y += VEL

def handle_bullets(red, yellow, red_bullets, yellow_bullets):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)   

def main():
    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    red = pygame.Rect((150, 250), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
    yellow = pygame.Rect((550, 250), (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x + red.width, red.y + (red.height//2 - 3), 10, 6)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x, yellow.y + (yellow.height//2 - 3), 10, 6)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                BULLET_HIT_SOUND.play()
                RED_HEALTH -= 1
            if event.type == YELLOW_HIT:
                BULLET_HIT_SOUND.play()
                YELLOW_HEALTH -= 1
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(yellow, keys_pressed)
        red_handle_movement(red, keys_pressed)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH)
        handle_bullets(red, yellow, red_bullets, yellow_bullets)

        winner_text = ""
        if RED_HEALTH <= 0:
            winner_text = "YELLOW WINS !"
        if YELLOW_HEALTH <= 0:
            winner_text = "RED WINS !"
        
        if winner_text != "":
            draw_winner(winner_text)
            main()
    pygame.quit()

if __name__ == '__main__':
    main()



