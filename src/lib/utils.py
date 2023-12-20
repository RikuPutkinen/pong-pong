import pygame
import math
import random

class Ball():
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 100
        self.vector = pygame.math.Vector2.from_polar((self.speed, angle))
        self.radius = 10
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
        self.rect.centerx = x
        self.rect.centery = y
    
    def update_pos(self, dt):
        (speed, angle) = pygame.math.Vector2.as_polar(self.vector)
        self.x += dt * speed * math.cos(math.radians(angle))
        self.y += dt * speed * math.sin(math.radians(angle))
        self.rect.update(self.x, self.y, self.radius * 2, self.radius * 2)
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def check_collision(self, screen, paddles):
        (width, height) = screen.get_size()
        horizontal = pygame.math.Vector2((1, 0))
        vertical = pygame.math.Vector2((0, 1))

        if (self.x <= self.radius):
            return 1
        if (self.x >= width - self.radius):
            return 2
        if (self.y <= self.radius) or (self.y > height - self.radius):
            self.speed *= 1.05
            self.vector = self.vector.reflect(vertical)
            self.vector.scale_to_length(self.speed)
            return 0
        if (self.rect.collideobjects(paddles)):
            self.speed *= 1.05
            self.vector = self.vector.reflect(horizontal)
            self.vector.scale_to_length(self.speed)
            return 0
        return -1


    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius)

class Paddle():
    def __init__(self, screen):
        self.rect = pygame.Rect(0, 0, 10, 150)
        self.pos = screen.get_height() / 2
        self.rect.centery = self.pos

    def move_paddle(self, screen, dt, direction):
        (width, height) = screen.get_size()
        if (direction == "up") and (self.rect.top > 0):
            self.pos -= 300 * dt
        elif (direction == "down") and (self.rect.bottom < height):
            self.pos += 300 * dt
        self.rect.centery = self.pos
    
    def reset_pos(self, screen):
        self.pos = screen.get_height() / 2
        self.rect.centery = self.pos

class Button():
    def __init__(self, text, x, y, id):
        self.text = text
        self.x = x
        self.y = y
        self.id = id

    def draw(self, screen, font, game_state):
        action = False

        border = pygame.Surface((204, 104))
        border = border.convert()
        if (self.id == game_state.selected_button_id):
            border.fill("white")
        else:
            border.fill("black")

        text_background = pygame.Surface((200, 100))
        text_background = text_background.convert()
        text_background.fill("black")
        
        text = pygame.font.Font.render(font, self.text, 1, "white")
        text_rect = text.get_rect(center=(text_background.get_width() / 2, text_background.get_height() / 2))
        
        text_background.blit(text, text_rect)
        border.blit(text_background, (2, 2))
        screen.blit(border, (self.x, self.y))

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_RETURN]) and (self.id == game_state.selected_button_id):
            action = True
        
        return action

class GameState():
    def __init__(self):
        self.dt = 0
        self.player_score = 0
        self.computer_score = 0
        self.balls = []
        self.bounces = 0
        self.added = False
        self.running = True
        self.selected_button_id = 0

def reset(game_state, screen, player_paddle, computer_paddle):
    game_state.__init__()
    player_paddle.reset_pos(screen)
    computer_paddle.reset_pos(screen)

def end_screen(screen, font, game_state, player_paddle, computer_paddle):
    (width, height) = screen.get_size()
    rematch_button = Button("Rematch", 100, 300, 0)
    exit_button = Button("Quit", 400, 300, 1)

    if (game_state.player_score < game_state.computer_score):
            text = pygame.font.Font.render(font, "You lost", 1, "white")
    elif (game_state.player_score > game_state.computer_score):
        text = pygame.font.Font.render(font, "You won", 1, "white")
    else:
        text = pygame.font.Font.render(font, "Tie", 1, "white")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game_state.selected_button_id = 0
    elif keys[pygame.K_RIGHT]:
        game_state.selected_button_id = 1

    text_rect = text.get_rect(center=(width/2, height/2))
    screen.fill("black")
    screen.blit(text, text_rect)
    
    if rematch_button.draw(screen, font, game_state):
        reset(game_state, screen, player_paddle, computer_paddle)
    if exit_button.draw(screen, font, game_state):
        game_state.running = False


def continue_game(screen, font, game_state, player_paddle, computer_paddle):
    (width, height) = screen.get_size()
    angles = list(range(-45, 46)) + list(range(135, 226))

    if (game_state.bounces % 3 == 0 and game_state.added == False) or (len(game_state.balls) == 0):
        new_ball = Ball(width / 2, random.randint(30, height - 30), random.choice(angles))
        game_state.balls.append(new_ball)
        game_state.added = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_paddle.move_paddle(screen, game_state.dt, "up")
    elif keys[pygame.K_DOWN]:
        player_paddle.move_paddle(screen, game_state.dt, "down")

    closest_ball = max(game_state.balls, key=lambda item: item.x)
    if (closest_ball.y < computer_paddle.rect.centery):
        computer_paddle.move_paddle(screen, game_state.dt, "up")
    elif (closest_ball.y > computer_paddle.rect.centery):
        computer_paddle.move_paddle(screen, game_state.dt, "down") 

    screen.fill("black")
    pygame.draw.rect(screen, "white", player_paddle)
    pygame.draw.rect(screen, "white", computer_paddle)

    to_pop = []
    for i in range(len(game_state.balls)):
        game_state.balls[i].update_pos(game_state.dt)
        res = game_state.balls[i].check_collision(screen, [player_paddle, computer_paddle])
        if (res > 0):
            to_pop.append(i)
            if (res == 1): game_state.computer_score += 1
            elif (res == 2): game_state.player_score += 1
        if (res == 0):
            game_state.bounces += 1
            game_state.added = False

        game_state.balls[i].draw(screen)

    to_pop.reverse()
    for i in to_pop:
        game_state.balls.pop(i)

    text = pygame.font.Font.render(font, f"{game_state.player_score} | {game_state.computer_score}", 1, "white")
    text_rect = text.get_rect()
    text_rect.centerx = width / 2
    text_rect.top = 10
    screen.blit(text, text_rect)