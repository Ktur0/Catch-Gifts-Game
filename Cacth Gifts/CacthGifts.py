import pygame
import random

pygame.init()

# Player
player_width = 100
player_height = 40
player_x = 200
player_y = 570
player_speed = 0.7
player = pygame.Rect(player_x,player_y,player_width,player_height)
car = pygame.image.load('minecar.png')

# Box
box_size = 40
box_speed = 0.55
boxes = []
gift = pygame.image.load('Gift.png')
tnt = pygame.image.load('boom.png')

# Boom
boom_size = 40
boom_speed = 0.55
booms = []
gift_bomb = pygame.image.load('gift_bomb.png')


# Set up screen
width_screen = 500
height_screen = 610
icon = pygame.image.load('tnt.png')
window = pygame.display.set_mode((width_screen,height_screen))
pygame.display.set_caption('Catch gifts')
pygame.display.set_icon(icon)
run = True

# Score
i = 0
score = 0
font = pygame.font.Font(None,25)
font_strt = pygame.font.Font(None,40)
sound = pygame.mixer.Sound('cash money.mp3')
boom_sound = pygame.mixer.Sound('boom.mp3')
scores = []

# Button
start = False
str_but = pygame.image.load('startbutton.png')
strt_but_rect = str_but.get_rect(center = (250,300))
def check_click(x_mouse,y_mouse,image_rect,width_but = 50, height_but = 50):
    x,y = image_rect.centerx,image_rect.centery   
    if abs(x_mouse - x) <= width_but and abs(y_mouse - y) <= height_but:
        return True
    return False
again_but = pygame.image.load('againbutton.png')
again_but_rect = again_but.get_rect(center = (250,300))
again = False

#Game loop
while run:
    window.fill('grey')

    if start == False:
        strt_text = font_strt.render("Click the button to play",True,(0,0,0))
        window.blit(strt_text,(100,200))
        window.blit(str_but,strt_but_rect)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        x,y = pygame.mouse.get_pos()
        if check_click(x,y,strt_but_rect) == True:
            start = True
        else:
            run = False

    if again == True:
        again_text = font_strt.render("Click the button to play again",True,(0,0,0))
        ur_score = font_strt.render("Your Score: " + str(score),True,(0,0,0))
        window.blit(ur_score,(150,370))
        window.blit(again_text,(50,200))
        window.blit(gift,(230,420))
        window.blit(again_but,again_but_rect)
        pygame.display.update()

    if event.type == pygame.MOUSEBUTTONDOWN:
        x,y = pygame.mouse.get_pos()
        if check_click(x,y,again_but_rect) == True:
            again = False
            score = 0
            player.x = 200
        else:
            run = False


    if start == True and again == False:

        # Key control player
        key = pygame.key.get_pressed()
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and player.x >= 0:
            player.x -= player_speed
        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and player.x <= width_screen - player_width:
            player.x += player_speed

        # Updata game object
        if len(boxes) < 4:
            box_x = random.randint(0,450)
            box_y = random.randint(-100,0)
            box = pygame.Rect(box_x,box_y,box_size,box_size)
            boxes.append(box)
        
        for box in boxes:
            box.y += box_speed
            if box.colliderect(player):
                score += 10
                boxes.remove(box)
                sound.play()
            if box.y >= 600:
                boxes.remove(box)
    
        if len(booms) < 1:
            boom_x = random.randint(0,450)
            boom_y = random.randint(-100,0)
            boom = pygame.Rect(boom_x,boom_y,boom_size,boom_size)
            booms.append(boom)

        for boom in booms:
            boom.y += boom_speed
            if boom.colliderect(player):
                window.blit(tnt,boom)
                booms.remove(boom)
                boomm = True
                if boomm == True:
                    boom_sound.play()
                    pygame.time.delay(1000)
                    scores.append(score)
                    again = True
            if boom.y >= 600:
                booms.remove(boom)

        # Draw   
        window.blit(car,player)
        for box in boxes:
            window.blit(gift,box)
        
        for boom in booms:
            window.blit(gift_bomb,boom)
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        window.blit(score_text, (10, 10))

        pygame.display.update()