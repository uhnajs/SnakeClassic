import pygame
import time
import random

pygame.init()
pygame.display.set_caption('Classic Snake Game')

# Kolory
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

# Rozmiary ekranu
display_width = 600
display_height = 400

# Ustawienia gry
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

scores_list = []
def your_score(score, y_offset):
    value = score_font.render("Your Score: " + str(score), True, red)
    gameDisplay.blit(value, [0, y_offset])

def draw_borders(border_color, border_width):
    pygame.draw.rect(gameDisplay, border_color, [0, 0, display_width, border_width])  # Górna ramka
    pygame.draw.rect(gameDisplay, border_color, [0, 0, border_width, display_height])  # Lewa ramka
    pygame.draw.rect(gameDisplay, border_color, [display_width - border_width, 0, border_width, display_height])  # Prawa ramka
    pygame.draw.rect(gameDisplay, border_color, [0, display_height - border_width, display_width, border_width])  # Dolna ramka

def prompt_for_name():
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:  # Ogranicz długość nazwy do 10 znaków
                        name += event.unicode
        gameDisplay.fill(white)
        block = score_font.render(name, True, black)
        rect = block.get_rect(center=(display_width / 2, display_height / 2))
        gameDisplay.blit(block, rect)
        pygame.display.update()
        clock.tick(15)



def show_scores():
    gameDisplay.fill(white)
    message("Lista Wyników", black, 100, display_height // 4)
    y_offset = display_height // 3
    for name, score in sorted(scores_list, key=lambda x: x[1], reverse=True):
        score_message = score_font.render(f"{name}: {score}", True, black)
        gameDisplay.blit(score_message, [display_width // 6, y_offset])
        y_offset += 30
    pygame.display.update()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting_for_input = False

    main_menu()



def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(gameDisplay, black, [x[0], x[1], snake_block, snake_block])






def gameLoop():
    game_over = False
    game_close = False

    x1 = display_width / 2
    y1 = display_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            gameDisplay.fill(white)
            message("You lost! Press C-Play Again or Q-Quit", red, 50, display_height // 3)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_close = False
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        your_score(Length_of_snake - 1, 10)

        our_snake(snake_block, snake_List)
        draw_borders(black, 10)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    if game_close:
        pygame.time.delay(500)
        player_name = prompt_for_name()
        if player_name:
            scores_list.append((player_name, Length_of_snake - 1))
            show_scores()
        game_over = True

    if game_over:
        main_menu()


def message(msg, color, x_displace, y_displace):
    mesg = font_style.render(msg, True, color)
    gameDisplay.blit(mesg, [x_displace, y_displace])

def main_menu():
    menu_active = True
    while menu_active:
        gameDisplay.fill(white)
        # Dostosuj położenie i treść komunikatów w menu głównym
        message("N - Nowa Gra", black, display_width // 6, display_height // 3)
        message("L - Lista Wyników", black, display_width // 6, display_height // 3 + 30)
        message("ESC - Wyjście", black, display_width // 6, display_height // 3 + 60)
        pygame.display.update()
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_active = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    gameLoop()  # Rozpocznij nową grę
                elif event.key == pygame.K_l:
                    show_scores()  # Pokaż listę wyników
                elif event.key == pygame.K_ESCAPE:
                    menu_active = False


main_menu()