import pygame
from lib.utils import Paddle, GameState, continue_game, end_screen

size = width, height = (640, 480)

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont("ubuntumono", 32)
score_limit = 50

player_paddle = Paddle(screen)
computer_paddle = Paddle(screen)
computer_paddle.rect.right = width

game_state = GameState()

while game_state.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False

    if (game_state.player_score < score_limit) and (game_state.computer_score < score_limit):
        continue_game(screen, font, game_state, player_paddle, computer_paddle)
    else:
        end_screen(screen, font, game_state)
    
    pygame.display.flip()
    game_state.dt = clock.tick(60) / 1000

pygame.quit()