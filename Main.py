import pygame
import os
import bolts
import AI
import time
import random


# citations:
# cat.png:  "Scratch Cat." Scratch, https://scratch.mit.edu/
# Jeroo.png: "Jeroo." Jeroo, https://www.jeroo.org/
# Alice.png: "Alice." Alice, https://www.alice.org/
# dino.png: "Daisy the Dinosaur." Daisy the Dinosaur, https://www.daisythedinosaur.com/

# noinspection PyUnusedLocal
def game():
    pygame.init()
    pygame.font.init()

    # setting variables like backgrounds and speed
    # load all backgrounds
    backgrounds = []
    for filename in os.listdir(r'C:\Users\Daniel J\PycharmProjects\Create_Game\assets\background'):
        backgrounds.append(filename)

    my_font = pygame.font.SysFont('Calibri', 20)
    count = 0
    speed = 3.5
    dis_width = 504
    dis_height = 648
    shots = []
    AIs = []
    total_shots = 0
    total_hits = 0
    score = 0
    lives = 3
    invul_time = 4  # in seconds
    is_invul = False
    call_time = time.time()
    curr_time = time.time()
    # load and set the logo
    logo = pygame.image.load("assets/cat.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Create Project")

    # create a surface on screen that has the size of 504 x 648 (o.g. background is 224 x 288)
    screen = pygame.display.set_mode((dis_width, dis_height))

    # noinspection PyShadowingNames,PyUnusedLocal
    def cat(x, y):
        if curr_time - call_time < invul_time:
            screen.blit(cat_inv, (x, y))
        else:
            screen.blit(cat_img, (x, y))

    # noinspection PyShadowingNames
    def bolt_print(x, y):
        screen.blit(bolt_img, (x, y))

    # noinspection PyShadowingNames
    def live_print():
        s_cat_img = pygame.transform.rotozoom(cat_img, 0, .35)
        x_life = 4
        for i in range(lives-1):    # 3 lives: 2 as icons, 1 as player
            screen.blit(s_cat_img, (x_life, dis_height - 20))    # arbitrary 20 for funsies
            x_life += 19    # small cat is 16 pixels so 3 pixel space

    # noinspection PyShadowingNames
    # print text at a location and keep in bounds
    def screen_print(text, x, y):
        # width of screen is 504 pixels, can fit close to 60 characters per line
        # one character ~= 8 pixels
        output = ""
        length = len(text)
        i = 0
        # - x/8 accounts for offset text
        off_check = int((60 - (x/8)))    # index of end of string of offset text
        while i < off_check:
            if i == length:
                break
            output += text[i]
            i += 1

        text_out = my_font.render(output, False, (255, 255, 255))
        screen.blit(text_out, (x, y))
        # if text is longer than width, print rest of text on new line (recursively)
        if length > off_check:
            screen_print(text[off_check:], x, y+20)

    # noinspection PyShadowingNames
    def rotate(scrn, img, x, y, angle):
        center = img.get_rect(topleft=(x, y)).center

        rot_img = pygame.transform.rotate(img, angle)
        new_rect = rot_img.get_rect(center=center)

        scrn.blit(rot_img, new_rect.topleft)

    # noinspection PyShadowingBuiltins
    # parent algorithm
    def create_enemy():
        num = random.randint(1, 10)
        # type name shadows the same name from AI
        if num == 10:
            type = 1
        elif 7 <= num < 10:
            type = 2
        else:
            type = 3

        left_right = random.randint(0, 1)
        if left_right == 1:
            x_strt = dis_width
        else:
            x_strt = 0

        y_strt = random.randint(0, dis_height-300)

        mob = AI.AI(type, x_strt, y_strt)
        AIs.append(mob)
        mob.bounds()
        mob.move()

    # startup screen stuff
    print("Press Space to Begin!")
    starting = True
    running = True
    ending = True
    while starting:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                starting = False
                ending = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    starting = False

        temp = pygame.image.load("assets/background/" + backgrounds[int(count)])
        screen.blit(temp, (0, 0))
        if int(count) == 7:
            count = 0
        else:
            count += 0.1
        screen_print("Use arrow keys to move and space to shoot", 10, dis_height-60)
        screen_print("If you get hit, you will gain a golden border to show that  you are invincible for a while", 10, dis_height-40)
        screen_print("Press space to begin", (dis_width/2)-100, (dis_height/2)-125)
        screen_print("Only shots hurt, not enemies", (dis_width/2)-130, (dis_height/2)-160)
        # screen_print("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum", 0, 30)
        pygame.display.update()

    # cat is 190 x 200 originally
    cat_img = pygame.image.load("assets/cat.png")
    cat_inv = pygame.image.load("assets/cat_invul.png")
    # cat is 47.5 x 50
    cat_img = pygame.transform.rotozoom(cat_img, 90, .25)
    cat_inv = pygame.transform.rotozoom(cat_inv, 90, .25)
    cat_width = 47.5
    cat_height = 50

    # bolt is 5x23 originally
    bolt_img = pygame.image.load("assets/shot.png")
    bolt_width = 5
    bolt_height = 23

    x = (dis_width*.45)
    y = (dis_height*.90)

    d_x = 0
    angle = 0
    # running = True <-- set earlier for convenience
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                ending = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    d_x = -speed
                    """ and x > 0"""
                elif event.key == pygame.K_RIGHT:
                    d_x = speed
                    """and x < dis_width"""
                elif event.key == pygame.K_SPACE:
                    shots.append(bolts.Bolts(x+10, y, True))     # I want laser beams from the eyes so start to right a little
                    total_shots += 1
                elif event.key == pygame.K_k:
                    lives -= 1
                    call_time = time.time()
                elif event.key == pygame.K_j:
                    score += 10
                elif event.key == pygame.K_r:
                    angle += 12

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    d_x = 0

        if lives == 0:
            running = False
        # in charge of boundaries
        x += d_x
        if x < 0:
            x += speed
        elif x > dis_width-cat_width:
            x -= speed

        # in charge of printing stuff in correct position and correct order
        # this should always be the first thing to print
        temp = pygame.image.load("assets/background/" + backgrounds[int(count)])
        screen.blit(temp, (0, 0))
        if int(count) == 7:
            count = 0
        else:
            count += 0.1

        # mob spawning related to count
        if count % 8 == 0:
            create_enemy()
            for i in AIs:
                if i.health == 0:
                    AIs.remove(i)
                i.move()
                d_angle = i.turn()
                rotate(screen, i.img, i.x, i.y, d_angle)
                i.bounds()
                if AI.AI.shoot():
                    shots.append(bolts.Bolts(i.x, i.y, False))
        for j in AIs:
            if j.health == 0:
                AIs.remove(j)
            j.move()
            j.bounds()
            rotate(screen, j.img, j.x, j.y, 0)

        for n in shots:
            n.move()
            if n.y < 0:
                shots.remove(n)
            elif n.y > dis_height:
                shots.remove(n)
            else:
                # handles enemy shots while not invul
                if not n.isPlayers and not is_invul:
                    # check if top left corner is within player model
                    if x < n.x < x + cat_width and y < n.y < y + cat_height:
                        lives -= 1
                        is_invul = True
                        call_time = time.time()
                        shots.remove(n)
                    # check if bottom left corner is within player model
                    elif x < n.x + n.bolt_width < x + cat_width and y < n.y + n.bolt_height < y + cat_height:
                        lives -= 1
                        is_invul = False
                        call_time = time.time()
                        shots.remove(n)
                # handles enemies, but only topleft corner to limit the amount of computations
                elif n.isPlayers:
                    for e in AIs:
                        if e.x < n.x < e.x + e.AI_width and e.y < n.y < e.y + e.AI_height:
                            e.hurt()
                            if n in shots:
                                shots.remove(n)
                            total_hits += 1
                            if e.type == 1:
                                score += 100
                            elif e.type == 2:
                                score += 40
                            else:
                                score += 20
                bolt_print(n.x, n.y)    # if the bolt isn't removed blit the shot at its stored coordinates

        cat(x, y)
        live_print()
        screen_print(("Score " + str(score)), 0, 0)
        pygame.display.update()
        curr_time = time.time()

    while ending:
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                ending = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ending = False
                    game()
        temp = pygame.image.load("assets/background/" + backgrounds[int(count)])
        screen.blit(temp, (0, 0))
        screen_print(("You shot " + str(total_shots) + " times!"), (dis_width/2)-120, (dis_height/2)-40)
        screen_print(("You hit an enemy " + str(total_hits) + " times!"), (dis_width/2)-120, (dis_height/2)+0)
        if total_shots == 0:
            screen_print("You had an accuracy of 0.00%!", (dis_width/2)-120, (dis_height/2)+40)
        else:
            screen_print(("You had an accuracy of " + "{0:.2f}".format(100*total_hits/total_shots) + "%!"), (dis_width/2)-120, (dis_height/2)+40)
        screen_print(("Your final score was " + str(score) + "! Congratulations!"), (dis_width/2)-120, (dis_height/2)+80)
        screen_print("Thank you for playing, press enter to play again or click the x button to close the   app", (dis_width / 2) - 120, (dis_height / 2) + 120)
        pygame.display.update()


# startup
if __name__ == "__main__":
    game()

