# Pong using MCP3008 and two potentiometers
# Run through Pygame Zero (pgzrun)
# Updated version with scoring - first to 11 points
# (does not need the 2 point lead)
import time
from mcp3008 import MCP3008

WIDTH = 1280
HEIGHT = 720

mcp = MCP3008()

WHITE = (255,255,255)
player0_color = (0, 0, 255)
player1_color = (0, 255, 0)


player0_pos = mcp.read_adc(0)
player1_pos = mcp.read_adc(1)

#starting positions
ball_x = 640
ball_y = 360
ball_speed = 5 # default 5
ball_velocity = [1 * ball_speed, 0.5 * ball_speed]
ball_radius = 10

paddle_height = 80
paddle_width = 20

scores = [0,0]

# Rectangle representing paddles
paddle_rect = [(0,0),(0,0)]

# Ratio screen (720) to adc (1024)
height_constant = 1.5

game_state = "play"
game_winner = 0
    
def draw():
    screen.clear()
    # Display score
    screen.draw.text(str(scores[0]), (300, 100), fontsize=120, color=player0_color)
    screen.draw.text(str(scores[1]), (900, 100), fontsize=120, color=player1_color)
    if (game_state == "gameover"):
        # To make more user friendly change player 0 to 1, and 1 to 2
        screen.draw.text("Player {} wins!".format(game_winner+1), (200, 250), fontsize=120)
    else:
        draw_paddle(screen, 0, color=player0_color)
        draw_paddle(screen, 1, color=player1_color)
        draw_ball(screen, ball_x, ball_y, ball_radius)
    
def update():
    global paddle_rect, player0_pos, player1_pos, ball_x, ball_y, ball_velocity, game_state, game_winner, scores
    adc0 = mcp.read_adc(0)
    adc1 = mcp.read_adc(1)
    player0_pos = HEIGHT - int(adc0 / height_constant) - paddle_height
    player1_pos = HEIGHT - int(adc1 / height_constant) - paddle_height
    paddle_rect[0] = Rect((40, player0_pos), (paddle_width, paddle_height))
    paddle_rect[1] = Rect((WIDTH-40, player1_pos), (paddle_width, paddle_height))
    # Update ball position
    ball_x += int(ball_velocity[0])
    ball_y += int(ball_velocity[1])
    
    # check for game over (allows paddles to move, but no ball)
    if game_state == "gameover":
        return
    
    # Hits wall = score point
    if (ball_x - ball_radius <= 0):
        # player 1 scores if passes left
        scores[1] += 1
        if scores[1] >= 11:
            game_winner = 1
            game_state = "gameover"
        else:
            reset_ball(1)
    elif (ball_x + ball_radius >= WIDTH):
        # player 0 scores if passes right
        scores[0] += 1
        if scores[0] >= 11:
            game_winner = 0
            game_state = "gameover"
        else:
            reset_ball(-1)
        # Collides with paddle - checks centre of the ball
    elif (paddle_rect[0].collidepoint (ball_x, ball_y)):
        deflect_ball (0)
    elif (paddle_rect[1].collidepoint (ball_x, ball_y)):
        deflect_ball (1)
        
    # Hit top or bottom (bounce)
    if (ball_y + ball_radius >= HEIGHT or ball_y - ball_radius <= 0):
        ball_velocity[1] = ball_velocity[1] * -1
        
    # Increase speed of ball - quick increase
    # Max speed 20
    if ball_velocity[0] < 20 and ball_velocity[0] > -20:
        ball_velocity[0] = ball_velocity[0] * 1.001
        ball_velocity[1] = ball_velocity[1] * 1.001
        
# player left = 0, right = 1
def draw_paddle(screen, player, color=WHITE):
    if player == 0:
        screen.draw.filled_rect(paddle_rect[0], color)
    else:
        screen.draw.filled_rect(paddle_rect[1], color)
    
def draw_ball(screen, ball_x, ball_y, ball_radius=10, ball_color=WHITE):
    screen.draw.filled_circle ((ball_x,ball_y), ball_radius, ball_color)
        
def deflect_ball (player):
    global ball_velocity, ball_x, ball_y
    # reverse horizontal direction
    ball_velocity[0] = ball_velocity[0] * -1
    # also move the ball 2 pixels away to prevent it getting stuck
    if player == 0 :
       ball_x += 2
    else :
        ball_x -= 2
    # if moving down
    if ball_velocity[1] > 0:
        if ball_y < paddle_rect[player].y + (paddle_height / 3):
            ball_velocity[1] = ball_velocity[1] * 0.5
        elif ball_y > paddle_rect[player].y + 2 * (paddle_height / 3):
            ball_velocity[1] = ball_velocity[1] * 1.5
        # If central part of paddle then no change
    else:
        if ball_y < paddle_rect[player].y + (paddle_height / 3):
            ball_velocity[1] = ball_velocity[1] * 1.5
        elif ball_y > paddle_rect[player].y + 2 * (paddle_height / 3):
            ball_velocity[1] = ball_velocity[1] * 0.5
        # If central part of paddle then no change


# Direction is whether to go to left or right
# 1 = to right, -1 = to left
def reset_ball (direction=1):
    # Resets the ball position and velocity
    global ball_x, ball_y, ball_velocity
    ball_x = 640
    ball_y = 360
    ball_velocity = [1 * ball_speed * direction, 0.5 * ball_speed]